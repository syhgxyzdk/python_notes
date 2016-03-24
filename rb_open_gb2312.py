# coding: utf-8

"""
三个文件, 分别为utf-8, gb2312, utf-16
[root@lb-vm3 tmp]# file file.a
file.a: UTF-8 Unicode text
[root@lb-vm3 tmp]# file file.win.txt 
file.win.txt: ISO-8859 text, with no line terminators
[root@lb-vm3 tmp]# file file.win.utf8.txt 
file.win.utf8.txt: Little-endian UTF-16 Unicode text, with no line terminators

正确打开这些文件的方式如下:
""""

with open('file.a', 'rb') as inlns:
    for ln in inlns:
        if ln.strip():
            print ln.strip().decode('utf-8')

with open('file.win.txt', 'rb') as inlns:
    for ln in inlns:
        if ln.strip():
            print ln.strip().decode('gb2312')

with open('file.win.utf8.txt', 'rb') as inlns:
    for ln in inlns:
        if ln.strip():
            print ln.strip().decode('utf-16')
            
            
"""
输出:
[root@lb-vm3 tmp]# python tmp.py 
this is file.a
中文字符的默认编码
this is file.win.txt
中文字符的默认编码
this is file.win.utf8.txt
中文字符的默认编码

"""
