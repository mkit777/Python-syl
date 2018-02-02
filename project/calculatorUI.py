#!/usr/bin/python3 
from tkinter import *
caled = False
lastret=0
def updateDisplay(buttonString):
    content=display.get()
    global caled
    if caled:
        lastret=eval(content.split('=')[1].strip())
        display.set(str(lastret)+buttonString)
        caled = False
        return
    if content=='0':
        content=''
    display.set(content+buttonString)

def calculate():
    global caled
    if caled:
        return
    result = eval(display.get())
    display.set(display.get()+'\n='+str(result))
    caled=True

def clear():
    global caled
    display.set('0')
    caled=False

def backspace():
    content = display.get()
    global caled
    if caled:
        content=content.split('=')[0].strip()
    if len(content) == 1:
        display.set('0')
        return
    display.set(content[:-1])
    caled=False

mainUI=Tk()
mainUI.title('Calculator')
mainUI.geometry('200x210+300+300')

display = StringVar()
display.set('0')

textlabel=Label(mainUI)
textlabel.grid(row=0,column=0,columnspan=4)
textlabel.config(bg='grey',width=28,height=3,anchor=SE)
textlabel['textvariable']=display

clearbutton = Button(mainUI,text='C',fg='orange',width=3,command=clear)
clearbutton.grid(row=1,column=0)
Button(mainUI,text='Del',width=3,command=backspace).grid(row=1,column=1)
Button(mainUI,text='/',width=3,command=lambda:updateDisplay('/')).grid(row=1,column=2)
Button(mainUI,text='*',width=3,command=lambda:updateDisplay('*')).grid(row=1,column=3)
Button(mainUI,text='7',width=3,command=lambda:updateDisplay('7')).grid(row=2,column=0)
Button(mainUI,text='8',width=3,command=lambda:updateDisplay('8')).grid(row=2,column=1)
Button(mainUI,text='9',width=3,command=lambda:updateDisplay('9')).grid(row=2,column=2)
Button(mainUI,text='-',width=3,command=lambda:updateDisplay('-')).grid(row=2,column=3)
Button(mainUI,text='4',width=3,command=lambda:updateDisplay('4')).grid(row=3,column=0)
Button(mainUI,text='5',width=3,command=lambda:updateDisplay('5')).grid(row=3,column=1)
Button(mainUI,text='6',width=3,command=lambda:updateDisplay('6')).grid(row=3,column=2)
Button(mainUI,text='+',width=3,command=lambda:updateDisplay('+')).grid(row=3,column=3)
Button(mainUI,text='1',width=3,command=lambda:updateDisplay('1')).grid(row=4,column=0)
Button(mainUI,text='2',width=3,command=lambda:updateDisplay('2')).grid(row=4,column=1)
Button(mainUI,text='3',width=3,command=lambda:updateDisplay('3')).grid(row=4,column=2)
Button(mainUI,text='=',width=3,command=calculate).grid(row=4,column=3,rowspan=2)
Button(mainUI,text='0',width=10,command=lambda:updateDisplay('0')).grid(row=5,column=0,columnspan=2)
Button(mainUI,text='.',width=3,command=lambda:updateDisplay('.')).grid(row=5,column=2)

mainUI.mainloop()
