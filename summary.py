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

# TODO: Set path for Result_Summary.xlsx
g_set_target_path = ''.join([os.getcwd(), r'\Data'])


class Summary(object):
    list_summary = []
    global g_set_target_path
    target_excel = ''.join([g_set_target_path, r'\Result_Summary.xlsx'])
    target_txt = ''.join([g_set_target_path, r'\Result_Summary.txt'])

    @classmethod
    def pr(cls):
        print(cls.target_excel)
        print(cls.target_txt)

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        return instance

    def __init__(self, path, data_effect, data_avg, data_sum, amplitude_99, mu_avg):
        self.dict_summary = {'path': path,
                             'Spanflächen_tiefe': None,
                             'Spanflächen_länge': None,
                             'h': None,
                             'vc': None,
                             'Versuch': None,
                             'KSS': None,
                             'M': None,
                             'Fx': data_avg['fx_avg'],
                             'Fx_max': data_effect['fx_max'],
                             'Fx_min': data_effect['fx_min'],
                             'Fy': data_avg['fy_avg'],
                             'Fy_max': data_effect['fy_max'],
                             'Fy_min': data_effect['fy_min'],
                             'Fz': data_avg['fz_avg'],
                             'Fz_max': data_effect['fz_max'],
                             'Fz_min': data_effect['fz_min'],
                             'Schnittkraft': data_sum['fsum_avg'],
                             'Schnittkraft_max': data_sum['fsum_max'],
                             'Schnittkraft_min': data_sum['fsum_min'],
                             'Amplitude_Fx': amplitude_99['6sigma_fx'],
                             'Amplitude_Fy': amplitude_99['6sigma_fy'],
                             'Amplitude_Fz': amplitude_99['6sigma_fz'],
                             'Amplitude_Schnittkraft': amplitude_99['6sigma_fsum'],
                             'mu_avg':mu_avg
                             }

        self.__set_value()
        self.__check_init_txt()
        self.__json_write()

    def __set_value(self):
        path = os.path.basename(self.dict_summary['path']).replace(',', '.')
        (path, _) = os.path.splitext(path)
        result = re.findall('\S+', path)
        sub_result = re.findall('([A-Z])(\S+)mm', result[1])

        try:
            self.dict_summary['Spanflächen_tiefe'] = str(sub_result[0][0])
        except:
            path=' '.join([result[0],'XX.Xmm X.XX XX MX'])
            result = re.findall('\S+', path)
            sub_result = re.findall('([A-Z])(\S+)mm', result[1])
            print(sub_result)
            self.dict_summary['Spanflächen_tiefe'] = str(sub_result[0][0])
        finally:
            self.dict_summary['Spanflächen_länge'] = str(sub_result[0][1])
            self.dict_summary['h'] = str(result[3])
            self.dict_summary['vc'] = str(result[2])
            self.dict_summary['Versuch'] = str(result[0][1:])
            if sub_result[0] == 'N':
                self.dict_summary['KSS'] = '1'
            else:
                self.dict_summary['KSS'] = '0'
            self.dict_summary['M'] = str(result[4][1])

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
                      'Fx_max': [],
                      'Fx_min': [],
                      'Fy': [],
                      'Fy_max': [],
                      'Fy_min': [],
                      'Fz': [],
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
        worksheet.set_column("H:P", 12, num_format)
        worksheet.set_column("Q:Q", 15, num_format)
        worksheet.set_column("R:S", 19, num_format)
        worksheet.set_column("T:V", 16, num_format)
        worksheet.set_column("T:V", 17, num_format)
        worksheet.set_column("W:W", 25, num_format)
        worksheet.set_column("X:X", 12, mu_format)

        # # Can not use with Table_Style  in the same time
        # worksheet.autofilter(0, 0, max_row, max_col - 1)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

        os.remove(cls.target_txt)

    def __check_init_txt(self):
        if not os.path.exists(self.target_txt):
            with open(self.target_txt, 'w') as f:
                f.write(json.dumps([]))

    def __json_write(self):
        with open(self.target_txt, "r") as f:
            data = json.loads(f.read())

        data.append(self.dict_summary)

        with open(self.target_txt, 'w') as f:
            f.write(json.dumps(data))

    def __json_read(self):
        with open(self.target_txt, "r") as f:
            data = json.loads(f.read())
        return data


if __name__ == '__main__':
    _data_sum = {'fsum': 1, 'fsum_max': 2, 'fsum_min': 3, 'fsum_avg': 4}

    _data_effect = {'fx_max': 11, 'fx_min': 12, 'fy_max': 13, 'fy_min': 14, 'fz_max': 15, 'fz_min': 16}
    _data_avg = {'fx_avg': 21, 'fy_avg': 22, 'fz_avg': 23}
    amplitude_99 = {'6sigma_fx': 217329.15937076055, '6sigma_fy': 10734.24652204412, '6sigma_fz': 572699.0424957989,
                    '6sigma_fsum': 36744.06981425831}
    g_set_target_path = r'E:\Python_Code\Tu\Data'
    Summary.pr()
    sum1 = Summary(r'E:\Python_Code\Tu_Data\Token\T1,4mm\V49 T1,4mm 38 0,05 M1.txt', _data_effect, _data_avg, _data_sum,
                   amplitude_99)
    sum2 = Summary(r'E:\Python_Code\Tu_Data\Trocken\T1,4mm\V49 T1,4mm 38 0,05 M2.txt', _data_effect, _data_avg,
                   _data_sum, amplitude_99)
    Summary.to_excel()
