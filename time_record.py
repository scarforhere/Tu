# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     time_record
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date：          2021-05-04 12:33 AM
-------------------------------------------------
Description : 

    Simplified time output
    t = Time_Monitor("Used Time", 20)

    # # # # # # # #
    #  code block #
    # # # # # # # #

    t.show()

"""
from datetime import datetime


class Time_Monitor(object):

    def __init__(self, text='Total Time', num=0):
        self.start = datetime.now()
        self.end = None
        self.text = text
        self.num = num

    def show(self):
        self.end = datetime.now()
        time_obj = self.end - self.start
        time_str_lst = [f"{self.text}: ".ljust(self.num), f"{time_obj.seconds}s".rjust(5)]
        time_str = ''.join(time_str_lst)
        print(time_str)
