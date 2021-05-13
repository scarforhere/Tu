# coding: utf-8
"""
-------------------------------------------------
   File Name：     main_ProcessSingle.py
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date：          2021-05-01 09:38 AM
-------------------------------------------------
Description :

    Program runs on Single Process Line

    # # # # # # # # # # # # # # # # # # # # #
    #         Debug Single Process          #
    # Don't run for Project with multi path #
    # # # # # # # # # # # # # # # # # # # # #

"""
from data_plot import data_plot
from data_convert import data_convert
from excel_write import excel_write
from get_all_files import get_all_files
from time_record import TimeMonitor

t_total = TimeMonitor()

path = r"E:\Python_Code\Tu\Data"


txt_list = get_all_files(path)

for path in txt_list:
    t = TimeMonitor(f'\tSub Time', 25)

    print(f"Working on {path}")
    data, data_effect, data_avg = data_convert(path)
    data_plot(path, data, data_effect, data_avg)
    excel_write(path, data)

    t.show()

t_total.show()
