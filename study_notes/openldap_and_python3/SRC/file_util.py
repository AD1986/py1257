#! /usr/bin/env python3
# coding:utf-8

"""
原始作者：
@author: www.crazyant.net
@version: 2014-12-5

作者：杨超
日期：2018-06-08
* 文件名称：file_util.py
* 功能说明：用list或dict字段模式读取文件
"""


class FileUtil(object):
    @staticmethod
    def read_file_data(filepath):
        """
        根据路径按行读取文件, 参数filepath：文件的绝对路径
        @param filepath: 读取文件的路径
        @return: 按,分割后的每行的数据列表
        """
        f_in = open(filepath, 'r', encoding='utf-8')
        for line in f_in:
            try:
                line = line[:-1]
                if not line:
                    continue
            except:
                continue

            try:
                fields = line.split(",")
            except:
                continue
            yield fields
        f_in.close()

    @staticmethod
    def transform_list_to_dict(para_list):
        """
        把['a', 'b']转换成{'a':0, 'b':1}的形式
        @param para_list: 列表，里面是每个列对应的字段名
        @return: 字典，里面是字段名和位置的映射
        """
        res_dict = {}
        idx = 0
        while idx < len(para_list):
            res_dict[str(para_list[idx]).strip()] = idx
            idx += 1
        return res_dict

    @staticmethod
    def map_fields_list_schema(fields, list_schema):
        """
        根据字段的模式，返回模式和数据值的对应值；例如 fields为['a','b','c'],schema为{'name', 'age'}，那么就返回{'name':'a','age':'b'}
        @param fields: 包含有数据的数组，一般是通过对一个Line String通过按照\t分割得到
        @param list_schema: 列名称的列表list
        @return: 词典，key是字段名称，value是字段值
        """
        dict_schema = FileUtil.transform_list_to_dict(list_schema)
        return FileUtil.map_fields_dict_schema(fields, dict_schema)

    @staticmethod
    def map_fields_dict_schema(fields, dict_schema):
        """
        根据字段的模式，返回模式和数据值的对应值；例如 fields为['a','b','c'],schema为{'name':0, 'age':1}，那么就返回{'name':'a','age':'b'}
        @param fields: 包含有数据的数组，一般是通过对一个Line String通过按照\t分割得到
        @param dict_schema: 一个词典，key是字段名称，value是字段的位置；
        @return: 词典，key是字段名称，value是字段值
        """
        pdict = {}
        for fstr, findex in dict_schema.items():
            pdict[fstr] = str(fields[int(findex)])
        return pdict
