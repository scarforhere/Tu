# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     get_count.py
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date：          2021-05-01 10:11 AM
-------------------------------------------------
Description :

    Count numbers of ch in s

"""


def get_count(s, ch):
    """
    Count numbers of ch in s

    :param s: string
    :param ch: char
    :return: numbers of char in string
    """
    count = 0
    for item in s:
        if ch.upper() == item or ch.lower() == item:
            count += 1
    return count
