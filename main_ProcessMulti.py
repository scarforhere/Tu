# coding: utf-8
"""
-------------------------------------------------
   File Name：     main_ProcessMulti
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date：          2021-05-04 10:13 PM
-------------------------------------------------
Description : 

    Program runs on Multi Process Lines

"""
import multiprocessing
from get_all_files import get_all_files
from time_record import TimeMonitor
from single_process import single_process
import os

g_path = r'E:\Python_Code\Tu\Data'


def main(target_path: str = '', process: int = None):
    if target_path == '':
        path = os.getcwd()
    else:
        path = target_path

    if not process:
        num_pool = 4
    else:
        num_pool = process

    t_total = TimeMonitor('\nTotal Time')

    # TODO: Set Proper Process Number for ProcessingPool!!!
    pool = multiprocessing.Pool(num_pool)

    path_list = get_all_files(path)

    for path in path_list:
        # 异步执行程序
        pool.apply_async(func=single_process, args=(path,))

    pool.close()
    pool.join()

    t_total.show()

    print('------------------------------')
    print('Finished!'.center(30))
    print('------------------------------')


if __name__ == '__main__':

    path = input("\nDefault: Path = Current Folder (Press Enter)\n"
                 "Set Path of Target Folder:\n")

    try:
        num = int(input("Default: Process Quantity = 4 (Press Enter)\n"
                        "Set Proper Process Quantity for ProcessingPool:\n"))
    except ValueError:
        num = None

    main(path, num)
