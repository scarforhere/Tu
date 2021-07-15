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
from summary import Summary


def single_process(path):
    """
    Operation for every TXT file

    :param path: Path of target TXT file
    """
    try:
        print(f'Processing: {path}')
        info = InfoPrint(path)
        data, data_effect, data_avg, data_median, data_sum, amplitude_99, info.line, mu_avg, info.t_convert = \
            data_convert(path)
        info.t_plot = data_plot(path, data, data_effect, data_avg)
        info.t_excel = excel_write(path, data, data_effect)
        Summary(path, data_effect, data_avg, data_median, data_sum, amplitude_99, mu_avg)

        info.show()

    except Exception as e:
        print(f'Fail: {path}\n\t{e}')


if __name__ == '__main__':
    # _path = list()
    # _path.append(r'E:\Python_Code\Tu\Data\Menze\T0.5 V161-168\V165 T0.5mm 0.05 75 M1.txt')
    # _path.append(r'E:\Python_Code\Tu\Data\Menze\T0.5 V161-168\V165 T0.5mm 0.05 75 M1.txt')
    #
    # for path_item in _path:
    #     single_process(path_item)
    #
    # Summary.to_excel()

    _path=r'E:\Python_Code\Tu\Data\Trocken\T1,8mm\0,1 38\V18 T1,8mm 38 0,1 M1.txt'
    single_process(_path)