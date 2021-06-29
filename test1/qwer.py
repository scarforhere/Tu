# coding: utf-8
"""
-------------------------------------------------
   File Name:      1
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date:           2021-06-29 10:46 AM
-------------------------------------------------
Description : 

    Print info with under format:

"""
import multiprocessing
from globle_variante import GlobalValue
from cont import cont
from a import printtest1,printtest2
import a

GlobalValue()

num_process=3

pool = multiprocessing.Pool(num_process+1)

# pool.apply_async(func=cont)
pool.apply_async(func=printtest1)
# pool.apply_async(func=printtest2)


pool.close()
pool.join()


