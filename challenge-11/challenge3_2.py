#! -*-coding:utf-8 -*-
#!/usr/bin/env python3

from openpyxl import load_workbook
from openpyxl import Workbook

import datetime

def combine():
    wb = load_workbook('courses.xlsx')
    sheet_stds= wb['students']
    for cell in sheet_stds['A']:
        print(type(cell.value))
        print(cell.value)

if __name__ =='__main__':
    combine()
