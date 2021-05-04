# coding: utf-8
"""
-------------------------------------------------
   File Name：     main
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date：          2021-05-04 11:59 PM
-------------------------------------------------
Description : 

    Data Analysis
    Generate plots and excel files

"""
from main_ProcessMulti import main

path = input("Set Path of Target Folder:\n")
# Default: E:\Python_Code\Tu\Data

num = int(input("Set Proper Process Number for ProcessingPool:\n"))
# Default: 4

main(path, num)
