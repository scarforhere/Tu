# coding: utf-8
"""
-------------------------------------------------
   File Name:      a
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date:           2021-06-29 10:52 AM
-------------------------------------------------
Description : 

    Print info with under format:

"""
from globle_variante import GlobalValue
import os
import time

def printtest1():

    pid=os.getpid()
    GlobalValue.set_value(pid,False)

    for j in range(1,5):
        print(pid,j)
        time.sleep(1)

    GlobalValue.set_value(pid, True)

    for j in range(5,10):
        print(pid,j)
        time.sleep(1)

    GlobalValue.set_value(pid, False)

def printtest2():

    pid=os.getpid()
    GlobalValue.set_value(pid,False)


    for j in range(1,5):
        print(pid,j)
        time.sleep(1)

    GlobalValue.set_value(pid, False)

    for j in range(5,0):
        print(pid,j)
        time.sleep(1)




