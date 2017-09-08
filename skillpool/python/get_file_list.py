# -*- encoding: utf-8 -*-
import os.path
import sys

# python get_file_list.py dir_path

#get dirPath
def getParameters():
    if len(sys.argv) != 2:
        print('Please input a parameter and only one, for example:')
        print('python get_file_list.py /app/jetty/server/实例名称/logs/')
        sys.exit()
    else:
        dir_path = sys.argv[1]
    return dir_path
#sorting folder list according to create time
def swap(target_list):
    for i in range(len(target_list)):
        if i < (len(target_list)-1) and target_list[i][0] > target_list[i+1][0]:
            temp = target_list[i+1]
            target_list[i+1] = target_list[i]
            target_list[i] = temp
        else:
            continue
    return target_list
def main():
    dir_log = getParameters()
    data = {}
    result = None
    status = None
    if os.path.exists(dir_log):
        if os.path.isdir(dir_log):
            file_names = os.listdir(dir_log)
            file_temp = file_names[:]
            # delete file start with '.'
            for file in file_names:
                if file.startswith('.') or os.path.isdir(dir_log + os.sep + file):
                    file_temp.remove(file)
            file_names = file_temp
            # file_names.remove('System Volume Information')
            files_with_time = [(os.path.getctime(dir_log + os.sep + folder), folder) for folder in
                               file_names]
            # create a list with 2 elements, one is folder name and the other is create time
            # print("the orginal filelist is")
            # print(files_with_time)
            cyc_times = len(files_with_time)
            i = 0
            while (i < cyc_times):  # a cycle to re-arrange folder
                i = i + 1
                files_with_time = swap(files_with_time)
            lis = []
            for file in files_with_time:
                lis.append(file[1])
            lis.reverse()
            # print less than 500 files
            if len(lis) >= 500:
                lis = lis[:500]
            status = 'succeed'
            msg = 'get file list success!'
            result = lis
        else:
            status = 'failure'
            msg = 'ERROR:Input path is a file!'
    else:
        status = 'failure'
        msg = 'ERROR:Input path is not exit!'
    data['status'] = status
    data['msg'] = msg
    data['result'] = result
    print(data)


if __name__ == '__main__':
    main()