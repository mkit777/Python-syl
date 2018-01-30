#!/usr/bin/env python3
import sys
import multiprocessing as mp
class Config(object):

    def __init__(self,dir):
        #if not sys.path.exist(dir)
           # raise FileNotFoundError()
        self.__config={}
        with open(dir) as file:
            for data in file:
                index, val = data.split('=')
                self.__config[index.strip()]=float(val.strip())
    @property
    def jishuh(self):
        return self.__config['JiShuH']
    @property
    def jishul(self):
        return self.__config['JiShuL']
    #@property
    def values(self):
        ret=[]
        for x in self.__config:
            if x == 'JiShuH' or x == 'JiShuL':
                continue
            ret.append(self.__config[x])
        return ret

class UserData(object):

    def __init__(self,dir):
        self.__userdata={}
        with open(dir) as file:
            for data in file:
                id, salary = data.split(',')
                self.__userdata[int(id.strip())]={'salary':float(salary.strip())}

    def update(self,id,**datas):
        for k,v in datas.items(): 
            self.__userdata[id][k]=v

    def get(self,id=-1,key=None):
        if id <= 0 and key==None:
            return self.__userdata
        elif id>0 and key == None:
            return self.__userdata[id]
        elif id>0 and key != None:
            return self.__userdata[id][key]
        else:
            raise TypeError()

class Taxcalculator(object):
    def __init__(self,config):
        self.__config=config

    def calculate(self,userdata):
        self.__userdata=userdata
        for id in userdata.get():
            self.__ccl_social_insurance(id)
            self.__ccl_tax_amount(id)
            self.__ccl_taxable_income(id)

    def showret(self):
        data=self.__userdata.get()
        for x in data:
            print('{},{:.0f},{:.2f},{:.2f},{:.2f}'.format(x,data[x]['salary'],data[x]['si'],data[x]['ta'],data[x]['ti']))
    def saveret(self,filename):
        data=self.__userdata.get()
        with open(filename,'w') as file:
            for x in data:
                file.write('{},{:.0f},{:.2f},{:.2f},{:.2f}\n'.format(x,data[x]['salary'],data[x]['si'],data[x]['ta'],data[x]['ti']))

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
    
    def __ccl_tax_amount(self,id): 
        data=self.__userdata.get(id)
        pre_taxable_income =data['salary']-data['si']-3500
        #judge taxable income and quick deduction
        if pre_taxable_income<0:
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
        tax_amount=pre_taxable_income*tx-qd
        self.__userdata.update(id,ta=tax_amount)

    def __ccl_taxable_income(self,id):
        data= self.__userdata.get(id)
        taxable_income = data['salary']-data['si']-data['ta']
        self.__userdata.update(id,ti=taxable_income)

class Args(object):

    def __init__(self):
        self.__check()
        self.__argv={}
        for i,arg in enumerate(sys.argv[1:]):
            if i%2==0:
                key=arg.strip('-')
                self.__argv[key]=None
            else:
                self.__argv[key]=arg
    
    def __check(self):
        if len(sys.argv)!=7:
            print('Parameter Error.')
            sys.exit(-1)

        parameters = ('-c','-d','-o')
        for parameter in parameters:
            if parameter not in sys.argv:
                print('Parameter Error.')
                sys.exit(-1)
 
    def get(self,key=None):
        if key==None:
            return self.__argv
        return self.__argv[key]

def initUserdata(args,queue):
    queue.put(UserData(args['d']))

def calculate(args,queue1,queue2):
    config=Config(args['c'])
    tc=Taxcalculator(config)
    tc.calculate(queue1.get())
    queue2.put(tc)

def saveret(args,queue):
    tx=queue.get()
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
