# coding: utf-8

'''

audioConverter： 微信适配里面做音频转换的服务。简称ac。

post url to 微信服务(触发opus >> MP3转换)

'''

import re
import json
import urllib
import urllib2
import time

from time import sleep

Mp3_down_url_pattern = re.compile(r'http://.*\.[mpMP3]')

# 音频转换接口
AC_url = 'http://10.30.2.252:8181/audioConverter/ac?'

# 获取对应的MP3接口
Ret_url = 'http://10.30.2.252:8181/audioConverter/aq?'


# 第一个url必须以post方式才能触发
def post_request_id(req_id):
    # ac_url + 'reqID=7de355f16ff291ae31b005958719e70f'

    # para = {'reqID': req_id}
    para = {'reqID': req_id}
    post_data = urllib.urlencode(para)         # 进行url编码
    req = urllib2.Request(AC_url, post_data)    # 生成Request对象
    resp = urllib2.urlopen(req)
    ret_str = resp.read()
    print ret_str
    return ret_str

    # postDict = {}
    # postDict["method"] = "CommonQueryService"
    # postDict["params"] = params
 
    # #postData = urllib.urlencode(postDict);
    # postData = json.dumps(postDict, ensure_ascii=False)
    # req = urllib2.Request(AC_url, postData);

    # # in most case, for do POST request, the content-type, is application/x-www-form-urlencoded
    # req.add_header('Content-Type', "application/x-www-form-urlencoded");
    # resp = urllib2.urlopen(req);



def get_mp3_reuslt(req_id):
    # ret_url + 'reqID=7de355f16ff291ae31b005958719e70f'
    sleep(0.5)
    url = Ret_url + 'reqID=%s' % req_id
    ret = urllib2.urlopen(url).read()
    print ret
    mp3_url = Mp3_down_url_pattern.findall(ret)[0]
    print mp3_url
    return ret


def main():
    req_id = '70e1b76bcfa9b0cdce9315e22d6375b6'.lower()
    print req_id
    post_request_id(req_id)
    get_mp3_reuslt(req_id)


if __name__ == '__main__':
    main()
