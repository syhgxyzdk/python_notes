# encoding: utf-8

"""
1.检查所有的pcm的md5值是否相同，期望是不相同，输出md5值相同的“语音路径/语音文件名”
2.检查所有的pcm文件和对应的标注文本文件，一一对应，不多不少，输出缺少对应的文件名；
3.检查speakerinfo中的文件名都能在pcm中找到；
4.检查所有的标注文本文件的格式是否正确：输出格式不正确的
（1）格式：开始时间 结束时间 文本 识别结果的标记 <念错等>，前三列必须有，且必须是时间 时间 文本
（2）结束时间必须大于开始时间
调试用的数据：美的冷唤醒语音集

    judge_md5_unique()
    judge_file_in_speaker_list()
    judge_each_pcm_has_note()
    judge_pcm_note_format()

"""
import os
import re
from hashlib import md5


# 子文件名/pcm名: [md5值]
Total_Dict = {}
md5_dict = {}
Speaker_List = []

Ln_Pattern = re.compile(u'\d{2}\.\d{6}\s\d{2}\.\d{6}\s[\d\u4eee-\u9fff]+[\u4eee-\u9fff]+\s?.*')
Root_Dir = './'
PCM_Ext = '.pcm'
Note_Ext = '.annote'
Speaker_Info = 'speaker_info.txt'
Output_Log = 'missing_or_dup.txt'

def is_correct_ln(ln):
    ln_parts = ln.split(' ')
    if len(ln_parts) < 3:
        return False
    if not Ln_Pattern.match(ln.strip().decode('utf-8')):
        return False
    try:
        beg = float(ln_parts[0])
        end = float(ln_parts[1])
        if beg >= end:
            return False
    except Exception, e:
        print e
        return False
    return True

def check_file_format(note_file):
    '''
    检查标注文本是否正确：返回格式不正确的信息
    '''
    r = note_file
    with open(note_file) as note:
        for ln in note:
            if ln.strip():
                if not is_correct_ln(ln):
                    r += '\n格式错误行 : %s\n' % ln.strip()
    return r

def judge_pcm_note_format():
    output = file(Output_Log, 'a')
    output.write('\n\n========== 标注文件格式错误的列表如下: ==========\n\n')
    for k in Total_Dict.keys():
        tar_note = k.replace(PCM_Ext, Note_Ext)
        if os.path.exists(tar_note):
            r = check_file_format(tar_note)
            if r != tar_note:
                output.write('- ' * 10 + '\n')
                output.write(r)
    output.close()

def judge_each_pcm_has_note():
    output = file(Output_Log, 'a')
    output.write('\n\n========== 缺少标注文件的pcm列表如下: ==========\n\n')
    for k in Total_Dict.keys():
        tar_note = k.replace(PCM_Ext, Note_Ext)
        if not os.path.exists(tar_note):
            output.write(k + '\n')

    output.close()

def judge_md5_unique():
    output = file(Output_Log, 'a')
    output.write('\n\n========== 重复的pcm文件列表如下: ==========\n\n')
    tmp_dict = {}
    # 颠倒total_dict的键值, 来判断md5是否唯一.
    for k,v in Total_Dict.items():
        md5 = v[0]
        if tmp_dict.has_key(md5):
            tmp_dict[md5].append(k)
        else:
            tmp_dict[md5] = [k]

    for k,v in tmp_dict.items():
        print k,v
        if len(v) > 1:
            for item in v:
                output.write('%s -> %s\n' % (item, k))
            output.write('-' * 50)
    output.close()

def judge_file_in_speaker_list():
    sep = os.sep
    output = file(Output_Log, 'a')
    output.write('\n\n========== 丢失的pcm文件列表如下: ==========\n\n')
    
    all_pcm = []
    for k in Total_Dict.keys():
        pcm = k.split(sep)[-1]
        all_pcm.append(pcm)
            
    for pcm in Speaker_List:
        if pcm not in all_pcm:
            output.write(pcm + '\n')
    output.close()

def get_md5(name):
    m = md5()
    a_file = open(name, 'rb')
    m.update(a_file.read())
    a_file.close()
    r = m.hexdigest()
    del m
    return r

def init_total_dict():
    # 遍历当前目录, 用pcm文件做key, md5做value第一个元素.
    for root, dirs, files in os.walk(Root_Dir):
        for filespath in files:
            tar_file = os.path.join(root, filespath)
            if tar_file.endswith(PCM_Ext):
                md5 = get_md5(tar_file)
                Total_Dict[tar_file] = [md5]
                # print tar_file, md5

def init_speaker_list():
    with open(Speaker_Info) as info:
        for ln in info:
            if ln.strip():
                Speaker_List.append(ln.split('\t')[0])

def init_log():
    if os.path.exists(Output_Log):
        os.remove(Output_Log)


def main():
    init_log()
    init_total_dict()
    init_speaker_list()
    judge_md5_unique()
    judge_file_in_speaker_list()
    judge_each_pcm_has_note()
    judge_pcm_note_format()


if __name__ == '__main__':
    main()
