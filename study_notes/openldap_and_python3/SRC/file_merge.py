#! /usr/bin/env python3
# coding:utf-8

"""
作者：杨超
日期：2018-06-11
* 文件名称：file_merge.py
* 功能说明：将两个文件合并为一个新文件
* 生成文件：file_path3
"""
import os


def file_merge(file_path1, file_path2, file_path3):
    """
    file_path1 和 file_path2 为待合并文件
    file_path3 为合并之后的新文件
    先判断是否存在 file_path3 ，若存在，则先删除 file_path3 ，再执行拼接操作
    """
    is_exists = os.path.exists(file_path3)
    if is_exists:
        os.remove(file_path3)

    with open(file_path3, 'a', encoding='utf-8') as f_out:
        with open(file_path1, 'r', encoding='utf-8') as f_in:
            for line in f_in:
                try:
                    line = line[:-1]
                    f_out.writelines(line + "\n")
                    if not line:
                        continue
                except:
                    continue

        with open(file_path2, 'r', encoding='utf-8') as f_in:
            for line in f_in:
                try:
                    line = line[:-1]
                    f_out.writelines(line + "\n")
                    if not line:
                        continue
                except:
                    continue

