# coding: utf-8
"""
-------------------------------------------------
   File Name:      cont
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date:           2021-06-29 04:27 PM
-------------------------------------------------
Description : 

    Print info with under format:

"""
from globle_variante import GlobalValue
import psutil


def cont():
    while 1:
        pid_flag=False

        # get pid_stats from GlobalValue
        pid_dict = GlobalValue.get_value()

        # get suspend flag
        for key, values in pid_dict:
            if values is True:
                pid_flag = True
                break

        # suspend process except pid with True value
        if pid_flag:
            # get pids except pid with True value
            pid_list = list(pid_dict.keys())
            pid_list.remove(key)
            for pid in pid_list:
                pause = psutil.Process(pid)
                pause.suspend()

        # resume process
        else:
            try:
                pause.resume()
            except:
                pass

        # kill this process
        if pid_dict == {}:
            break
