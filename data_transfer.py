# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     data_transfer.py
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date：          2021-05-01 10:30 AM
-------------------------------------------------
Description :

    Sort data from TXT and transfer data, data_effect, data_avg in Dict type

"""
from numpy import *
from readline_format import readline_format02
from time_record import Time_Monitor


def data_transfer(file: str):
    """
    Sort data from TXT and transfer data, data_effect, data_avg in Dict type

    :param file: Path of file
    :return: data, data_effect, data_avg
    """
    t = Time_Monitor('\tData Transfer Time', 25)

    # 读取文件所有行并统计文件行数
    with open(file, 'r') as f:
        data_total = f.readlines()
    len_data = len(data_total)

    print(f"\tLine: {len_data}")

    # 初始化阵列空间
    s = []
    fx = []
    fy = []
    fz = []
    # f4 = []
    # f5 = []

    # 从文档中读取所有数值
    for data_line in data_total:
        data_list = readline_format02(data_line)

        # 为DataFrame构建DataDict
        s.append(data_list[0])
        fx.append(data_list[1])
        fy.append(data_list[2])
        fz.append(data_list[3])
        # f4.append(data_list[4])
        # f5.append(data_list[5])

    data = {'s': s,
            'fx': fx,
            'fy': fy,
            'fz': fz,
            # 'f4': f4,
            # 'f5': f5
            }

    # 初始化平均值数据字典
    data_avg = {}
    # 初始化有效值数据字典
    data_effect = {}

    # 平均值起始参数
    fx_ref = max(fx) * 0.8

    # 获取效数据起始点和平均值起始点    --->   平均值起始点肯定晚于有效数据起始点出现
    flag_num_start = False
    for i in range(len_data):
        # 捕获有效数据起始点
        if not flag_num_start:
            if abs(fx[i]) >= 20:
                data_effect['num_start'] = i
                flag_num_start = True
        # 捕获平均值起始点
        else:
            if abs(fx[i]) >= fx_ref:
                data_avg['num_start'] = i
                break
            else:
                continue

    # 获取效数据终止点和平均值终止点    --->   平均值起始点肯定早于有效数据起始点出现
    flag_num_avg_end = False
    for i in range((len_data - 1), 0, -1):
        # 捕获平均值终止点
        if not flag_num_avg_end:
            if abs(fx[i]) >= fx_ref:
                data_avg['num_end'] = i
                flag_num_avg_end = True
        # 捕获有效数据终止点
        else:

            if abs(fx[i]) >= 20:
                data_effect['num_end'] = i
                break
            else:
                continue

    # 求稳定平均值
    data_avg['fx'] = mean(list(fx[data_avg['num_start']:data_avg['num_end']]))
    data_avg['fy'] = mean(list(fy[data_avg['num_start']:data_avg['num_end']]))
    data_avg['fz'] = mean(list(fz[data_avg['num_start']:data_avg['num_end']]))
    # data_avg['f4'] = mean(list(f4[num_avg_start:num_avg_end]))
    # data_avg['f5'] = mean(list(f5[num_avg_start:num_avg_end]))

    t.show()

    return data, data_effect, data_avg
