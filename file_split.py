import os, sys
from settings import Settings
import datetime
import re

def tail(file, taillines=500, return_str=True, avg_line_length=None):
    with open(file, errors='ignore') as f:
        if not avg_line_length:
            f.seek(0, 2)
            f.seek(f.tell() - 3000)
            avg_line_length = int(3000 / len(f.readlines())) + 10
        f.seek(0, 2)
        end_pointer = f.tell()
        offset = taillines * avg_line_length
        if offset > end_pointer:
            f.seek(0, 0)
            lines = f.readlines()[-taillines:]
            return "".join(lines) if return_str else lines
        offset_init = offset
        i = 1
        while len(f.readlines()) < taillines:
            location = f.tell() - offset
            f.seek(location)
            i += 1
            offset = i * offset_init
            if f.tell() - offset < 0:
                f.seek(0, 0)
                break
        else:
            f.seek(end_pointer - offset)
        lines = f.readlines()
        if len(lines) >= taillines:
            lines = lines[-taillines:]

        return "".join(lines) if return_str else lines


def split_by_count(src_file, count):
    filedir, name = os.path.split(src_file)
    name, ext = os.path.splitext(name)
    filedir = os.path.join(filedir, 'count')
    if not os.path.exists(filedir):
        os.mkdir(filedir)

    partno = 0
    stream = open(src_file, 'r', encoding='utf-8')
    while True:
        partfilename = os.path.join(filedir,name + '_' + str(partno) + ext)
        print('write start %s' % partfilename)
        part_stream = open(partfilename, 'w', encoding='utf-8')
 
        read_count = 0
        while read_count < count:
            read_content = stream.readline()
            if read_content:
                part_stream.write(read_content)
            else:
                break
            read_count += 1
          
        part_stream.close()
        if (read_count < count) :
            break
        partno += 1


def split_by_date(src_file):

    filedir, name = os.path.split(src_file)
    name, ext = os.path.splitext(name)
    filedir = os.path.join(filedir, 'date')
    if not os.path.exists(filedir):
        os.mkdir(filedir)

    stream = open(src_file, 'r', encoding='utf-8')
    first_content = stream.readline()
    first_dict = eval(first_content)

    last_content = tail(src_file, 1)
    last_dict = eval(last_content)
    end_date = last_dict['@timestamp'].split("T")[0]
    end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
    date = first_dict['@timestamp'].split("T")[0]
    while True:
        partfilename = os.path.join(filedir, name + ext + '.' + str(date))
        print('write start %s' % partfilename)
        part_stream = open(partfilename, 'w', encoding='utf-8')
        re_timestamp = re.compile(r'(?<="@timestamp":").*?(?=T)')

        dt = datetime.datetime.strptime(date, "%Y-%m-%d")
        while (dt <= end_dt):
            read_content = stream.readline()
            log_date = date # 解决日志格式不统一导致跳出循环的问题
            if '@timestamp' in read_content:
                # 效率太慢
                # content_dict = eval(read_content)
                # log_date = content_dict['@timestamp'].split("T")[0]
                log_date = re_timestamp.search(read_content).group()
            elif not read_content:
                log_date = ''
            if date == log_date:
                part_stream.write(read_content)
            else:
                break
        part_stream.close()
        if (dt >= end_dt):
            break
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")

def return_cut_list(lst):
        rt = []
        n = 0
        for i in range(len(lst)-1):
            if lst[i].split('.')[-1] != lst[i+1].split('.')[-1]:
                rt.append(lst[n:i+1])
                n = i+1
        rt.append(lst[n:])
        return rt

def get_date(str):
    date = str.split('.')[-1]
    return date

def merge_by_date(src_dir):
    filenames = []
    merge_filedir = os.path.join(src_dir, 'date')
    if not os.path.exists(merge_filedir):
        os.mkdir(merge_filedir)
    for filename in os.listdir(src_dir):
        if not os.path.isdir(os.path.join(src_dir, filename)):
            filenames.append(filename)
    filenames = sorted(filenames, key=get_date)
    filenames = return_cut_list(filenames)
    for merge_list in filenames:
        merge_filename = "gateway.log." + str(get_date(merge_list[0]))
        merge_filename = os.path.join(merge_filedir, merge_filename)
        print('write start %s' % merge_filename)
        merge_stream = open(merge_filename, 'w', encoding='utf-8')
        for filename in merge_list:
            filename = os.path.join(src_dir, filename)
            stream = open(filename, 'r', encoding='utf-8')
            merge_stream.write(stream.read())
            stream.close()
        merge_stream.close()
        

if __name__ == '__main__':

    src_file = './access_login/access.log'
    src_dir = './gateway_login/'
    # split_by_count(src_file, 500000)
    merge_by_date(src_dir)