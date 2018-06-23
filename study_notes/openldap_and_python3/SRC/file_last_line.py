#! /usr/bin/env python3
# coding:utf-8

"""
作者：杨超
日期：2018-06-08
* 文件名称：file_last_line.py
* 功能说明：检查文件末行是否为空行，如果是，则删除。
"""
import os


def get_last_line(file_path):
    file_size = os.path.getsize(file_path)
    block_size = 1024
    dat_file = open(file_path, 'r', encoding='utf-8')
    last_line = ""
    if file_size > block_size:
        max_seek_point = (file_size // block_size)
        dat_file.seek((max_seek_point - 1) * block_size)
    elif file_size:
        # max_seek_point = block_size % file_size
        dat_file.seek(0, 0)
    else:
        print("Ooops! The file_size is too small.")
    lines = dat_file.readlines()
    if lines:
        last_line = lines[-1].strip()

    dat_file.close()
    # print(last_line)
    return last_line
