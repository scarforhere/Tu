# coding: utf-8
"""
-------------------------------------------------
   Project :       Tu
   File Name :     regression
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date：          2021-05-12 09:44 PM
-------------------------------------------------
Description : 

    Fix the error caused by sensor
    Determine a file need to be fixed or not

"""
import os
import json
import numpy as np
from numpy import array
from readline_format import readline_format03

# TODO: Set Path of Messung_Problem.txt
g_path = r'E:\Python_Code\Tu\Important'


def read_res_regression(path):
    """
    Read regression's parameters from Fix_Data.txt

    :param path: Path of Fix_Data.txt
    :return: Values of a_fx, b_fx, a_fy, b_fy, a_fz, b_fz
    """
    with open(''.join([path, r'\Fix_Data.txt']), "r") as f:
        _data = f.read()
        fix_data_dict = json.loads(_data)

    a_fx = fix_data_dict['a_fx']
    b_fx = fix_data_dict['b_fx']
    a_fy = fix_data_dict['a_fy']
    b_fy = fix_data_dict['b_fy']
    a_fz = fix_data_dict['a_fz']
    b_fz = fix_data_dict['b_fz']

    return a_fx, b_fx, a_fy, b_fy, a_fz, b_fz


def write_res_regression(path):
    """
    Calculate the linear regression's parameters according to Messungs_Problem.tet
    Write regression's parameters into Fix_Data.txt

    :param path: Path of Fix_Data.txt
    :return: Values of a_fx, b_fx, a_fy, b_fy, a_fz, b_fz
    """
    # read total TXT file and count line's quantity
    with open(''.join([path, r'\Messung Problem.txt']), 'r') as f:
        data_total = f.readlines()

    s = []
    fx = []
    fy = []
    fz = []

    for data_line in data_total:
        data_list = readline_format03(data_line)
        s.append(data_list[0])
        fx.append(data_list[1])
        fy.append(data_list[2])
        fz.append(data_list[3])

    (a_fx, b_fx) = np.polyfit(s, fx, 1)
    (a_fy, b_fy) = np.polyfit(s, fy, 1)
    (a_fz, b_fz) = np.polyfit(s, fz, 1)

    fix_data_dict = {
        'a_fx': a_fx, 'b_fx': b_fx,
        'a_fy': a_fy, 'b_fy': b_fy,
        'a_fz': a_fz, 'b_fz': b_fz
    }

    with open(''.join([path, r'\Fix_Data.txt']), 'w') as f:
        _data = json.dumps(fix_data_dict)
        f.write(_data)

    return a_fx, b_fx, a_fy, b_fy, a_fz, b_fz


def regression(path):
    """
    Get the values of linear regression's parameters

    :param path: Path of Fix_Data.txt
    :return: a_fx, b_fx, a_fy, b_fy, a_fz, b_fz
    """
    dlist = os.listdir(path)
    flag = False
    for item in dlist:
        if item == 'Fix_Data.txt':
            flag = True
    if flag:
        a_fx, b_fx, a_fy, b_fy, a_fz, b_fz = read_res_regression(path)
    else:
        a_fx, b_fx, a_fy, b_fy, a_fz, b_fz = write_res_regression(path)

    return a_fx, b_fx, a_fy, b_fy, a_fz, b_fz


def fix_data(s_array, fx_array, fy_array, fz_array):
    """
    Fix the error caused by sensor

    :param s_array: Array of s point
    :param fx_array: Array of Fx point
    :param fy_array: Array of Fy point
    :param fz_array: Array of Fz point
    :return: fx, fy, fz
    """
    # TODO: Set path of regressions() according to the program
    a_fx, b_fx, a_fy, b_fy, a_fz, b_fz = regression(g_path)
    len_data = len(s_array)

    fx_fixed = fx_array - (a_fx * s_array + array([b_fx for _ in range(len_data)]))
    fy_fixed = fy_array - (a_fy * s_array + array([b_fy for _ in range(len_data)]))
    fz_fixed = fz_array - (a_fz * s_array + array([b_fz for _ in range(len_data)]))

    return fx_fixed, fy_fixed, fz_fixed


def determine_data(path):
    """
    Determine a file need to be fixed or not

    :param path: Path of Fix_Data.txt
    :return: True (need to be fixed) or False (no need to be fixed)
    """
    if path.rfind('T2mm') != -1:
        return False
    else:
        return True


def res_regression(path):
    """
    Check the linear regression's result

    :param path: Path of target TXT
    """
    from data_convert import data_convert
    import matplotlib.pyplot as plt
    import os

    data, data_effect, data_avg, _, _ = data_convert(path)

    plt.figure(figsize=(18, 6))

    s = data['s']
    fx = data['fx']
    fy = data['fy']
    fz = data['fz']

    l_f1, = plt.plot(s, fx, label='Fx_Error')
    l_f2, = plt.plot(s, fy, label='Fy_Error')
    l_f3, = plt.plot(s, fz, label='Fz_Error')

    s = np.linspace(0, 31.624969, 1012000)
    s_array = array(s)

    a_fx, b_fx, a_fy, b_fy, a_fz, b_fz = regression(r'E:\Python_Code\Tu\Important')
    fx_r = a_fx * s_array + array([b_fx for _ in range(1012000)])
    fy_r = a_fy * s_array + array([b_fy for _ in range(1012000)])
    fz_r = a_fz * s_array + array([b_fz for _ in range(1012000)])

    l_f4, = plt.plot(s, fx_r, label='Fx_Regression', linewidth=3.0)
    l_f5, = plt.plot(s, fy_r, label='Fy_Regression', linewidth=3.0)
    l_f6, = plt.plot(s, fz_r, label='Fz_Regression', linewidth=3.0)

    # fx_f, fy_f, fz_f = fix_data(s, fx, fy, fz)
    # l_f7, = plt.plot(s, fx_f, label='Fx_Fixed')
    # l_f8, = plt.plot(s, fy_f, label='Fx_Fixed')
    # l_f9, = plt.plot(s, fz_f, label='Fx_Fixed')

    plt.xlim((0, 31.624969))

    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')

    plt.title(f"{os.path.basename(path)}".replace('.txt', ''))

    plt.legend(handles=[l_f1, l_f2, l_f3, l_f4, l_f5, l_f6,
                        # l_f7, l_f8, l_f9
                        ],
               loc='best',  # TODO: Set Location of Legend
               )

    plt.savefig(f"{path.replace('.txt', '')}.png")


if __name__ == '__main__':
    _path = r'E:\Python_Code\Tu\Important\Messung Problem.txt'
    res_regression(_path)

    # _path = r'E:\Python_Code\Tu_Data\Trocken\T2mm V1-V8 -1\V1 T2mm 38 0,05 M1.txt'
    # print(determine_data(_path))
    # _path = r'E:\Python_Code\Tu\Data\Trocdsdfdfsdf0mm 38 0,05 M1.txt'
    # print(determine_data(_path))
