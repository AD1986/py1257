#! /usr/bin/env python3
# coding:utf-8

"""
作者：杨超
日期：2018-06-07
* 文件名称：ldap_main.py
* 功能说明：实现README.vsd中的功能
* 生成文件：
"""

import os
import time
import sys

import file_util
import file_del_duplicate_line
import file_dos2unix
import file_merge
import file_copy
import file_comparison_add_diff_line
import file_comparison_add_dup_line

# 不含日期与后缀的文件名
hr_txt_base_name = 'HR'
hr_tmp_txt_base_name = 'HRtmp'
dp_tmp_txt_base_name = 'DPtmp'
wb_txt_base_name = 'WB'
wb_tmp_txt_base_name = 'WBtmp'
wbdp_tmp_txt_base_name = 'WBDPtmp'
hr_new_txt_base_name = 'HRnew'
dp_new_txt_base_name = 'DPnew'
hr_bak_txt_base_name = 'HRbak'
dp_bak_txt_base_name = 'DPbak'
hr_everyday_txt_base_name = 'HR'
dp_everyday_txt_base_name = 'DP'
add_tree_dp_ldif_name = 'DPadd.ldif'
add_tree_hr_ldif_name = 'HRadd.ldif'
del_tree_dp_ldif_name = 'DPdel.ldif'
del_tree_hr_ldif_name = 'HRdel.ldif'
dp_del_base_txt_name = 'DPdel.txt'
dp_add_base_txt_name = 'DPadd.txt'
hr_del_base_txt_name = 'HRdel.txt'
hr_add_base_txt_name = 'HRadd.txt'
dp_tmp_base_txt_name = 'DPtmp.txt'
hr_tmp_base_txt_name = 'HRtmp.txt'


def time_now():
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return t


def date_now():
    d = time.strftime('%Y%m%d', time.localtime(time.time()))
    return d


def make_dir(path):
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
        print(path+' 创建成功')
        return True
    else:
        print(path + ' 已存在')
        return False


def hr_txt_pretreatment(today):
    # 拼接出 HRyymmdd.txt 的绝对路径
    hr_txt_base_dir = os.path.join(os.getcwd(), hr_txt_base_name + today + '.txt')
    # 拼接出 HRtmpyymmdd.txt 的绝对路径，该文件在yymmddtmp目录中
    hr_tmp_txt_base_dir = os.path.join(os.getcwd(), today + 'tmp', hr_tmp_txt_base_name + today + '.txt')

    is_exists = os.path.exists(hr_txt_base_dir)
    if is_exists:
        list_schema = ["ou", "physicalDeliverOfficeName", "cn", "sn", "description", "st", "title", "l"]
        """
            先判断是否存在 hr_tmp_txt_base_dir ，若存在，则先删除 hr_tmp_txt_base_dir ，再执行写入工作
        """
        is_exists = os.path.exists(hr_tmp_txt_base_dir)
        if is_exists:
            os.remove(hr_tmp_txt_base_dir)

        for fields in file_util.FileUtil.read_file_data(hr_txt_base_dir):
            dict_fields = file_util.FileUtil.map_fields_list_schema(fields, list_schema)
            with open(hr_tmp_txt_base_dir, 'a', encoding='utf-8') as f_tmp:
                f_tmp.writelines(str(dict_fields.get("ou") + ',' + dict_fields.get("physicalDeliverOfficeName") + ',' +
                                     dict_fields.get("cn") + ',' + dict_fields.get("sn") + ',' +
                                     dict_fields.get("description")).replace('\"', '') + "\n")

    else:
        print('i can\'t find HR' + today + ' in the root directory, please check the file status.')
        sys.exit()


