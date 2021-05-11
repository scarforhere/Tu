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
import re


def readline_format01(data_line):
    """
    Convert data of single line from String to readable Tuple

    :param data_line: Fata of single line
    :return: None(illegal data) or List of data
    """
    # replace ',' with '.'  Fucking Silly German Format
    data_line = data_line.replace(",", ".")

    # split sting with '\t' and convert it to List of substring
    data_list = [0 for _ in range(6)]
    lst = data_line.partition('\t')
    data_list[0] = lst[0]
    for i in range(2, 7):
        lst = lst[2].partition('\t')
        data_list[i - 1] = lst[0]

    # remove '"' in list of string     "string"-->string
    # convert List of substring to List of float number
    len_data_list = len(data_list)
    data_value_list = [0 for _ in range(len_data_list)]
    for i in range(0, len_data_list):
        # regardless of '“'
        if get_count(data_list[i], '"') == 0:
            return None
        else:
            lst = data_list[i].partition('"')
            lst = lst[2].partition('"')
            data_value = lst[0]

        # solve situation with 2 '.'
        if get_count(data_value, ".") == 2:
            data_value = data_value.rpartition('.')
            data_value = ''.join([data_value[0], data_value[2]])

        # convert List of substring to List of float number
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
        data_list[i] = float(data_list[i])

    return data_list


def readline_format03(data_line):
    """
    Convert data of single line from String to readable Tuple\n
    Target num = 4
    Use Regular Expression

    :param data_line: Fata of single line
    :return: None(illegal data) or List of data
    """
    if data_line == '\n':
        return
    # replace ',' with '.'  Fucking Silly German Format
    data_line = data_line.replace(",", ".")

    # Regular Expression Rule
    re_g = re.compile('(.*?)\t(.*?)\t(.*?)\t(.*?)\n')
    data_line = re_g.search(data_line)

    # convert List of substring to List of float number
    data_list = []
    for i in range(1, 5):
        data_item = float(data_line.group(i))
        data_list.append(data_item)

    return data_list


def readline_format04(data_line):
    """
    Convert data of single line from String to readable Tuple\n
    Target num = 6
    Use Regular Expression

    :param data_line: Fata of single line
    :return: None(illegal data) or List of data
    """
    if data_line == '\n':
        return
    # replace ',' with '.'  Fucking Silly German Format
    data_line = data_line.replace(",", ".")

    # Regular Expression Rule
    re_g = re.compile('(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\n')
    data_line = re_g.search(data_line)

    # convert List of substring to List of float number
    data_list = []
    for i in range(1, 5):
        data_item = float(data_line.group(i))
        data_list.append(data_item)

    return data_list
