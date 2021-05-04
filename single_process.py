# coding: utf-8
"""
-------------------------------------------------
   File Name：     single_process
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date：          2021-05-04 11:48 PM
-------------------------------------------------
Description : 

    Single process in ProcessingPool

"""
from info_print import InfoPrint
from data_convert import data_convert
from data_plot import data_plot
from excel_write import excel_write


def single_process(path):
    """
    Operation for every TET file

    :param path: Path of target TXT file
    """
    print(f'Processing: {path}')
    info = InfoPrint(path)
    data, data_effect, data_avg, line, info.t_convert = data_convert(path)
    info.t_plot = data_plot(path, data, data_effect, data_avg)
    info.t_excel = excel_write(path, data)
    info.show()