def dp_txt_pretreatment(today):
    # 拼接出 HRtmpyymmdd.txt 的绝对路径，该文件在yymmddtmp目录中
    hr_tmp_txt_base_dir = os.path.join(os.getcwd(), today + 'tmp', hr_tmp_txt_base_name + today + '.txt')
    # 拼接出 DPtmpyymmdd.txt 的绝对路径，该文件在yymmddtmp目录中
    dp_tmp_txt_base_dir = os.path.join(os.getcwd(), today + 'tmp', dp_tmp_txt_base_name + today + '.txt')

    list_schema = ["ou", "physicalDeliverOfficeName", "cn", "sn", "description"]
    """
        先判断是否存在 dp_tmp_txt_base_dir ，若存在，则先删除 dp_tmp_txt_base_dir ，再执行写入工作
    """
    is_exists = os.path.exists(dp_tmp_txt_base_dir)
    if is_exists:
        os.remove(dp_tmp_txt_base_dir)

    for fields in file_util.FileUtil.read_file_data(hr_tmp_txt_base_dir):
        dict_fields = file_util.FileUtil.map_fields_list_schema(fields, list_schema)
        with open(dp_tmp_txt_base_dir, 'a', encoding='utf-8') as f_tmp:
            f_tmp.writelines(str(dict_fields.get("ou") + ',' + dict_fields.get("physicalDeliverOfficeName")) + "\n")

    # 删除重复行
    file_del_duplicate_line.file_del_dup_line(dp_tmp_txt_base_dir)


def wb_txt_pretreatment(today):
    # 拼接出 WB.txt 的绝对路径
    wb_txt_base_dir = os.path.join(os.getcwd(), wb_txt_base_name + '.txt')
    # 进行文件的格式转换，转换后的文件名为"原文件名.doc"
    file_dos2unix.dos_to_unix(wb_txt_base_dir)
    # 拼接出转换后的 WB.txt.dos 的绝对路径
    wb_txt_dos_dir = wb_txt_base_dir + '.dos'

    # 拼接出 WBtmpyymmdd.txt 的绝对路径，该文件在yymmddtmp目录中
    wb_tmp_txt_base_dir = os.path.join(os.getcwd(), today + 'tmp', wb_tmp_txt_base_name + today + '.txt')
    list_schema = ["ou", "physicalDeliverOfficeName", "cn", "sn", "description", "st", "title", "l"]
    """
    先判断是否存在 wb_tmp_txt_base_dir ，若存在，则先删除 wb_tmp_txt_base_dir ，再执行有效期判定与写入工作
    """
    is_exists = os.path.exists(wb_tmp_txt_base_dir)
    if is_exists:
        os.remove(wb_tmp_txt_base_dir)

    for fields in file_util.FileUtil.read_file_data(wb_txt_dos_dir):
        dict_fields = file_util.FileUtil.map_fields_list_schema(fields, list_schema)
        if int(dict_fields.get("l")) >= int(today):
            # 将未过期的条目写入 WBtmpyymmdd.txt
            with open(wb_tmp_txt_base_dir, 'a', encoding='utf-8') as f_tmp:
                f_tmp.writelines(str(dict_fields.get("ou") + ',' + dict_fields.get("physicalDeliverOfficeName") + ',' +
                                     dict_fields.get("cn") + ',' + dict_fields.get("sn") + ',' +
                                     dict_fields.get("description")) + "\n")


def wbdp_txt_pretreatment(today):
    # 拼接出 WBtmpyymmdd.txt 的绝对路径，该文件在yymmddtmp目录中
    wb_tmp_txt_base_dir = os.path.join(os.getcwd(), today + 'tmp', wb_tmp_txt_base_name + today + '.txt')

    # 拼接出 WBDPtmpyymmdd.txt 的绝对路径，该文件在yymmddtmp目录中
    wbdp_tmp_txt_base_dir = os.path.join(os.getcwd(), today + 'tmp', wbdp_tmp_txt_base_name + today + '.txt')
    list_schema = ["ou", "physicalDeliverOfficeName", "cn", "sn", "description"]

    """
    先判断是否存在 wbdp_tmp_txt_base_dir ，若存在，则先删除 wbdp_tmp_txt_base_dir ，再执行写入工作
    """
    is_exists = os.path.exists(wbdp_tmp_txt_base_dir)
    if is_exists:
        os.remove(wbdp_tmp_txt_base_dir)

    for fields in file_util.FileUtil.read_file_data(wb_tmp_txt_base_dir):
        dict_fields = file_util.FileUtil.map_fields_list_schema(fields, list_schema)
        with open(wbdp_tmp_txt_base_dir, 'a', encoding='utf-8') as f_tmp:
            f_tmp.writelines(
                str(dict_fields.get("ou") + ',' + dict_fields.get("physicalDeliverOfficeName")) + "\n")

    # 删除重复行
    file_del_duplicate_line.file_del_dup_line(wbdp_tmp_txt_base_dir)


