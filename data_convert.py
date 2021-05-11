# coding: utf-8
"""
-------------------------------------------------
   File Name：     data_convert.py
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date：          2021-05-01 10:30 AM
-------------------------------------------------
Description :

    Sort data from TXT and transfer data, data_effect, data_avg in Dict type

"""
from numpy import *
from readline_format import readline_format03, readline_format04
from time_record import TimeMonitor


def data_convert(file: str):
    """
    Sort data from TXT and transfer data, data_effect, data_avg in Dict type

    :param file: Path of file
    :return: data, data_effect, data_avg
    """
    t = TimeMonitor('\tData Convert Time', 25)

    # read total TXT file and count line's quantity
    with open(file, 'r') as f:
        data_total = f.readlines()

        # how many item in a data_line
        f.seek(0)
        data_firstline = f.readline()
        data_itemnum = data_firstline.count(',')

    len_data = len(data_total)

    # used by ProcessSingle
    # print(f"\tLine: {len_data}")

    # init data space
    s = []
    fx = []
    fy = []
    fz = []
    # f4 = []
    # f5 = []

    # transfer line's data to readable string
    for data_line in data_total:
        if data_itemnum == 6:
            data_list = readline_format04(data_line)
        elif data_itemnum == 4:
            data_list = readline_format03(data_line)
        else:
            print(f"Error: Data Item Number Wrong\n"
                  f"Error File: {file}")
            return

        if data_list is None:
            break

        # create DataDict for DataFrame
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

    # init DataDict for data transfer to other methode
    data_avg = {}
    # init Dict to save info of effective data
    data_effect = {}

    # init Dict to save info of average data
    fx_ref = max(fx) * 0.8

    # --> effective start point must be later than average start point
    flag_num_start = False
    for i in range(len_data):
        # catch index of effective start point
        if not flag_num_start:
            if abs(fx[i]) >= 20:
                data_effect['num_start'] = i
                flag_num_start = True
        # catch index of average start point
        else:
            if abs(fx[i]) >= fx_ref:
                data_avg['num_start'] = i
                break
            else:
                continue

    # --> average start point must be earlier than effective start point
    flag_num_start = False
    for i in range((len_data - 1), 0, -1):
        # catch index of average start point
        if not flag_num_start:
            if abs(fx[i]) >= 20:
                data_effect['num_end'] = i
                flag_num_start = True
        # catch index of effective end point
        else:

            if abs(fx[i]) >= fx_ref:
                data_avg['num_end'] = i
                break
            else:
                continue

    # calculate average value for each force
    data_avg['fx'] = mean(list(fx[data_avg['num_start']:data_avg['num_end']]))
    data_avg['fy'] = mean(list(fy[data_avg['num_start']:data_avg['num_end']]))
    data_avg['fz'] = mean(list(fz[data_avg['num_start']:data_avg['num_end']]))
    # data_avg['f4'] = mean(list(f4[num_avg_start:num_avg_end]))
    # data_avg['f5'] = mean(list(f5[num_avg_start:num_avg_end]))

    return data, data_effect, data_avg, len_data, t.trans()
