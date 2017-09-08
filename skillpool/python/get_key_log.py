# -*- coding: utf-8 -*-
import linecache
import re
import sys

################################################################
# [Version: 1.0] Zong @ 28-July-2017
# egg.
# python get_key_log.py file_path  key start_line opt_line opt_type
# python get_key_log.py /app/jetty/server/实例名称/logs/novatar_20170717.0.log  error 2000 1000 1
# opt_type = 0 : 代表查找
# opt_type = 1 : 向上查找
# opt_type = 2 : 向下查找
# opt_type = 3 : 向上翻看
# opt_type = 4 : 向下翻看
################################################################
import os


def getParameters():
    '''
        get parameters from console command
    '''
    ret = []
    if len(sys.argv) != 6:
        print('Please input correct parameter, for example:')
        print('python get_key_log.py /app/jetty/server/实例名称/logs/novatar_20170717.0.log  error 2000 1000 1')
        sys.exit()
    else:
        for i in range(0, len(sys.argv)):
            # print(i, sys.argv[i]
            ret.append(sys.argv[i])
    return ret
# 从开始行往上查找匹配key，如没找到顶多5万行，找到则显示key所在的行后500行
def find_log(file_path, key, start_line):
    lines = linecache.getlines(file_path)
    if start_line > len(lines):
        start_line = len(lines)
    find_lines = lines[:start_line]
    opt_line = None
    log = None
    count = 0
    for i in range(start_line - 2, -1, -1):
        if i > start_line -50000:
            rs = re.search(key, find_lines[i], re.IGNORECASE)
            if rs:
                count += 1
                opt_line = i + 1
                if opt_line + 500 <= len(lines):
                    log = lines[opt_line - 1 : opt_line + 500 - 1]
                else:
                    log = lines[opt_line - 1 : ]
                break
        else:
            break
    if count == 0 : opt_line = start_line
    return opt_line, log

#向上查找
def up_find(file_path, key, opt_line):
    return find_log(file_path, key, opt_line)

#向下查找
def down_find(file_path, key, opt_line):
    lines = linecache.getlines(file_path)
    if opt_line > len(lines):
        opt_line = len(lines)
    log = None
    for i in range(opt_line , len(lines)):
        if i < opt_line + 50000:
            rs = re.search(key, lines[i], re.IGNORECASE)
            if rs:
                opt_line = i + 1
                if opt_line + 500 <= len(lines):
                    log = lines[opt_line - 1: opt_line + 500 - 1]
                else:
                    log = lines[opt_line - 1: ]
                break
        else:
            break
    return opt_line, log

#向上翻看
def look_up(file_path, opt_line):
    lines = linecache.getlines(file_path)
    if opt_line > len(lines): opt_line = len(lines)
    if opt_line < 500:
        log = lines[:opt_line]
        opt_line = 1
    else:
        log = lines[opt_line -500 : opt_line]
        opt_line = opt_line - 500 + 1
    return opt_line, log
# 向下翻看
def look_down(file_path, opt_line):
    lines = linecache.getlines(file_path)
    if opt_line > len(lines): opt_line = len(lines)
    if opt_line + 500 >= len(lines):
        log = lines[opt_line - 1 : ]
        opt_line = len(lines)
    else:
        log = lines[opt_line : opt_line + 500]
        opt_line = opt_line + 500 - 1
    return opt_line, log

def main():
    data = {}
    result = {}
    status = None
    ls = getParameters()
    file_path = ls[1]
    key = ls[2]
    start_line = int(ls[3])
    opt_line = int(ls[4])
    opt_type = int(ls[5])
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            if opt_type == 0:
                opt_line, log = find_log(file_path, key, start_line)
            elif opt_type == 1:
                opt_line, log = up_find(file_path, key, opt_line)
            elif opt_type == 2:
                opt_line, log = down_find(file_path, key, opt_line)
            elif opt_type == 3:
                opt_line, log = look_up(file_path, opt_line)
            elif opt_type == 4:
                opt_line, log = look_down(file_path, opt_line)
            status = 'succeed'
            msg = 'get key log success!'
            result['opt_line'] = opt_line
            result['log'] = log
        else:
            status = 'failure'
            msg = 'ERROR:Input path is not a file!'
    else:
        status = 'failure'
        msg = 'ERROR:Input path is not exit!'
    data['status'] = status
    data['msg'] = msg
    data['result'] = result
    linecache.clearcache()
    print(data)

if __name__ == '__main__':
    main()