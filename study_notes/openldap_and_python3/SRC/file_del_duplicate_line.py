#! /usr/bin/env python3
# coding:utf-8

"""
作者：杨超
日期：2018-06-11
* 文件名称：file_del_dup_line.py
* 功能说明：删除文件中重复的行
"""
import os


def file_del_dup_line(path):
    line_dict = {}

    with open(path, 'r', encoding='utf-8') as f_in:
        for line in f_in:
            if line not in line_dict:
                line_dict[line] = ""

    os.remove(path)

    with open(path, 'a', encoding='utf-8') as f_out:
        for key in line_dict:
            f_out.write(key)
