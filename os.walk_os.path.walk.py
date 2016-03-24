# os.walk()

import os

root = './'

for root,dirs,fnames in os.walk(root):

    for dr in dirs:

        print os.path.join(root, dr)

    print 'files here:'

    for f in fnames:

        print os.path.join(root,f)



import os
root = './'
for root, dirs, fnames in os.walk(root):
    for f in fnames:
        print os.path.join(root, f)


"""
函数声明：os.walk(top,topdown=True,onerror=None)

(1)参数top表示需要遍历的顶级目录的路径。

(2)参数topdown的默认值是“True”表示首先返回顶级目录下的文件，然后再遍历子目录中的文件。
当topdown的值为"False"时，表示先遍历子目录中的文件，然后再返回顶级目录下的文件。

(3)参数onerror默认值为"None"，表示忽略文件遍历时的错误。
如果不为空，则提供一个自定义函数提示错误信息后继续遍历或抛出异常中止遍历。

返回值：
函数返回一个元组，含有三个元素。
这三个元素分别是：每次遍历的路径名、路径下子目录列表、目录下文件列表。
"""
#os.walk使用实例：删除某个文件夹（当然可以通过os.listdir的递归调用删除）

01	#! /usr/bin/env python
02	# coding=utf-8
03	import os
04	

05	def Remove_dir(top_dir):
06	    if os.path.exists(top_dir)==False:
07	        print "not exists"
08	        return
09	    if os.path.isdir(top_dir)==False:
10	        print "not a dir"
11	        return
12	    for dir_path,subpaths,files in os.walk(top_dir,False):
13	        for file in files:
14	            file_path=os.path.join(dir_path,file)
15	            print "delete file:%s"  %file_path
16	            os.remove(file_path)
17	        print "delete dir:%s" %dir_path
18	        os.rmdir(dir_path)
19	
"""
#调用
21	Remove_dir(r"C:\Users\Administrator\Desktop\zrbuN7zRuc")
# os.path.walk

函数声明：os.path.walk(top,func,arg)

(1)参数top表示需要遍历的目录路径

(2)参数func表示回调函数，即对遍历路径进行处理的函数。
所谓回调函数，是作为某个函数的参数使用，当某个时间触发时，程序将调用定义好的回调函数处理某个任务。
注意：walk的回调函数必须提供三个参数：
第1个参数为os.path.walk的参数arg，
第2个参数表示目录dirname，
第3个参数表示文件列表names。

注意：os.path.walk的回调函数中的文件列表不和os.walk()那样将子目录和文件分开，而是混为了一摊，需要在回调函数中判断是文件还是子目录。

(3)参数arg是传递给回调函数的元组，为回调函数提供处理参数，arg可以为空。回调函数的第1个参数就是用来接收这个传入的元组的。

过程：
以top 为根的目录树中的每一个目录 (包含 top 自身，如果它是一个目录)，以参数 (arg, dirname, names)调用回调函数 funct。
参数 dirname 指定访问的目录，参数 names 列出在目录中的文件(从 os.listdir(dirname)中得到)。
回调函数可以修改 names 改变 dirname 下面访问的目录的设置，例如，避免访问树的某一部分。
由 names 关连的对象必须在合适的位置被修改，使用 del 或 slice 指派。
注意：符号连接到目录不被作为一个子目录处理，并且因此 walk()将不访问它们。
访问连接的目录你必须以os.path.islink(file) 和 os.path.isdir(file)标识它们，并且必须调用walk() 。 

os.path.walk使用实例：
遍历文件夹下所有文件（os.path.walk()不能用于删除文件夹（可能是我没想到），因为os.path.walk()先遍历顶级目录，再遍历子目录中的文件）。
"""
01	#! /usr/bin/env python
02	#coding=utf-8
03	import os
04	#回调函数
05	def find_file(arg,dirname,files):
06	    for file in files:
07	        file_path=os.path.join(dirname,file)
08	        if os.path.isfile(file_path):
09	            print "find file:%s" %file_path
10	
"""
12	#调用
13	os.path.walk(r"C:\Users\Administrator\Desktop\4",find_file,())

区别：
os.path.walk()与os.walk()产生的文件名列表并不相同，
os.walk()产生目录树下的目录路径和文件路径，
而os.path.walk()只产生文件路径（是子目录与文件的混合列表）。
"""
