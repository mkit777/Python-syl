#!/usr/bin/env python3
import sys
import multiprocessing as mp
import os
#存储配置文件
class Config(object):
    #初始化，通过文件实例化Config对象
    def __init__(self,dir):
        #检查文件是否存在
        if not os.path.exists(dir):
            raise FileNotFoundError()
        #创建一个字典，用于存储配置信息
        self.__config={}
        with open(dir) as file:
            for data in file：
                index, val = data.split('=')
                self.__config[index.strip()]=float(val.strip())
    #获得基数下线值
    @property
    def jishuh(self):
        return self.__config['JiShuH']
    #获得基数上线值
    @property
    def jishul(self):
        return self.__config['JiShuL']
    #获得税率数据
    def values(self):
        ret=[]
        for x in self.__config:
            #去除基数上下限数据
            if x == 'JiShuH' or x == 'JiShuL':
                continue
            #将其他数据加入列表中
            ret.append(self.__config[x])
        return ret
#存储数据文件
class UserData(object):
    #初始化，通过文件实例化UeserData对象
    def __init__(self,dir):
        #建立一个字典，用于存储用户信息
        self.__userdata={}
        if not os.path.exists(dir):
            raise FileNotFoundError()
        with open(dir) as file:
            for data in file:
                id, salary = data.split(',')
                self.__userdata[int(id.strip())]={'salary':float(salary.strip())}
    #更新数据
    def update(self,id,**datas):
        for k,v in datas.items(): 
            self.__userdata[id][k]=v
    #得到相应数据
    def get(self,id=-1,key=None):
        #得到所有数据
        if id <= 0 and key==None:
            return self.__userdata
        #得到指定用户数据
        elif id>0 and key == None:
            return self.__userdata[id]
        #得到指定用户的指定keyy值数据
        elif id>0 and key != None:
            return self.__userdata[id][key]
        #否则报错
        else:
            raise TypeError()
#用于计算
class Taxcalculator(object):
    #通过Config实例初始化Taxcalculator对象
    def __init__(self,config):
        self.__config=config
    #指定UserData对象后进行计算
    def calculate(self,userdata):
        self.__userdata=userdata
        for id in userdata.get():
            #计算社会保险
            self.__ccl_social_insurance(id)
            #计算应纳税额
            self.__ccl_tax_amount(id)
            #计算税后工资
            self.__ccl_taxable_income(id)
    #控制台展示数据
    def showret(self):
        data=self.__userdata.get()
        for x in data:
            print('{},{:.0f},{:.2f},{:.2f},{:.2f}'.format(x,data[x]['salary'],data[x]['si'],data[x]['ta'],data[x]['ti']))
    #将结果保存到指定文件
    def saveret(self,filename):
        data=self.__userdata.get()
        with open(filename,'w') as file:
            for x in data:
                file.write('{},{:.0f},{:.2f},{:.2f},{:.2f}\n'.format(x,data[x]['salary'],data[x]['si'],data[x]['ta'],data[x]['ti']))
    #计算社会保险
    def __ccl_social_insurance(self,id):
        #datermine salary
        salary=self.__userdata.get(id,'salary')
        if salary<self.__config.jishul:
           _salary=self.__config.jishul
        elif salary>self.__config.jishuh:
           _salary=self.__config.jishuh
        else:
           _salary=salary
            
        #load ratio
        insurance_ratios = self.__config.values()
        #count social insurance
        social_insurance=0
        for insurance_ratio in  insurance_ratios:
            social_insurance += salary * insurance_ratio
        self.__userdata.update(id,si=social_insurance)
    #计算应纳税额
    def __ccl_tax_amount(self,id): 
        data=self.__userdata.get(id)
        pre_taxable_income = data['salary']-data['si']-3500
        #judge taxable income and quick deduction
        if pre_taxable_income<=0:
            tx,qd=0,0
        elif pre_taxable_income<=1500:  
            tx,qd=0.03,0
        elif pre_taxable_income<=4500:
            tx,qd=0.1,105
        elif pre_taxable_income<=9000:
            tx,qd=0.2,555
        elif pre_taxable_income<=35000:
            tx,qd=0.25,1005
        elif pre_taxable_income<=55000:
            tx,qd=0.3,2755
        elif pre_taxable_income<=80000:
            tx,qd=0.35,5505
        else:
            tx,qd=0.45,13505
        #calculate tax_amount
        tax_amount = pre_taxable_income*tx-qd
        tax_amount = tax_amount if tax_amount>0 else 0
        self.__userdata.update(id,ta=tax_amount)
    #计算税后工资
    def __ccl_taxable_income(self,id):
        data= self.__userdata.get(id)
        taxable_income = data['salary']-data['si']-data['ta']
        self.__userdata.update(id,ti=taxable_income)
#处理参数相关
class Args(object):
    def __init__(self):
        #检查参数是否正确
        self.__check()
        #将参数以字典形式存储
        self.__argv={}
        for i,arg in enumerate(sys.argv[1:]):
            #偶数为key
            if i%2==0:
                key=arg.strip('-')
                self.__argv[key]=None
            #基数为value
            else:
                self.__argv[key]=arg
    #检查参数
    def __check(self):
        #检查数量
        if len(sys.argv)!=7:
            print('Parameter Error.')
            sys.exit(-1)
        #检查参数名是否正确
        parameters = ('-c','-d','-o')
        for parameter in parameters:
            if parameter not in sys.argv:
                print('Parameter Error.')
                sys.exit(-1)
    #得到指定参数 
    def get(self,key=None):
        #返回所有参数
        if key==None:
            return self.__argv
        #返回指定key参数值
        return self.__argv[key]

#进程1，用于读取用户数据文件
def initUserdata(args,queue):
    queue.put(UserData(args['d']))

#进程2，读取配置文件，并计算
def calculate(args,queue1,queue2):
    config=Config(args['c'])
    tc=Taxcalculator(config)
    #获得用户数据并计算
    tc.calculate(queue1.get())
    queue2.put(tc)

def saveret(args,queue):
    #获得结果并保存
    tx=queue.get()
    #tx.showret()
    tx.saveret(args['o'])

    
if __name__=="__main__":
    args_instance=Args()
    args=args_instance.get()
    queue1=mp.Queue()
    queue2=mp.Queue()
    p1=mp.Process(target=initUserdata,args=(args,queue1))
    p2=mp.Process(target=calculate,args=(args,queue1,queue2))
    p3=mp.Process(target=saveret,args=(args,queue2))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
