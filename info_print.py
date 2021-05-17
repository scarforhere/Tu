# coding: utf-8
"""
-------------------------------------------------
   File Name：     info_print
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date：          2021-05-04 11:47 PM
-------------------------------------------------
Description : 

    Print info with under format:


"""
from time_record import TimeMonitor


class InfoPrint(object):
    def __init__(self, path):
        self.t = TimeMonitor(f'\tSub Time', 25)
        self.path = path
        self.line = None
        self.t_convert = None
        self.t_plot = None
        self.t_excel = None

    def show(self):
        try:
            print(f'Sub Process Succeed!')
            print(f'\tPath: {self.path}')
            print(f"\tLine: {self.line}")
            if self.t_convert is not None:
                print(self.t_convert)
            if self.t_plot is not None:
                print(self.t_plot)
            if self.t_excel is not None:
                print(self.t_excel)
            self.t.show()
        except Exception as e:
            print(f'Sub Process Failed!')
            print(f'\tPath: {self.path}')
            print(f'\tFail Info: {e}')
