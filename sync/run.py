#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
# from syncart import  art
from syncart import  init

from syncart import lofter
from syncart import zhihu
from syncart import mpwx
from syncart import weibo
import os.path
import sys

try:
    input = raw_input
except:
    pass

if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = input('请输入要处理的url\n>  ')

# url = 'http://www.jianshu.com/p/86a670b9b1e1'

if (url.strip() == ''):
    print('要处理的文章url为空')
    sys.exit()

print(url)

qsj = input('请输入要处理的额外链接空格分隔\n>  ')
# qsj = 'http://www.jianshu.com/p/c0159a3e2f73 http://www.jianshu.com/p/0f39cf1bd4b2'


if qsj.strip() != '':

    qsj = qsj.strip().split(' ')
else:
    qsj = []
    
print(qsj)




# 根据简书发布的文章url，生成文章目录、img和index.md
# # 文章存放的路径在sync.py所在目录的上一级
file_parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir) + os.path.sep)


folder = init.fetch_url(file_parent_path, url)
print(folder)
qsj_folder_arr = []
for i in range(0, len(qsj)):

    # qsj_folder = {}
    # qsj_folder['folder'] = init.fetch_url(file_parent_path + os.path.sep + 'tmp', qsj[i])

    qsj_folder = init.get_qsj_folder(file_parent_path, qsj[i])
    qsj_folder_arr.append(qsj_folder)


# lofter.pub(file_parent_path, folder)
zhihu.pub(file_parent_path, folder)
# weibo.pub(file_parent_path, folder)
# mpwx.pub(file_parent_path, folder, qsj_folder_arr, url)

init.clean_tmp(file_parent_path + os.sep + 'tmp')




