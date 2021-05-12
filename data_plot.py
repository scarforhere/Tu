# coding: utf-8
"""
-------------------------------------------------
   File Name：     get_count.py
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date：          2021-05-01 10:14 AM
-------------------------------------------------
Description :

    Piot the data from file

"""
import matplotlib.pyplot as plt
import os
from time_record import TimeMonitor


def data_plot(path: str, data: dict, data_effect: dict, data_avg: dict):
    """
    Piot the data from file

    :param data:
    :param data_effect:
    :param data_avg:
    :param path:Path of the file
    """
    t = TimeMonitor('\tPlot Time', 25)

    # TODO: Set Size of PNG
    plt.figure(figsize=(18, 6))

    s = data['s']
    fx = data['fx']
    fy = data['fy']
    fz = data['fz']

    num_start = data_effect['num_start']
    num_end = data_effect['num_end']

    fx_max_effect = data_effect['fx_max']
    fx_min_effect = data_effect['fx_min']
    fy_max_effect = data_effect['fy_max']
    fy_min_effect = data_effect['fy_min']
    fz_max_effect = data_effect['fz_max']
    fz_min_effect = data_effect['fz_min']

    fx_avg = data_avg['fx']
    fy_avg = data_avg['fy']
    fz_avg = data_avg['fz']

    l_f1, = plt.plot(s, fx, label='Fx')
    l_f2, = plt.plot(s, fy, label='Fy')
    l_f3, = plt.plot(s, fz, label='Fz')

    # l_f4, = plt.plot(x, f4, label='f4')
    # l_f5, = plt.plot(x, f5, label='f5')

    # TODO Set Effective Horizontal Axis Range
    plt.xlim((s[num_start] - 0.1, s[num_end] + 0.1))  # plot all range
    # plt.xlim((x[0], x[len_data-1]))               # plot effective range

    plt.xlabel('Time (s)')
    plt.ylabel('Force (N)')

    plt.title(f"{os.path.basename(path)}".replace('.txt', ''))

    lg = plt.legend(handles=[l_f1, l_f2, l_f3],
                    labels=[
                        'Fx  -->  Fx_avg=' + '{0:6.2f}N'.format(fx_avg).rjust(8) +
                        '  Fx_max=' + '{0:6.2f}N'.format(fx_max_effect).rjust(8) +
                        '  Fx_min=' + '{0:6.2f}N'.format(fx_min_effect).rjust(8),

                        'Fy  -->  Fy_avg=' + '{0:6.2f}N'.format(fy_avg).rjust(8) +
                        '  Fy_max=' + '{0:6.2f}N'.format(fy_max_effect).rjust(8) +
                        '  Fy_min=' + '{0:6.2f}N'.format(fy_min_effect).rjust(8),

                        'Fz  -->  Fz_avg=' + '{0:6.2f}N'.format(fz_avg).rjust(8) +
                        '  Fz_max=' + '{0:6.2f}N'.format(fz_max_effect).rjust(8) +
                        '  Fz_min=' + '{0:6.2f}N'.format(fz_min_effect).rjust(8)],
                    loc='best',  # TODO: Set Location of Legend
                    )

    # lg.get_frame().set_facecolor('none')
    # lg.get_frame().set_linewidth(0.0)

    plt.savefig(f"{path.replace('.txt', '')}.png")
    # plt.show()

    return t.trans()
