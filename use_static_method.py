# coding: utf-8

'''
并发调用后, 收集Total, Pass, Fail等统计信息.
用静态方法, 装饰器.

'''


import bs4 # using bs4.BeautifulSoup to parse html5 (get 'Play' button and mp3 url link)
import re
import time
from time import sleep
import urllib2
from threading import Thread



CC_NUM = 50
Req_Id_File = 'req_id.txt'
Req_Id_File = 'req_id500.txt'
# Link_pattern = re.compile(r'"html5Url":"http[^"]*')
URL_Prefix = 'http://10.10.19.11:8080/smg_service/m/getconn?reqId=%s'


class HTML5_CC(Thread):
    Total = 0
    Succ = 0
    Fail = 0
    Total_time = 0

    def __init__(self, req_id):
        Thread.__init__(self)
        self.req_id = req_id.strip()
    
    def html5_can_play(self, html_doc):
        if html_doc.strip():
            sp = bs4.BeautifulSoup(html_doc)
            if sp.find(id="asrAudio") is not None and sp.find(onclick="playAudio()") is not None:
                return True
            return False
        else:
            return False

    def get_resp(self, html5_url):
        """ 返回html5的响应时间和html_doc """
        begin = time.time()
        html_doc = ''
        reps = 0
        try:
            html_doc = urllib2.urlopen(html5_url, timeout=7).read()
            reps = '%.2f' % ((time.time() - begin) * 1000)
        except:
            reps = 7000
            print 'open url err: %s' % html5_url
        # print reps + 'ms', html5_url
        return [float(reps), html_doc]

    def run(self):
        if  self.req_id:
            html5_url = URL_Prefix % self.req_id
            rep_time, html_doc = self.get_resp(html5_url)
            HTML5_CC.Total += 1
            HTML5_CC.Total_time += rep_time
            if self.html5_can_play(html_doc):
                HTML5_CC.Succ += 1
            else:
                HTML5_CC.Fail += 1
                print 'Fail', html5_url
        else:
            print 'Skipped empty request id ..'

    @staticmethod
    def get_avg_time():
        return HTML5_CC.Total_time / HTML5_CC.Total


def main():
    thread_num = CC_NUM
    Req_ID_List = open(Req_Id_File).readlines()
    req_id_num = len(Req_ID_List)

    print 'Run %d\tthreads vs %d\t urls ...' % (thread_num, req_id_num)
    for i in range(0, req_id_num / thread_num + 1):
        threads = []
        for j in range(0, thread_num):
            index = i * thread_num + j
            if index < req_id_num:
                t = HTML5_CC(Req_ID_List[index])
                threads.append(t)
        for x in range(0, len(threads)):
            threads[x].start()
        for x in range(0, len(threads)):
            threads[x].join()

    avg_time = HTML5_CC.get_avg_time()
    t, p, f = HTML5_CC.Total, HTML5_CC.Succ, HTML5_CC.Fail
    print '-' * 80
    print 'Total: %d Succ: %d Fail: %d Avg_Resp_Time: %.2fms' % (t, p, f, avg_time)
    print '-' * 80
    return t, p, f, avg_time


def stab_run(hours=12):
    T = P = F = AT = 0
    print 'stab'
    loop = hours * 60 * 60 / 100
    i = 0
    while i < loop:
        t, p, f, at = main()
        i += 1
        T += t
        P += p
        F += f
        AT += at
        print 'loop %d done ...' % i
    print '-' * 80
    print 'Total: %d Succ: %d Fail: %d Avg_Resp_Time: %.2fms' % (T, P, F, AT)
    print '-' * 80



if __name__ == '__main__':
    main()
    # stab_run()
