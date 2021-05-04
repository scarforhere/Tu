# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main.py
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date：          2021-05-01 09:38 AM
-------------------------------------------------
Description :



"""
from data_plot import data_plot
from data_transfer import data_transfer
from excel_write import excel_write
import os
from time_record import Time_Monitor

t_total = Time_Monitor()

path = r"E:\Python_Code\Tu\Data"
os.chdir(path)

txt_list = []

file_list = os.walk(path)

for dirpath, dirname, filename in file_list:
    for filename_item in filename:
        if filename_item.endswith(".txt"):
            path_full = "".join([dirpath, '\\', filename_item])
            txt_list.append(path_full)
        else:
            continue

for path in txt_list:
    t = Time_Monitor(f'\tSub Time', 25)

    print(f"Working on {path}")
    data, data_effect, data_avg = data_transfer(path)
    data_plot(path, data, data_effect, data_avg)
    excel_write(path, data)

    t.show()

t_total.show()
