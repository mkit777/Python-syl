#!/usr/bin/env python3
import sys

if __name__=="__main__":
    try:
        if len(sys.argv) != 2 :  #check peremeters type
            raise TypeError()
        get=int(sys.argv[1])
    except:
        print("Parameter Error")

    sde=get-3500  #count ge ren suo de e
    #judge sl
    if sde<=1500:
        sl,kc=0.03,0
    elif sde<=4500:
        sl,kc=0.1,105
    elif sde<=9000:
        sl,kc=0.2,555
    elif sde<=35000:
        sl,kc=0.25,1005
    elif sde<=55000:
        sl,kc=0.3,2755
    elif sde<=80000:
        sl,kc=0.35,5505
    else:
        sl,kc=0.45,13505
    # count ret
    se=sde*sl-kc
    print(format(se,".2f"))
