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
import numpy as np
from readline_format import readline_format03, readline_format04, readline_format05
from time_record import TimeMonitor
from data_fix import fix_data, determine_data


def data_convert(file: str):
    """
    Sort data from TXT and transfer data, data_effect, data_avg in Dict type

    :param file: Path of file
    :return: data, data_effect, data_avg
    """
    try:
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
            if file.rfind('V2 T2mm 38 0,1 M1.txt') == -1:
                if data_itemnum == 6:
                    data_list = readline_format04(data_line)
                elif data_itemnum == 4:
                    data_list = readline_format03(data_line)
                else:
                    print(f"Error: Data Item Number Wrong\n"
                          f"Error File: {file}")
                    return
            else:
                data_list = readline_format05(data_line)

            if data_list is None:
                break

            # create DataDict for DataFrame
            s.append(data_list[0])
            fx.append(data_list[1])
            fy.append(data_list[2])
            fz.append(data_list[3])
            # f4.append(data_list[4])
            # f5.append(data_list[5])

        s_array = array(s)
        fx_array = array(fx)
        fy_array = array(fy)
        fz_array = array(fz)

        # determine data need to be fixed or not
        fix_stat, calibration_file = determine_data(file)
        if fix_stat:
            fx, fy, fz = fix_data(s_array, fx_array, fy_array, fz_array, calibration_file)
            # print(f'{file} is fixed')

        # Calculate mu = Fx / Fz
        mu = fx_array / fz_array

        # init DataDict for data transfer to other methode
        data_avg = {}
        # init Dict to save info of effective data
        data_effect = {}

        # init Dict to save info of average and effective data
        fx_avg_ref = max(fx) * 0.8
        fx_eff_ref = max(fx) * 0.1

        # --> effective start point must be later than average start point
        flag_num_start = False
        for i in range(len_data):
            # catch index of effective start point
            if not flag_num_start:
                if abs(fx[i]) >= fx_eff_ref:
                    data_effect['num_start'] = i
                    flag_num_start = True
            # catch index of average start point
            else:
                if abs(fx[i]) >= fx_avg_ref:
                    data_avg['num_start'] = i
                    break
                else:
                    continue

        # --> average start point must be earlier than effective start point
        flag_num_start = False
        for i in range((len_data - 1), 0, -1):
            # catch index of average start point
            if not flag_num_start:
                if abs(fx[i]) >= fx_eff_ref:
                    data_effect['num_end'] = i
                    flag_num_start = True
            # catch index of effective end point
            else:

                if abs(fx[i]) >= fx_avg_ref:
                    data_avg['num_end'] = i
                    break
                else:
                    continue

        data = {'s': s,
                'fx': fx,
                'fy': fy,
                'fz': fz,
                'mu': mu,
                # 'f4': f4,
                # 'f5': f5
                }

        # get max and min value of Fx, Fy and Fz in Effective Range
        data_effect['fx_max'] = max(fx[data_avg['num_start']:data_avg['num_end']])
        data_effect['fx_min'] = min(fx[data_avg['num_start']:data_avg['num_end']])
        data_effect['fy_max'] = max(fy[data_avg['num_start']:data_avg['num_end']])
        data_effect['fy_min'] = min(fy[data_avg['num_start']:data_avg['num_end']])
        data_effect['fz_max'] = max(fz[data_avg['num_start']:data_avg['num_end']])
        data_effect['fz_min'] = min(fz[data_avg['num_start']:data_avg['num_end']])

        # calculate average value for each force
        data_avg['fx_avg'] = mean(list(fx[data_avg['num_start']:data_avg['num_end']]))
        data_avg['fy_avg'] = mean(list(fy[data_avg['num_start']:data_avg['num_end']]))
        data_avg['fz_avg'] = mean(list(fz[data_avg['num_start']:data_avg['num_end']]))
        # data_avg['f4'] = mean(list(f4[num_avg_start:num_avg_end]))
        # data_avg['f5'] = mean(list(f5[num_avg_start:num_avg_end]))

        # calculate median value for each force
        data_median = dict()
        data_median['fx_median'] = median(list(fx[data_avg['num_start']:data_avg['num_end']]))
        data_median['fy_median'] = median(list(fy[data_avg['num_start']:data_avg['num_end']]))
        data_median['fz_median'] = median(list(fz[data_avg['num_start']:data_avg['num_end']]))
        # data_median['f4_median'] = mean(list(f4[num_avg_start:num_avg_end]))
        # data_median['f5_median'] = mean(list(f5[num_avg_start:num_avg_end]))

        # Calculate Sum F for every time point
        fsum_array = (fx_array ** 2 + fy_array ** 2 + fz_array ** 2) ** 0.5
        data_sum = {
            'fsum': fsum_array[data_avg['num_start']:data_avg['num_end']],
            'fsum_max': fsum_array[data_avg['num_start']:data_avg['num_end']].max(),
            'fsum_min': fsum_array[data_avg['num_start']:data_avg['num_end']].min(),
            'fsum_avg': mean(fsum_array[data_avg['num_start']:data_avg['num_end']])
        }

        # Standard Deviation 99% --> 6sigma
        amplitude_99 = {
            '6sigma_fx': np.std(fx_array[data_avg['num_start']:data_avg['num_end']], ddof=1) * 6,
            '6sigma_fy': np.std(fy_array[data_avg['num_start']:data_avg['num_end']], ddof=1) * 6,
            '6sigma_fz': np.std(fz_array[data_avg['num_start']:data_avg['num_end']], ddof=1) * 6,
            '6sigma_fsum': np.std(data_sum['fsum'], ddof=1) * 3,
        }

        # Calculate mu_avg
        mu_avg = mean(list(mu[data_avg['num_start']:data_avg['num_end']]))

        return data, data_effect, data_avg, data_median, data_sum, amplitude_99, len_data, mu_avg, t.trans()

    except Exception as e_info:
        print('Data Convert Failed!!!')
        print(f'\tFailed Path: {file}')
        print(f'\t{e_info}')
