#! /usr/bin/env python3
# coding:utf-8

"""
作者：杨超
日期：2018-06-11
* 文件名称：file_dos2unix.py
* 功能说明：对windows环境下的文件进行格式转换
* 生成文件：filepath + '.dos'
"""


def dos_to_unix(file_path):
    """
    @ src_file为未转换的文件
    @ dst_file为最终的生成文件
    """
    src_file = file_path
    dst_file = file_path + '.dos'
    src_fobj = open(src_file, 'r', encoding='utf-8')
    dst_fobj = open(dst_file, 'w', encoding='utf-8')
    for line in src_fobj:
        dst_fobj.write(line.rstrip('\r\n') + '\n')
    src_fobj.close()
    dst_fobj.close()
