# coding: utf-8
"""
-------------------------------------------------
   File Name:      globle_variante
   Author :        Scar
   E-mail :        scarforhere@gmail.com
   Date:           2021-06-29 11:01 AM
-------------------------------------------------
Description : 

        #先必须在主模块初始化（只在Main模块需要一次即可）
        GlobalValue()

        #定义跨模块全局变量
        GlobalValue.set_value('CODE','UTF-8')

        # 读取全局变量
        code = GlobalValue.get_value('CODE')

"""
_global_dict = {}


class GlobalValue:
    def __init__(self):
        global _global_dict

    @staticmethod
    def set_value(key, value):
        """ 定义一个全局变量 """
        _global_dict[key] = value

    @staticmethod
    def get_value(defValue=None):
        """ 获得一个全局变量,不存在则返回默认值 """

        try:
            return _global_dict
        except KeyError:
            return defValue

    @staticmethod
    def del_value(key):
        _global_dict.pop(key)

# GlobalValue()
# GlobalValue.set_value(1111, 10)
# GlobalValue.set_value(2222, 20)
# GlobalValue.set_value(3333, 30)
# print(GlobalValue.get_value())



