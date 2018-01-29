#!/usr/bin/env python3
import sys
def calculate(salary):
    if not isinstance(salary,int):
        raise TypeError()
    #count social insurance
    insurance_ratios = (0.08,0.02,0.005,0,0,0.06)
    social_insurance=0
    for insurance_ratio in  insurance_ratios:
        social_insurance += salary * insurance_ratio
    taxable_income = salary-social_insurance-3500
    if taxable_income <0:
        taxable_income=0 
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
    #count ret
    tax = taxable_income * tx - qd   
    return salary - tax - social_insurance

if __name__=="__main__":
    try:
        if len(sys.argv) <2:
            raise TypeError()
        usrdict={}   
        for arg in sys.argv[1:]:
            work_number,salary=arg.split(':')
            usrdict[work_number]=calculate(int(salary))
            print(work_number+':'+format(usrdict[work_number],'.2f'))
    except:
        print('Parameter Error')
