import sys
from multiprocessing import Process, Queue

'''
解析参数
解析配置文件
解析数据文件
计算结果
保存结果
'''


class Args(object):
    '''
    解析命令行参数
    '''

    def __init__(self, argv):
        '''
        Args:
            argv (sys.argv):传入命令行参数，初始化Args对象
        '''
        self.argv = argv

    def __parse_args(self, arg):
        '''
        Args:
            arg (str):传入参数名，返回对应值
        '''
        try:
            value = self.argv[self.argv.index(arg) + 1]
        except (ValueError, IndexError):
            return
        return value

    def getarg(self, arg):
        '''
        Args:
            arg (str)：传入参数名，返回对应值
        '''
        return self.__parse_args(arg)


class Congfig(object):

    def __init__(self, filedir):
        self.jishul, self.jishuh, self.total_rate = self.__parse_file(filedir)

    def __parse_file(self, filedir):
        total_rate = 0
        with open(filedir) as file:
            for line in file:
                key, value = line.split('=')
                key = key.strip()
                value = float(value.strip())
                if key == 'JiShuL':
                    jishul = value
                elif key == 'JiShuH':
                    jishuh = value
                else:
                    total_rate += value

        return jishul, jishuh, total_rate


class UserData(Process):

    def __init__(self, filedir, outqueue):
        super().__init__()
        self.outqueue = outqueue
        self.filedir = filedir

    def __parse(self, filedir):
        with open(filedir) as file:
            for line in file:
                userid, salary = line.split(',')
                yield int(userid), int(salary)

    def run(self):
        for data in self.__parse(self.filedir):
            self.outqueue.put(data)
            print('---------------------->', data)


class Calculator(Process):
    INCOME_TAX_QUICK_LOOKUP_TABLE = [
        (80000, 0.45, 13505),
        (55000, 0.35, 5505),
        (35000, 0.30, 2755),
        (9000, 0.25, 1005),
        (4500, 0.2, 555),
        (1500, 0.1, 105),
        (0, 0.03, 0)
    ]

    INCOME_TAX_START_POINT = 3500

    def __init__(self, congfig, inqueue, outqueue):
        super().__init__()
        self.inqueue = inqueue
        self.outqueue = outqueue
        self.congfig = congfig

    def calculate(self, item):
        shebao = self.__calculate_social_insurance(item)
        taxable_salary = item[1] - shebao - Calculator.INCOME_TAX_START_POINT
        if taxable_salary > 0:
            for reference in Calculator.INCOME_TAX_QUICK_LOOKUP_TABLE:
                if taxable_salary > reference[0]:
                    tax = taxable_salary * reference[1] - reference[2]
                    break
        else:
            tax = 0
        final_salary = item[1] - shebao - tax

        return str(item[0]), str(item[1]), '{:.2f}'.format(shebao), '{:.2f}'.format(tax), '{:.2f}'.format(final_salary)

    def __calculate_social_insurance(self, item):
        if item[1] < self.congfig.jishul:
            return self.congfig.jishul * self.congfig.total_rate
        elif item[1] > self.congfig.jishuh:
            return self.congfig.jishuh * self.congfig.total_rate
        return item[1] * self.congfig.total_rate

    def run(self):
        while True:
            try:
                data = self.inqueue.get(timeout=1)
                ret = self.calculate(data)
            except:
                print('------------task complete----------------')
                return
            self.outqueue.put(ret)
            print('-------------------------->', ret)


class Exporter(Process):
    def __init__(self, filedir, queue):
        super().__init__()
        self.queue = queue
        self.file = open(filedir, 'w')

    def export(self, data):
        print(data)
        self.file.write(','.join(data)+'\n')

    def run(self):
        print('='*20)
        while True:
            try:
                print('+' * 15)
                line = self.queue.get(timeout=1)
                print('<---------------------------', line)
                self.export(line)
            except:
                print('----------------error-------------')
                self.file.close()
                return


if __name__ == '__main__':
    q1 = Queue()
    q2 = Queue()

    args = Args(sys.argv)
    config = Congfig(args.getarg('-c'))
    calculator = Calculator(config, q1, q2)
    userdata = UserData(args.getarg('-d'), q1)
    exporter = Exporter(args.getarg('-o'), q2)

    exporter.start()
    calculator.start()
    userdata.start()

    calculator.join()
    userdata.join()
    exporter.join()
