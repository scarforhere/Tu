# coding: utf-8
"""
-------------------------------------------------
   Project :       Tu
   File Name :     summary
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date：          2021-05-13 11:24 AM
-------------------------------------------------
Description : 

    Summary data from all sub processes
    Write in Parameter-1.xlsx

"""
import json
import os
import re
import pandas as pd
from get_all_files import get_all_files

# TODO: Set Path For Result_Summary.xlsx
g_set_excel_path = ''.join([os.getcwd(), r'\Data'])


class Summary(object):
    list_summary = []
    global g_set_excel_path

    # Create folder for temp files
    g_set_temp_path = ''.join([g_set_excel_path, r'\Temp_Summary'])
    try:
        os.mkdir(g_set_temp_path)
    except FileExistsError:
        pass

    target_excel = ''.join([g_set_excel_path, r'\Result_Summary.xlsx'])

    # One instance exist in total program
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        return instance

    def __init__(self, path, data_effect, data_avg, data_median, data_sum, amplitude_99, mu_avg):
        self.dict_summary = {'path': path,
                             'Spanflächen_tiefe': None,
                             'Spanflächen_länge': None,
                             'h': None,
                             'vc': None,
                             'Versuch': None,
                             'KSS': None,
                             'M': None,
                             'Fx': data_avg['fx_avg'],
                             'Fx_median': data_median['fx_median'],
                             'Fx_max': data_effect['fx_max'],
                             'Fx_min': data_effect['fx_min'],
                             'Fy': data_avg['fy_avg'],
                             'Fy_median': data_median['fy_median'],
                             'Fy_max': data_effect['fy_max'],
                             'Fy_min': data_effect['fy_min'],
                             'Fz': data_avg['fz_avg'],
                             'Fz_median': data_median['fz_median'],
                             'Fz_max': data_effect['fz_max'],
                             'Fz_min': data_effect['fz_min'],
                             'Schnittkraft': data_sum['fsum_avg'],
                             'Schnittkraft_max': data_sum['fsum_max'],
                             'Schnittkraft_min': data_sum['fsum_min'],
                             'Amplitude_Fx': amplitude_99['6sigma_fx'],
                             'Amplitude_Fy': amplitude_99['6sigma_fy'],
                             'Amplitude_Fz': amplitude_99['6sigma_fz'],
                             'Amplitude_Schnittkraft': amplitude_99['6sigma_fsum'],
                             'mu_avg': mu_avg
                             }

        self.__set_value()
        self.__json_write()

    # Set value from name of txt files
    def __set_value(self):
        path = os.path.basename(self.dict_summary['path']).replace(',', '.')
        (path, _) = os.path.splitext(path)

        result = re.findall('\S+', path)
        sub_result = re.findall('([A-Z])(\S+)mm', result[1])
        self.dict_summary['Spanflächen_tiefe'] = str(sub_result[0][0])
        self.dict_summary['Spanflächen_länge'] = float(sub_result[0][1])

        # correct the mix of 'h' anf 'vc'
        if float(result[2]) > 10.0:
            self.dict_summary['h'] = float(result[3])
            self.dict_summary['vc'] = float(result[2])
        else:
            self.dict_summary['h'] = float(result[2])
            self.dict_summary['vc'] = float(result[3])

        self.dict_summary['Versuch'] = float(result[0][1:])
        if sub_result[0] == 'N':
            self.dict_summary['KSS'] = '1'
        else:
            self.dict_summary['KSS'] = '0'
        self.dict_summary['M'] = float(result[4][1])

    # Write data in EXCEL
    @classmethod
    def to_excel(cls):
        cls.list_summary = cls.__json_read(cls)

        # Init dict{} for DataFrame
        excel_dict = {'Spanflächen_tiefe': [],
                      'Spanflächen_länge': [],
                      'h': [],
                      'vc': [],
                      'Versuch': [],
                      'KSS': [],
                      'M': [],
                      'Fx': [],
                      'Fx_median': [],
                      'Fx_max': [],
                      'Fx_min': [],
                      'Fy': [],
                      'Fy_median': [],
                      'Fy_max': [],
                      'Fy_min': [],
                      'Fz': [],
                      'Fz_median': [],
                      'Fz_max': [],
                      'Fz_min': [],
                      'Schnittkraft': [],
                      'Schnittkraft_max': [],
                      'Schnittkraft_min': [],
                      'Amplitude_Fx': [],
                      'Amplitude_Fy': [],
                      'Amplitude_Fz': [],
                      'Amplitude_Schnittkraft': [],
                      'mu_avg': []
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
        writer = pd.ExcelWriter(cls.target_excel, engine='xlsxwriter')

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
        mu_format = workbook.add_format({'align': 'center', 'num_format': '#,##0.0000'})
        worksheet.set_column("A:B", 21, rank_format)
        worksheet.set_column("C:C", 8, rank_format)
        worksheet.set_column("D:D", 7, rank_format)
        worksheet.set_column("E:E", 11, rank_format)
        worksheet.set_column("F:F", 7, rank_format)
        worksheet.set_column("G:G", 5, rank_format)
        worksheet.set_column("H:S", 12, num_format)
        worksheet.set_column("T:T", 15, num_format)
        worksheet.set_column("U:V", 19, num_format)
        worksheet.set_column("W:Y", 17, num_format)
        worksheet.set_column("Z:Z", 25, num_format)
        worksheet.set_column("AA:AA", 12, mu_format)

        # # Can not use with Table_Style  in the same time
        # worksheet.autofilter(0, 0, max_row, max_col - 1)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

    # Write in if txt does not exist
    def __check_init_txt(self):
        if not os.path.exists(self.target_txt):
            with open(self.target_txt, 'w') as f:
                f.write(json.dumps([]))

    # Write temp files for storage of data
    def __json_write(self):
        self.target_txt = ''.join([self.g_set_temp_path, '\\', os.path.split(self.dict_summary['path'])[1]])
        with open(self.target_txt, 'w') as f:
            f.write(json.dumps(self.dict_summary))

    # Read all datas form temp folder
    def __json_read(self):
        data = []
        path_list = get_all_files(self.g_set_temp_path)
        for path_item in path_list:
            path_item = ''.join([self.g_set_temp_path, '\\', os.path.split(path_item)[1]])
            with open(path_item, "r") as f:
                data.append(json.loads(f.read()))
            os.remove(path_item)
        return data


if __name__ == '__main__':
    _data_sum = {'fsum': 1, 'fsum_max': 2, 'fsum_min': 3, 'fsum_avg': 4}

    _data_effect = {'fx_max': 11, 'fx_min': 12, 'fy_max': 13, 'fy_min': 14, 'fz_max': 15, 'fz_min': 16}
    _data_avg = {'fx_avg': 21, 'fy_avg': 22, 'fz_avg': 23}
    _amplitude_99 = {'6sigma_fx': 217329.15937076055, '6sigma_fy': 10734.24652204412, '6sigma_fz': 572699.0424957989,
                     '6sigma_fsum': 36744.06981425831}

    # g_set_temp_path = r'E:\Python_Code\Tu\Data'
    _data_median = {
        'fx_median': 111,
        'fy_median': 111,
        'fz_median': 111,
    }
    _mu_avg = 0

    sum1 = Summary(r'E:\Python_Code\Tu_Data\Token\T1,4mm\V49 T1,4mm 38 0,05 M1.txt', _data_effect, _data_avg,
                   _data_median, _data_sum, _amplitude_99, _mu_avg)

    sum2 = Summary(r'E:\Python_Code\Tu_Data\Trocken\T1,4mm\V49 T1,4mm 38 0,05 M2.txt', _data_effect, _data_avg,
                   _data_median, _data_sum, _amplitude_99, _mu_avg)

    Summary.to_excel()
