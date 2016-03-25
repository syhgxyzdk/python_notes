# encoding: utf-8
"""
查找pcm文件是否, 输出是否可能削波, 采样点, 削波点个数, 文件名
"""

import os
import struct
from sys import argv

def output_pcm_clipping_counter(pcm_file):
    pcm_size = os.path.getsize(pcm_file)
    clip_counter = 0 
    in_pcm = open(pcm_file, 'rb')
    sample_bytes = pcm_size/2
    for i in xrange(0, sample_bytes):
        _b = in_pcm.read(2)
        n, = struct.unpack('h', _b) 
        if n > 32000 or n < -32000:
            clip_counter += 1
    cut = 'No' if clip_counter < 500 else 'Yes'
    print "sample_bytes: %d\tclipped: %d\t 可能削波: %s\t %s" % (sample_bytes, clip_counter, cut, pcm_file)

def main():
    if len(argv) == 2:
        for pcm in os.listdir(argv[1]):
            if pcm.endswith('.pcm'):
                pcm_file = os.path.join(argv[1], pcm)
                output_pcm_clipping_counter(pcm_file)
    else:
        print "python %s pcm_dir" % argv[0]
  
  

if __name__ == '__main__':
    main()
