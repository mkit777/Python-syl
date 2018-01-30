#!/usr/bin/env python3
import sys

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

    #@property
    def items(self):
        return self.__congfig.itmes()

class UserData(object):
    #init
    def __init__(self,dir):
        self.__userdata={}
        with open(dir) as file:
            for data in file:
                id, salary = data.split(',')
                self.__userdata[int(id.strip())]=[float(salary.strip())]

    def adddata(self,id,*datas):
        for data in datas: 
            self.__userdata[id].append(data)

    def getdata(self,id=-1):
        if id <= 0:
            return self.__userdata
        else:
            return self.__userdata[id]
    
    def getsalary(self,id):
        return self.__userdata[id][0]
class Taxcalculator(object):
    def __init__(self,config):
        self.__config=config

    def calculate(self,userdata):
        self.__userdata=userdata
        for id in self.__userdata.getdata():
            self.__ccl_social_insurance(id)
            self.__ccl_tax_amount(id)
            self.__ccl_taxable_income(id)

    def showret(self):
        data=self.__userdata.getdata()
        for x in data:
            print('{},{:.0f},{:.2f},{:.2f},{:.2f}'.format(x,data[x][0],data[x][1],data[x][2],data[x][3]))
    def saveret(self,filename):
        data=self.__userdata.getdata()
        with open(filename,'w') as file:
            for x in data:
                file.write('{},{:.0f},{:.2f},{:.2f},{:.2f}\n'.format(x,data[x][0],data[x][1],data[x][2],data[x][3]))

    def __ccl_social_insurance(self,id):
        #datermine salary
        if self.__userdata.getsalary(id)<self.__config.jishul:
            salary=self.__config.jishul
        elif self.__userdata.getsalary(id)>self.__config.jishuh:
            salary=self.__config.jishuh
        else:
            salary=self.__userdata.getsalary(id)
            
        #load ratio
        insurance_ratios = self.__config.values()
        #count social insurance
        social_insurance=0
        for insurance_ratio in  insurance_ratios:
            social_insurance += salary * insurance_ratio
        self.__userdata.adddata(id,social_insurance)
    
    def __ccl_tax_amount(self,id): 
        data = self.__userdata.getdata(id)
        _ =data[0]-data[1]-3500
        taxable_income = _ if _>0 else 0 
        #judge taxable income and quick deduction
        if taxable_income<=1500:  
            tx,qd=0.03,0
        elif taxable_income<=4500:
            tx,qd=0.1,105
        elif taxable_income<=9000:
            tx,qd=0.2,555
        elif taxable_income<=35000:
            tx,qd=0.25,1005
        elif taxable_income<=55000:
            tx,qd=0.3,2755
        elif taxable_income<=80000:
            tx,qd=0.35,5505
        else:
            tx,qd=0.45,13505
        #calculate tax_amount
        tax_amount=taxable_income*tx
        self.__userdata.adddata(id,tax_amount-qd)
    def __ccl_taxable_income(self,id):
        data= self.__userdata.getdata(id)
        taxable_income = data[0]-data[1]-data[2]
        self.__userdata.adddata(id,taxable_income)
class Args(object):
    def __init__(self):
        self.args=sys.argv[1:]
    def check(self):
        if len(self.args)!=6:
            print('Parameter Error')
            sys.exit(-1)
    def getargs(self): 
        return self.__args('-c'),self.__args('-d'),self.__args('-o')
    def __args(self,parameter):
        return self.args[self.args.index(parameter)+1]
if __name__=="__main__":
    args=Args()
    args.check()
    ret=args.getargs()
    config=Config(ret[0])
    userdata=UserData(ret[1])
    tc=Taxcalculator(config)
    tc.calculate(userdata)
    #tc.showret()
    tc.saveret(ret[2])