def dp_new_txt_pretreatment(today):
    # 拼接出 DPnew.txt 的绝对路径，该文件在 process 目录中
    dp_new_base_txt_dir = os.path.join(os.getcwd(), 'process', dp_new_txt_base_name + '.txt')
    # 拼接出 DPtmpyymmdd.txt 的绝对路径，该文件在 yymmddtmp 目录中
    dp_tmp_txt_base_dir = os.path.join(os.getcwd(), today + 'tmp', dp_tmp_txt_base_name + today + '.txt')
    # 拼接出 WBDPtmpyymmdd.txt 的绝对路径，该文件在 yymmddtmp 目录中
    wbdp_tmp_txt_base_dir = os.path.join(os.getcwd(), today + 'tmp', wbdp_tmp_txt_base_name + today + '.txt')

    # 拼接文件
    file_merge.file_merge(dp_tmp_txt_base_dir, wbdp_tmp_txt_base_dir, dp_new_base_txt_dir)


def hr_new_txt_pretreatment(today):
    # 拼接出 HRnew.txt 的绝对路径，该文件在 process 目录中
    hr_new_base_txt_dir = os.path.join(os.getcwd(), 'process', hr_new_txt_base_name + '.txt')
    # 拼接出 HRtmpyymmdd.txt 的绝对路径，该文件在 yymmddtmp 目录中
    hr_tmp_txt_base_dir = os.path.join(os.getcwd(), today + 'tmp', hr_tmp_txt_base_name + today + '.txt')
    # 拼接出 WBtmpyymmdd.txt 的绝对路径，该文件在 yymmddtmp 目录中
    wb_tmp_txt_base_dir = os.path.join(os.getcwd(), today + 'tmp', wb_tmp_txt_base_name + today + '.txt')

    # 拼接文件
    file_merge.file_merge(hr_tmp_txt_base_dir, wb_tmp_txt_base_dir, hr_new_base_txt_dir)


