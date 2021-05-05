# coding: utf-8
"""
-------------------------------------------------
   File Name：     get_count.py
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date：          2021-05-01 10:14 AM
-------------------------------------------------
Description :

    Convert data of single line from String to readable Tuple

"""
from get_count import get_count


def readline_format01(data_line):
    """
    Convert data of single line from String to readable Tuple

    :param data_line: Fata of single line
    :return: None(illegal data) or List of data
    """
    # 傻逼德语格式换成英语格式
    data_line = data_line.replace(",", ".")

    # 拆分string转化为string列表
    data_list = [0 for _ in range(6)]
    lst = data_line.partition('\t')
    data_list[0] = lst[0]
    for i in range(2, 7):
        lst = lst[2].partition('\t')
        data_list[i - 1] = lst[0]

    # 去除string列表内修饰符'"'     "string"-->string
    # 将string列表转化为float列表
    len_data_list = len(data_list)
    data_value_list = [0 for _ in range(len_data_list)]
    for i in range(0, len_data_list):
        # 解决狗屁科学计数法没有'"'问题
        if get_count(data_list[i], '"') == 0:
            return None
        else:
            lst = data_list[i].partition('"')
            lst = lst[2].partition('"')
            data_value = lst[0]

        # 去除数据中有两个逗号的情况
        if get_count(data_value, ".") == 2:
            data_value = data_value.rpartition('.')
            data_value = ''.join([data_value[0], data_value[2]])

        # 将string列表转化为float列表
        data_value_list[i] = eval(data_value)
    return data_value_list


def readline_format02(data_line):
    """
    Convert data of single line from String to readable Tuple

    :param data_line: Fata of single line
    :return: None(illegal data) or List of data
    """
    data_line = data_line.replace('\n', '')
    # replace ',' with '.'  Fucking Silly German Format
    data_line = data_line.replace(",", ".")

    # split sting with '\t' and convert it to List of substring
    data_list = [0 for _ in range(6)]
    lst = data_line.partition('\t')
    data_list[0] = lst[0]
    for i in range(2, 7):
        lst = lst[2].partition('\t')
        data_list[i - 1] = lst[0]

    # convert List of substring to List of float number
    for i in range(6):
        data_list[i] = eval(data_list[i])

    return data_list
