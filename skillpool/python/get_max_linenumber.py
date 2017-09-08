# -*- coding: utf-8 -*-
import os
import sys
import linecache

# python get_max_linenumber.py file_path

def getParameters():
    if len(sys.argv) != 2:
        print('Please input a parameter and only one, for example:')
        print('python get_max_linenumber.py /app/jetty/server/实例名称/logs/novatar_20170716.0.log')
        sys.exit()
    else:
        file_path = sys.argv[1]
    return file_path

def main():
    file_path = getParameters()
    data = {}
    result = None
    status = None
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            max_linenumber = len(linecache.getlines(file_path))
            status = 'succeed'
            msg = 'get max line number success!'
            result = max_linenumber
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