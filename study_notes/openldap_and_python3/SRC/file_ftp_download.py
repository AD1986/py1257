#! /usr/bin/env python3
# coding:utf-8

"""
作者：杨超
日期：2018-06-25
* 文件名称：file_ftp_download.py
* 功能说明：远程连接到目标ftp服务器，并下载特定文件
* 生成文件：
"""
import ftplib


def ftp_download(ftp_ip, ftp_username, ftp_password, ftp_local_path, ftp_remote_path, ftp_remote_name):
    ftp = ftplib.FTP(ftp_ip)
    ftp.login(ftp_username, ftp_password)
    ftp.cwd(ftp_remote_path)
    bufsize = 1024
    file_handler = open(ftp_local_path, 'wb')
    ftp.retrbinary('RETR ' + ftp_remote_name, file_handler.write, bufsize)
    file_handler.close()
    ftp.quit()
    ftp.close()