def file_process_txt_ldif(today):
    # 拼接出 HRnew.txt 的绝对路径，该文件在 process 目录中
    hr_new_base_txt_dir = os.path.join(os.getcwd(), 'process', hr_new_txt_base_name + '.txt')
    # 拼接出 DPnew.txt 的绝对路径，该文件在 process 目录中
    dp_new_base_txt_dir = os.path.join(os.getcwd(), 'process', dp_new_txt_base_name + '.txt')
    # 拼接出 HRbak.txt 的绝对路径，该文件在 process 目录中
    hr_bak_base_txt_dir = os.path.join(os.getcwd(), 'process', hr_bak_txt_base_name + '.txt')
    # 拼接出 DPbak.txt 的绝对路径，该文件在 process 目录中
    dp_bak_base_txt_dir = os.path.join(os.getcwd(), 'process', dp_bak_txt_base_name + '.txt')

    # 拼接出 HRyymmdd.txt 的绝对路径，该文件在 yymmdd 目录中
    hr_everyday_txt_base_dir = os.path.join(os.getcwd(), today, hr_everyday_txt_base_name + today + '.txt')
    # 拼接出 DPyymmdd.txt 的绝对路径，该文件在 yymmdd 目录中
    dp_everyday_txt_base_dir = os.path.join(os.getcwd(), today, dp_everyday_txt_base_name + today + '.txt')

    # 拼接出 DPadd.ldif 的绝对路径，该文件在 process 目录中
    add_tree_dp_ldif_dir = os.path.join(os.getcwd(), 'process', add_tree_dp_ldif_name)
    # 拼接出 HRadd.ldif 的绝对路径，该文件在 process 目录中
    add_tree_hr_ldif_dir = os.path.join(os.getcwd(), 'process', add_tree_hr_ldif_name)
    # 拼接出 DPdel.ldif 的绝对路径，该文件在 process 目录中
    del_tree_dp_ldif_dir = os.path.join(os.getcwd(), 'process', del_tree_dp_ldif_name)
    # 拼接出 HRdel.ldif 的绝对路径，该文件在 process 目录中
    del_tree_hr_ldif_dir = os.path.join(os.getcwd(), 'process', del_tree_hr_ldif_name)

    # 拼接出 DPdel.txt 的绝对路径，该文件在 yymmddtmp 目录中
    dp_del_base_txt_dir = os.path.join(os.getcwd(), today + 'tmp', dp_del_base_txt_name)
    # 拼接出 DPadd.txt 的绝对路径，该文件在 yymmddtmp 目录中
    dp_add_base_txt_dir = os.path.join(os.getcwd(), today + 'tmp', dp_add_base_txt_name)
    # 拼接出 HRdel.txt 的绝对路径，该文件在 yymmddtmp 目录中
    hr_del_base_txt_dir = os.path.join(os.getcwd(), today + 'tmp', hr_del_base_txt_name)
    # 拼接出 HRadd.txt 的绝对路径，该文件在 yymmddtmp 目录中
    hr_add_base_txt_dir = os.path.join(os.getcwd(), today + 'tmp', hr_add_base_txt_name)
    # 拼接出 DPtmp.txt 的绝对路径，该文件在 yymmddtmp 目录中
    dp_tmp_base_txt_dir = os.path.join(os.getcwd(), today + 'tmp', dp_tmp_base_txt_name)
    # 拼接出 HRtmp.txt 的绝对路径，该文件在 yymmddtmp 目录中
    hr_tmp_base_txt_dir = os.path.join(os.getcwd(), today + 'tmp', hr_tmp_base_txt_name)

    # 核心函数功能，先复制
    file_copy.file_copy(dp_new_base_txt_dir, dp_everyday_txt_base_dir)
    file_copy.file_copy(hr_new_base_txt_dir, hr_everyday_txt_base_dir)

    # 判断 DPbak.txt 或 HRbak.txt 是否存在，两者都存在，视为通常情况（非初始化的正常情况）
    # 两者都不存在时，视为初始化
    # 其他情况（一个存在另一个不存在），即 else 分支，异常处理
    if os.path.exists(hr_bak_base_txt_dir) and os.path.exists(dp_bak_base_txt_dir):
        # 通常情况
        # 初始化 DPadd.ldif HRadd.ldif DPdel.ldif HRdel.ldif
        is_exists = os.path.exists(del_tree_dp_ldif_dir)
        if is_exists:
            os.remove(del_tree_dp_ldif_dir)

        is_exists = os.path.exists(add_tree_dp_ldif_dir)
        if is_exists:
            os.remove(add_tree_dp_ldif_dir)

        is_exists = os.path.exists(del_tree_hr_ldif_dir)
        if is_exists:
            os.remove(del_tree_hr_ldif_dir)

        is_exists = os.path.exists(add_tree_hr_ldif_dir)
        if is_exists:
            os.remove(add_tree_hr_ldif_dir)

        # 将DPbak中存在&&DPnew中不存在的条目写入DPdel.txt
        file_comparison_add_diff_line.file_comparison_add_dup_line(dp_bak_base_txt_dir, dp_new_base_txt_dir,
                                                                   dp_del_base_txt_dir)
        # 将DPbak中存在&&DPnew中存在的条目写入DPtmp.txt
        file_comparison_add_dup_line.file_comparison_add_dup_line(dp_bak_base_txt_dir, dp_new_base_txt_dir,
                                                                  dp_tmp_base_txt_dir)
        # 将DPnew中存在&&DPtmp.txt中不存在的条目写入DPadd.txt
        file_comparison_add_diff_line.file_comparison_add_dup_line(dp_new_base_txt_dir, dp_tmp_base_txt_dir,
                                                                   dp_add_base_txt_dir)
        # 如果存在 DPdel.txt ，则使用 DPdel.txt 生成 DPdel.idlf
        is_exists = os.path.exists(dp_del_base_txt_dir)
        if is_exists:
            list_schema_dp_del = ["ou", "physicalDeliverOfficeName"]

            # 生成 DPdel.idlf
            for fields in file_util.FileUtil.read_file_data(dp_del_base_txt_dir):
                dict_fields = file_util.FileUtil.map_fields_list_schema(fields, list_schema_dp_del)
                with open(del_tree_dp_ldif_dir, 'a', encoding='utf-8') as f_tmp:
                    f_tmp.writelines('ou=' + str(dict_fields.get("ou")) + ',dc=tcrcb,dc=com' + '\n')

        # 如果存在 DPadd.txt ，则使用 DPadd.txt 生成 DPadd.idlf
        is_exists = os.path.exists(dp_add_base_txt_dir)
        if is_exists:
            list_schema_dp_add = ["ou", "physicalDeliverOfficeName"]

            # 生成 DPadd.idlf
            for fields in file_util.FileUtil.read_file_data(dp_add_base_txt_dir):
                dict_fields = file_util.FileUtil.map_fields_list_schema(fields, list_schema_dp_add)
                with open(add_tree_dp_ldif_dir, 'a', encoding='utf-8') as f_tmp:
                    f_tmp.writelines('dn: ou=' + str(dict_fields.get(
                        "ou")) + ',dc=tcrcb,dc=com' + '\n' + 'objectClass: top' + '\n' + 'objectClass: organizationalUnit' + '\n' + 'ou: ' + str(
                        dict_fields.get("ou")) + '\n' + 'physicalDeliveryOfficeName: ' + str(
                        dict_fields.get("physicalDeliverOfficeName")) + '\n\n')

        # 将HRbak中存在&&HRnew中不存在的条目写入HRdel.txt
        file_comparison_add_diff_line.file_comparison_add_dup_line(hr_bak_base_txt_dir, hr_new_base_txt_dir,
                                                                   hr_del_base_txt_dir)
        # 将HRbak中存在&&HRnew中存在的条目写入HRtmp.txt
        file_comparison_add_dup_line.file_comparison_add_dup_line(hr_bak_base_txt_dir, hr_new_base_txt_dir,
                                                                  hr_tmp_base_txt_dir)
        # 将HRnew中存在&&HRtmp.txt中不存在的条目写入HRadd.txt
        file_comparison_add_diff_line.file_comparison_add_dup_line(hr_new_base_txt_dir, hr_tmp_base_txt_dir,
                                                                   hr_add_base_txt_dir)
        # 如果存在 HRdel.txt ，则使用 HRdel.txt 生成 HRdel.idlf
        is_exists = os.path.exists(hr_del_base_txt_dir)
        if is_exists:
            list_schema_hr_del = ["ou", "physicalDeliverOfficeName", "cn", "sn", "description"]

            # 生成 HRdel.idlf
            for fields in file_util.FileUtil.read_file_data(hr_del_base_txt_dir):
                dict_fields = file_util.FileUtil.map_fields_list_schema(fields, list_schema_hr_del)
                with open(del_tree_hr_ldif_dir, 'a', encoding='utf-8') as f_tmp:
                    f_tmp.writelines('cn=' + str(dict_fields.get("cn")) + ',ou=' + str(dict_fields.get(
                        "ou")) + ',dc=tcrcb,dc=com' + '\n')

        # 如果存在 HRadd.txt ，则使用 HRadd.txt 生成 HRadd.idlf
        is_exists = os.path.exists(hr_add_base_txt_dir)
        if is_exists:
            list_schema_hr_add = ["ou", "physicalDeliverOfficeName", "cn", "sn", "description"]

            # 生成 HRadd.idlf
            for fields in file_util.FileUtil.read_file_data(hr_add_base_txt_dir):
                dict_fields = file_util.FileUtil.map_fields_list_schema(fields, list_schema_hr_add)
                with open(add_tree_hr_ldif_dir, 'a', encoding='utf-8') as f_tmp:
                    f_tmp.writelines('dn: cn=' + str(dict_fields.get("cn")) + ',ou=' + str(dict_fields.get(
                        "ou")) + ',dc=tcrcb,dc=com' + '\n' + 'objectClass: top' + '\n' + 'objectClass: person' + '\n' + 'objectClass: organizationalPerson' + '\n' + 'cn: ' + str(
                        dict_fields.get("cn")) + '\n' + 'sn: ' + str(
                        dict_fields.get("sn")) + '\n' + 'description: ' + str(dict_fields.get("description")) + '\n\n')

        # 复制 DPnew.txt 为 DPbak.txt
        file_copy.file_copy(dp_new_base_txt_dir, dp_bak_base_txt_dir)
        # 复制 HRnew.txt 为 HRbak.txt
        file_copy.file_copy(hr_new_base_txt_dir, hr_bak_base_txt_dir)

        print("通常情况已处理完成")

    elif (not os.path.exists(hr_bak_base_txt_dir)) and (not os.path.exists(dp_bak_base_txt_dir)):
        # 两者都不存在时，视为初始化
        file_copy.file_copy(dp_new_base_txt_dir, dp_bak_base_txt_dir)
        file_copy.file_copy(hr_new_base_txt_dir, hr_bak_base_txt_dir)
        # 预处理并生成 DPadd.ldif
        list_schema_dp = ["ou", "physicalDeliverOfficeName"]

        is_exists = os.path.exists(add_tree_dp_ldif_dir)
        if is_exists:
            os.remove(add_tree_dp_ldif_dir)

        for fields in file_util.FileUtil.read_file_data(dp_everyday_txt_base_dir):
            dict_fields = file_util.FileUtil.map_fields_list_schema(fields, list_schema_dp)
            with open(add_tree_dp_ldif_dir, 'a', encoding='utf-8') as f_tmp:
                f_tmp.writelines('dn: ou=' + str(dict_fields.get(
                    "ou")) + ',dc=tcrcb,dc=com' + '\n' + 'objectClass: top' + '\n' + 'objectClass: organizationalUnit' + '\n' + 'ou: ' + str(
                    dict_fields.get("ou")) + '\n' + 'physicalDeliveryOfficeName: ' + str(
                    dict_fields.get("physicalDeliverOfficeName")) + '\n\n')

        # 预处理并生成 HRadd.ldif
        list_schema_hr = ["ou", "physicalDeliverOfficeName", "cn", "sn", "description"]

        is_exists = os.path.exists(add_tree_hr_ldif_dir)
        if is_exists:
            os.remove(add_tree_hr_ldif_dir)

        for fields in file_util.FileUtil.read_file_data(hr_everyday_txt_base_dir):
            dict_fields = file_util.FileUtil.map_fields_list_schema(fields, list_schema_hr)
            with open(add_tree_hr_ldif_dir, 'a', encoding='utf-8') as f_tmp:
                f_tmp.writelines('dn: cn=' + str(dict_fields.get("cn")) + ',ou=' + str(dict_fields.get(
                    "ou")) + ',dc=tcrcb,dc=com' + '\n' + 'objectClass: top' + '\n' + 'objectClass: person' + '\n' + 'objectClass: organizationalPerson' + '\n' + 'cn: ' + str(
                    dict_fields.get("cn")) + '\n' + 'sn: ' + str(dict_fields.get("sn")) + '\n' + 'description: ' + str(
                    dict_fields.get("description")) + '\n\n')

        print("初始化已处理完成")
        # 之后依次执行 ldapadd 操作，先完成 DPadd.ldif 的添加，之后完成 HRadd.ldif  的添加
        # 需要编写调用目标操作系统 shell 命令的函数

    else:
        # 异常处理
        print("Oops, some errors have occurred in file_process_txt_ldif()!")
        sys.exit()


