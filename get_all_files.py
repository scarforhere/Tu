# coding: utf-8
"""
-------------------------------------------------
   File Name：     get_all_files
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date：          2021-05-04 11:42 PM
-------------------------------------------------
Description : 

    Get all file path

"""
import os


def get_all_files(path):
    """
    Get all file path in target folder

    :param path: Path of target folder
    :return: List of all target files
    """
    os.chdir(path)

    lst = []

    file_list = os.walk(path)

    for dirpath, dirname, filename in file_list:
        for filename_item in filename:
            if filename_item.endswith(".txt"):
                path_full = "".join([dirpath, '\\', filename_item])
                lst.append(path_full)
            else:
                continue
    return lst
