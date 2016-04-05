# encoding: utf-8

"""
找出稳定性测试中响应时间: >1s, >2s 或指定秒的比例.
默认不输入参数, 找出>1s 和 >2s的比例.
输入一个数字参数, 比如python this_script.py 3, 会找出>1s, >2s和>3s的比例.
"""

import re
from sys import argv

rc = re.compile(r'\d{1,3}\.\d{1,3}\ssecs:')


if len(argv) == 1:
    argv.append(2)
print argv

time_list = range(1, int(argv[-1]) + 1)
counter_list = ['counter_%ds' % x for x in time_list]
counter_dict = {}
for key in counter_list:
    counter_dict[key] = 0

total = 0
output = file('longer_reps.txt', 'w')

with open('stab.log') as log:
    for ln in log:
        find = rc.findall(ln.strip())
        if find:
            total += 1
            reps_time = float(find[0].split(' ')[0])
            for x in time_list:
                if reps_time > x:
                    key = 'counter_%ds' % x
                    counter_dict[key] += 1
                    output.write(ln)

print "total: %d" % total
for k, v in counter_dict.items():
    rating = "%.2f" % (float(v) / float(total) * 100) + '%'
    print "%s+: %d\trating: %s" % (k, v, rating)