def shell_process_ldif(today):
    # 拼接出 DPadd.ldif 的绝对路径，该文件在 process 目录中
    add_tree_dp_ldif_dir = os.path.join(os.getcwd(), 'process', add_tree_dp_ldif_name)
    # 拼接出 HRadd.ldif 的绝对路径，该文件在 process 目录中
    add_tree_hr_ldif_dir = os.path.join(os.getcwd(), 'process', add_tree_hr_ldif_name)
    # 拼接出 DPdel.ldif 的绝对路径，该文件在 process 目录中
    del_tree_dp_ldif_dir = os.path.join(os.getcwd(), 'process', del_tree_dp_ldif_name)
    # 拼接出 HRdel.ldif 的绝对路径，该文件在 process 目录中
    del_tree_hr_ldif_dir = os.path.join(os.getcwd(), 'process', del_tree_hr_ldif_name)

    # 若 HRdel.ldif 存在，则执行 ldapdelete HRdel.ldif
    is_exists = os.path.exists(del_tree_hr_ldif_dir)
    if is_exists:
        os.system('ldapdelete -x -D "cn=admin,dc=tcrcb,dc=com" -w ldap -f ./process/HRdel.ldif')
        print("已更新人员信息：del")

    # 若 DPdel.ldif 存在，则执行 ldapdelete DPdel.ldif
    is_exists = os.path.exists(del_tree_dp_ldif_dir)
    if is_exists:
        os.system('ldapdelete -x -D "cn=admin,dc=tcrcb,dc=com" -w ldap -f ./process/DPdel.ldif')
        print("已更新部门信息：del")

    # 若 DPadd.ldif 存在，则执行 ldapadd DPadd.ldif
    is_exists = os.path.exists(add_tree_dp_ldif_dir)
    if is_exists:
        os.system('ldapadd -x -D "cn=admin,dc=tcrcb,dc=com" -w ldap -f ./process/DPadd.ldif')
        print("已更新部门信息：add")

    # 若 HRadd.ldif 存在，则执行 ldapadd HRadd.ldif
    is_exists = os.path.exists(add_tree_hr_ldif_dir)
    if is_exists:
        os.system('ldapadd -x -D "cn=admin,dc=tcrcb,dc=com" -w ldap -f ./process/HRadd.ldif')
        print("已更新人员信息：add")


