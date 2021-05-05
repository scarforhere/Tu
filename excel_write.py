# coding: utf-8
"""
-------------------------------------------------
   File Name：     excel_write.py
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date：          2021-05-03 11:57 PM
-------------------------------------------------
Description : 

    Create Excel with path and data_dict

"""
import pandas as pd
import os
from time_record import TimeMonitor


def excel_write(path: str, data_dict: dict):
    """
    Create Excel with path and data_dict

    :param path: Path of target EXCEL
    :param data_dict: Dict to generate DataFrame
    """
    t = TimeMonitor('\tGenerate Excel Time', 25)

    # TODO Rewrite Header of EXCEL
    # crate dict{} for DataFrame
    excel_dict = {'Time [s]': data_dict['s'],
                  'Fx [N]': data_dict['fx'],
                  'Fy [N]': data_dict['fy'],
                  'Fz [N]': data_dict['fz'],
                  # 'F4 [N]': data_dict['f4'],
                  # 'F5 [N]': data_dict['f5']
                  }

    # create Dataframe
    df = pd.DataFrame(excel_dict)

    # write data into Excel
    excel_path_split = os.path.split(path)
    excel_path_splitext = os.path.splitext(excel_path_split[1])
    excel_path_list = [excel_path_split[0], '\\', excel_path_splitext[0], '.xlsx']
    excel_path = ''.join(excel_path_list)
    df.to_excel(excel_path, index=False)

    return t.trans()
