#! /usr/bin/env python3
# coding:utf-8

"""
作者：杨超
日期：2018-06-11
* 文件名称：file_copy.py
* 功能说明：将 filepath1 复制为 filepath2
* 生成文件：filepath2
"""

import os


def file_copy(file_path1, file_path2):
    # 先判断 file_path2 是否存在
    if os.path.exists(file_path2):
        os.remove(file_path2)

    with open(file_path2, 'a', encoding='utf-8') as f_out:
        with open(file_path1, 'r', encoding='utf-8') as f_in:
            for line in f_in:
                try:
                    line = line[:-1]
                    f_out.writelines(line + "\n")
                    if not line:
                        continue
                except:
                    continue