def main():

    # 创建yymmdd与tmpyymmdd文件夹
    make_dir(os.path.join(os.getcwd(), date_now()))
    make_dir(os.path.join(os.getcwd(), date_now() + 'tmp'))

    # 创建process文件夹
    make_dir(os.path.join(os.getcwd(), 'process'))

    # 生成 HRtmpyymmdd.txt
    hr_txt_pretreatment(date_now())

    # 生成 DPtmpyymmdd.txt
    dp_txt_pretreatment(date_now())

    # 生成 WBtmpyymmdd.txt
    wb_txt_pretreatment(date_now())

    # 生成 WBDPtmpyymmdd.txt
    wbdp_txt_pretreatment(date_now())

    # 对 DPtmpyymmdd.txt WBDPtmpyymmdd 进行文件合并,形成 DPnew.txt
    dp_new_txt_pretreatment(date_now())

    # 对 HRtmpyymmdd WBtmpyymmdd 进行文件合并,形成 HRnew.txt
    hr_new_txt_pretreatment(date_now())

    # 核心处理函数，详细处理流程请见 README
    file_process_txt_ldif(date_now())

    # 调用 shell 进行 openldap 更新
    shell_process_ldif(date_now())


if __name__ == '__main__':
    print(time_now(), '系统开始启动')
    main()
