# coding: utf-8
"""
-------------------------------------------------
   File Name:      summary_csv
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date:           2021-07-14 08:29 AM
-------------------------------------------------
Description : 

    Summary datas from .CSV file

"""
import pandas as pd
import numpy as np
import json
import os
import re

# _path_folder = r'E:\Python_Code\Tu\CSV'
summary_txt = r'Summary_CSV.xlsx'


def main():
    path_folder = os.getcwd()
    # path_folder=_path_folder
    print(f'Target Folder: {path_folder}')
    print()

    os.chdir(path_folder)

    # TODO: Get All File Path
    path_list = get_all_csv(path_folder)

    for path in path_list:
        print(f'\tProcessing: {path}')
        # Read .csv File
        df = pd.read_csv(path)

        # Calculate
        data = df['Length'].tolist()
        for i in range(3):
            data.remove(max(data))
            data.remove(min(data))
        data = np.array(data)
        avg = np.mean(data)
        std = np.std(data)

        # Add to .txt
        SummaryCSV(path_folder, path, avg, std)

    SummaryCSV.to_excel(path_folder)

    print()
    print('-----------------------------------')
    print('-----                         -----')
    print('-----      Summary Done       -----')
    print('-----                         -----')
    print('-----------------------------------')
    print('                                                      :) from Scar')
    print()
    print()
    input('----- Press Enter To Continue -----')


class SummaryCSV(object):
    global summary_txt
    list_summary = []

    # One instance exist in total program
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        return instance

    def __init__(self, path_folder, path, avg, std):
        self.path_folder = path_folder
        self.dict_summary = {
            'path': path,
            'Name': None,
            'Name-Nr.': None,
            'Spanflächen_tiefe': None,
            'Spanflächen_länge': None,
            'h': None,
            'vc': None,
            'KSS': None,
            'AVG': avg,
            'STD': std
        }
        self.__set_value()
        self.__json_write()

    @classmethod
    def to_excel(cls, path_folder):
        cls.list_summary = cls.__json_read(path_folder)
        excel_dict = {
            'Name': [],
            'Name-Nr.': [],
            'Spanflächen_tiefe': [],
            'Spanflächen_länge': [],
            'h': [],
            'vc': [],
            'KSS': [],
            'AVG': [],
            'STD': []
        }
        # Append value for DataFrame
        for data_line in cls.list_summary:
            data_line_keys = data_line.keys()
            for key in data_line_keys:
                if key != 'path':
                    excel_dict[key].append(data_line[key])

        # Create Dataframe
        df = pd.DataFrame(excel_dict)

        # Create Writer with 'xlsxwriter' engine
        target_excel = ''.join([path_folder, '\\', summary_txt])
        writer = pd.ExcelWriter(target_excel, engine='xlsxwriter')

        # Write DataFrame back to Writer
        df.to_excel(writer, startrow=1, header=False, index=False, sheet_name='tabelle')

        (max_row, max_col) = df.shape

        workbook = writer.book
        worksheet = writer.sheets['tabelle']

        # Add Table Style
        column_settings = [{'header': column} for column in df.columns]
        worksheet.add_table(0, 0, max_row, max_col - 1, {'style': 'Table Style Medium 4', 'columns': column_settings})

        # Set the column width and format.
        rank_format = workbook.add_format({'align': 'center'})
        num_format = workbook.add_format({'align': 'center', 'num_format': '#,##0.00'})
        # mu_format = workbook.add_format({'align': 'center', 'num_format': '#,##0.0000'})
        worksheet.set_column("A:A", 10, rank_format)
        worksheet.set_column("B:B", 14, rank_format)
        worksheet.set_column("C:D", 24, rank_format)
        worksheet.set_column("E:G", 8, rank_format)
        worksheet.set_column("H:I", 16, num_format)

        # # Can not use with Table_Style  in the same time
        # worksheet.autofilter(0, 0, max_row, max_col - 1)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

    def __set_value(self):
        path = os.path.basename(self.dict_summary['path']).replace(',', '.')
        (path, _) = os.path.splitext(path)

        result = re.findall('\S+', path)
        sub_result = re.findall('([A-Z])(\S+)mm', result[1])
        sub_result_w = re.findall('([a-z])([0-9]+)', result[0])
        self.dict_summary['Spanflächen_tiefe'] = str(sub_result[0][0])
        self.dict_summary['Spanflächen_länge'] = float(sub_result[0][1])

        # correct the mix of 'h' anf 'vc'
        if float(result[2]) > 10.0:
            self.dict_summary['h'] = float(result[3])
            self.dict_summary['vc'] = float(result[2])
        else:
            self.dict_summary['h'] = float(result[2])
            self.dict_summary['vc'] = float(result[3])

        if sub_result[0] == 'N':
            self.dict_summary['KSS'] = '1'
        else:
            self.dict_summary['KSS'] = '0'
        self.dict_summary['Name'] = sub_result_w[0][0]
        self.dict_summary['Name-Nr.'] = float(sub_result_w[0][1])

    # Write temp files for storage of data
    def __json_write(self):
        path_name = os.path.split(self.dict_summary['path'])[1]
        self.target_txt = ''.join([self.path_folder, '\\', os.path.splitext(path_name)[0], '.txt'])
        with open(self.target_txt, 'w') as f:
            f.write(json.dumps(self.dict_summary))

    # Read all datas form temp folder
    @classmethod
    def __json_read(cls, path_folder):
        data = []
        path_list = get_all_files(path_folder)
        for path_item in path_list:
            path_item = ''.join([path_folder, '\\', os.path.split(path_item)[1]])
            with open(path_item, "r") as f:
                data.append(json.loads(f.read()))
            os.remove(path_item)
        return data


def get_all_files(path):
    """
    Get all file path in target folder

    :param path: Path of target folder
    :return: List of all target .TXT
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


def get_all_csv(path):
    """
    Get all file path in target folder

    :param path: Path of target folder
    :return: List of all target .CSV
    """
    os.chdir(path)

    lst = []

    file_list = os.walk(path)

    for dirpath, dirname, filename in file_list:
        for filename_item in filename:
            if filename_item.endswith(".csv"):
                path_full = "".join([dirpath, '\\', filename_item])
                lst.append(path_full)
            else:
                continue
    return lst


if __name__ == '__main__':
    main()
