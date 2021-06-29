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


def excel_write(path: str, data_dict: dict, data_effect: dict):
    """
    Create Excel with path and data_dict

    :param path: Path of target EXCEL
    :param data_dict: Dict to generate DataFrame
    :param data_effect: Dict to get start and end num
    """
    try:
        t = TimeMonitor('\tGenerate Excel Time', 25)

        # TODO Rewrite Header of EXCEL
        # crate dict{} for DataFrame
        excel_dict = {'Time [s]': data_dict['s'][data_effect['num_start']:data_effect['num_end']],
                      'Fx [N]': data_dict['fx'][data_effect['num_start']:data_effect['num_end']],
                      'Fy [N]': data_dict['fy'][data_effect['num_start']:data_effect['num_end']],
                      'Fz [N]': data_dict['fz'][data_effect['num_start']:data_effect['num_end']],
                      'u = Fx/Fz': data_dict['mu'][data_effect['num_start']:data_effect['num_end']],
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

    except Exception as e_info:
        print('Data Convert Failed!!!')
        print(f'\tFailed Path: {path}')
        print(f'\t{e_info}')
