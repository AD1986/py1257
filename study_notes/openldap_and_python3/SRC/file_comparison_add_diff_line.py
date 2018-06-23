#! /usr/bin/env python3
# coding:utf-8

"""
作者：杨超
日期：2018-06-11
* 文件名称：file_comparison_add_diff_line.py
* 功能说明：file_01 与 file_02 对比，取出 file_01 中存在 但 file_02 不存在的条目，存入 file_03
"""

import os


def file_comparison_add_dup_line(file_01, file_02, file_03):
    line_dict = {}

    # 预处理 file_01 ，确保其不含重复条目，预处理之后的文件命名不变
    line_dict_file_01 = {}
    with open(file_01, 'r', encoding='utf-8') as f_in:
        for line in f_in:
            if line not in line_dict_file_01:
                line_dict_file_01[line] = ""
    os.remove(file_01)
    with open(file_01, 'a', encoding='utf-8') as f_out:
        for key in line_dict_file_01:
            f_out.write(key)

    # 剔除 file_02 中的重复条目，之后建立字典
    with open(file_02, 'r', encoding='utf-8') as f_02:
        for line in f_02:
            if line not in line_dict:
                line_dict[line] = ""

    # 先初始化 file_03
    is_exists = os.path.exists(file_03)
    if is_exists:
        os.remove(file_03)

    with open(file_01, 'r', encoding='utf-8') as f_01:
        for line in f_01:
            # 如果 f_01 取出的条目不在字典中，则写入f_03
            if line not in line_dict:
                with open(file_03, 'a', encoding='utf-8') as f_03:
                    f_03.write(line)
