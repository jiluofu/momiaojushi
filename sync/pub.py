from syncart import  art
from syncart import  init
from syncart import  lofter_pub
from syncart import  zhihu_pub
import os.path

try:
    input = raw_input
except:
    pass

# url = input('请输入要处理的url\n>  ')

# # 根据简书发布的文章url，生成文章目录、img和index.md
# # # 文章存放的路径在sync.py所在目录的上一级
file_parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir) + os.path.sep)

# # init.fetch_url(file_parent_path, 'http://www.jianshu.com/p/fadd67ed6709')
# # folder = init.fetch_url(file_parent_path, 'http://www.jianshu.com/p/f494b2fac958')
# folder = init.fetch_url(file_parent_path, url)
# print(folder)

# # folder = input('请输入要处理的目录名\n>  ')

# art.get_imgs(file_parent_path, folder, 'zhihu');
# art.get_imgs(file_parent_path, folder, 'lofter');

lofter_pub.pub(file_parent_path, '289_20161123_与喵共舞153~漂亮的皮鞋')
# zhihu_pub.pub(file_parent_path, '289_20161123_与喵共舞153~漂亮的皮鞋')