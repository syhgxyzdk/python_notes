# encoding: utf-8

# 判断*.log文件是否在变化(以此来判断下发的音频数据是否完成)

import os
import time

# 判断*.log文件是否在变化(以此来判断下发的音频数据是否完成)
def wait_for_downloading_done():
    while 1:
        if is_downloading():
            time.sleep(2)
            print 'waiting audio file downloading ...'
        else:
            break

def is_downloading():
    stamp_list_begin = get_stamp_list()
    time.sleep(3)
    stamp_list_end = get_stamp_list()
    if stamp_list_end == stamp_list_begin:
        #print 'no timestamp changed'
        return False
    #print 'timestamp changed'
    return True

def get_log_list():
    log_list = []
    for file_name in os.listdir('./'):
        if file_name.endswith('.adpcm'):
            log_list.append(file_name)
    return log_list

def get_file_timestamp(file_name):
    return os.path.getmtime(file_name)

def get_stamp_list():
    log_list = get_log_list()
    return [get_file_timestamp(x) for x in log_list]

if __name__ == '__main__':
    wait_for_downloading_done()
