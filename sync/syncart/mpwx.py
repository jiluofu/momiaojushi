#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Required
- requests (必须)
- pillow (可选)
Info
- author : "zhuxu"
- email  : "zhu.xu@qq.com"
- date   : "2016.11.11"
Update

'''
import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path
try:
    from PIL import Image
except:
    pass
# import pytesseract
import hashlib   
import json
import sys

from syncart import init
import configparser

cf = configparser.RawConfigParser()
cf.read(os.path.dirname(__file__) + os.path.sep + 'sync.conf')
username = cf.get('mpwx', 'username')
password = cf.get('mpwx', 'password')

agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
    'Host': 'mp.weixin.qq.com',
    'Referer': 'https://mp.weixin.qq.com/cgi-bin/loginpage?t=wxm2-login&lang=zh_CN',
    'User-Agent': agent
}

# 使用登录cookie信息
session = requests.session()

token = ''



def login(username, password):


    t = str(int(time.time() * 1000))

    # 微信公众平台的密码要md5
    m = hashlib.md5()
    m.update(password.encode('utf-8'))
    password = m.hexdigest()

    # 提交登录用户名的url
    post_url = 'https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN'
    postdata = {
    
        'pwd': password,
        'username': username,
        'f': 'json',
        'imgcode': ''
    }

    headers['Content-Type'] = 'application/x-www-form-urlencoded'



    login_page = session.post(post_url, data=postdata, headers=headers)
    session.cookies.save()
    print(login_page.text)
    res = eval(login_page.text)
    # 登录提交后得到跳转的url
    url = 'https://mp.weixin.qq.com' + res['redirect_url']
    print(url)   

    # 获取ticket的post请求
    post_url = 'https://mp.weixin.qq.com/misc/safeassistant?1=1&token=&lang=zh_CN'
    

    data = {

        'lang': 'zh_CN',
        'f': 'json',
        'action': 'get_ticket',
        'auth': 'ticket'
    }
   
    login_page = session.post(post_url, data=data, headers=headers)
    session.cookies.save()
    print(login_page.text)
    res = eval(login_page.text)
    ticket = res['ticket']

    # 获取uuid的接口，需要提交appid和上面的ticket
    post_url = 'https://mp.weixin.qq.com/safe/safeqrconnect?1=1&token=&lang=zh_CN'
    
    # appid是一个写死的值
    appid = 'wx3a432d2dbe2442ce'
    data = {

        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': t,
        'appid': appid,
        'scope': 'snsapi_contact',
        'state': '0',
        'redirect_uri': 'https://mp.weixin.qq.com',
        'login_type': 'safe_center',
        'type': 'json',
        'ticket': ticket
    }

    # print(data)
   
    login_page = session.post(post_url, data=data, headers=headers)
    session.cookies.save()
    # print(login_page.text)
    res = eval(login_page.text)
    uuid = res['uuid']
    # print(uuid)

    # 二维码的图片url，需要上面的ticket和uuid
    img_url = 'https://mp.weixin.qq.com/safe/safeqrcode?ticket=' + ticket + '&uuid=' + uuid + '&action=check&type=login&auth=ticket&msgid=427152200'
    print(img_url)

    r = session.get(img_url, headers=headers)
    with open('qrcode.jpg', 'wb') as f:
        f.write(r.content)
        f.close()

    im = Image.open('qrcode.jpg')
    im.show()
    im.close()


    print('waiting for qrcode')
    time.sleep(10)
    print('going on')


    post_url = 'https://mp.weixin.qq.com/safe/safeuuid?timespam=' + t + '&token=&lang=zh_CN'
    data = {

        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': t,
        'uuid': uuid,
        'action': 'json',
        'type': 'json',
        'token': ''
    }

    
    login_page = session.post(post_url, data=data, headers=headers)
    session.cookies.save()
    print(login_page.text)

    post_url = 'https://mp.weixin.qq.com/misc/safeassistant?1=1&token=&lang=zh_CN'
    data = {

        'token': '',
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': t,
        'uuid': uuid,
        'action': 'get_uuid',
        'uuid': uuid,
        'auth': 'ticket'
    }

    login_page = session.post(post_url, data=data, headers=headers)
    session.cookies.save()
    print(login_page.text)


    post_url = 'https://mp.weixin.qq.com/cgi-bin/securewxverify'
    data = {

        'token': '',
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': t,
        'code': uuid,
        'account': username,
        'auth': 'ticket',
        'operation_seq': '427154860'
    }

    login_page = session.post(post_url, data=data, headers=headers)
    print(login_page.text)
    session.cookies.save()
    res = eval(login_page.text)

    if 'redirect_url' not in res:
        print('请刷二维码')
        sys.exit()

    url = 'https://mp.weixin.qq.com' + res['redirect_url'].replace('\\', '')
    print(url)
    login_page = session.get(url, headers=headers)
    # print(login_page.text)

    global token
    pattern = r'token=([^&=]*)'
    token = re.findall(pattern, url)
    token = token[0]
    print(token)

    # post_url = 'https://mp.weixin.qq.com/cgi-bin/uploadimg2cdn?lang=zh_CN&token=' + token
    # print(post_url)
    # data = {

    #     'imgurl': img_url,
    #     't': 'jax-editor-upload-img'
    # }

    # login_page = session.post(post_url, data=data, headers=headers)
    # print(login_page.text)

try:
    input = raw_input
except:
    pass

def inital():

    # if mpwx_token != '':
    #     token = mpwx_token
    #     mpwx_session = mpwx_session
    #     return False

    print('init mpwx')
    # return False

    # 使用登录cookie信息
    session.cookies = cookielib.LWPCookieJar(filename='cookies_mpwx')

    try:
        session.cookies.load(ignore_discard=True)
    except:
        print("Cookie 未能加载")

    login(username, password)

    return False

def upload_img(img_file_path):

    pattern = r'/([^/]*)$'
    img_file_name = re.findall(pattern, img_file_path)
    img_file_name = img_file_name[0]
    img_url = 'http://upload-images.jianshu.io/upload_images/' + img_file_name + '?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240'
    print(img_url)

    # print(token)    
    post_url = 'https://mp.weixin.qq.com/cgi-bin/uploadimg2cdn?lang=zh_CN&token=' + token
    # print(post_url)
    data = {

        'imgurl': img_url,
        't': 'jax-editor-upload-img'
    }

    login_page = session.post(post_url, data=data, headers=headers)
    print(login_page.text)
    res = eval(login_page.text)
    url = res['url'].replace('\\', '')
    time.sleep(0.1)


    return url

def get_img_file_new_url(file_parent_path, folder):

    file_pre = file_parent_path + os.path.sep + folder + os.path.sep

    img_file_new_url = {}
    img_files = init.listdir(file_pre + 'img')
    for i in range(0, len(img_files)):
        img_file_path = file_pre + 'img' + os.path.sep + img_files[i]
        img_file_new_url[img_files[i]] = upload_img(img_file_path)
        print(img_file_new_url[img_files[i]])

    # print(img_file_new_url)
    return img_file_new_url

def get_qsj_cover(file_parent_path, qsj_folder):
    
    qsj_cover = {}
    qsj_cover['folder'] = qsj_folder

    index_md_path = file_parent_path + os.sep + 'tmp' + os.sep + qsj_folder + os.sep + 'index.md'
    index_md_file = open(index_md_path, 'r', encoding='utf-8')
    file_md_content = index_md_file.read()
    index_md_file.close()

    pattern = r'\!\[\]\(([^\(\)]*?)\)'
    cover_url = re.findall(pattern, file_md_content)

    # if len(cover_url) == 1:
    #     cover_url = cover_url[0]
    # elif len(cover_url) >= 2:
    #     cover_url = cover_url[1]
    cover_url = cover_url[len(cover_url) - 1]


    qsj_cover['cover_url'] = upload_img(cover_url)

    return qsj_cover

def pub(file_parent_path, folder, qsj_folder_arr, url):

    inital()
    img_file_new_url = get_img_file_new_url(file_parent_path, folder)
    init.get_folder_imgs(file_parent_path, folder, img_file_new_url, 'mpwx')

    qsj_cover_arr = []
    print(qsj_folder_arr)

    for i in range(0, len(qsj_folder_arr)):
        img_file_new_url = get_img_file_new_url(file_parent_path + os.path.sep + 'tmp', qsj_folder_arr[i]['folder'])
        init.get_folder_imgs(file_parent_path + os.path.sep + 'tmp', qsj_folder_arr[i]['folder'], img_file_new_url, 'mpwx')
        qsj_cover = get_qsj_cover(file_parent_path, qsj_folder_arr[i]['folder'])
        qsj_cover_arr.append(qsj_cover)


    t = str(int(time.time() * 1000))

    title = re.sub(r'_[^_]*_', '.', folder)

    file_pre = file_parent_path + os.path.sep + folder + os.path.sep
    file_html_path = file_pre + 'index_mpwx.html'
    print(file_html_path)

    # 读取index.md
    index_html_file = open(file_html_path, 'r', encoding='utf-8')
    file_html_content = index_html_file.read()
    index_html_file.close()

    print(token)

    post_url = 'https://mp.weixin.qq.com/cgi-bin/operate_appmsg?t=ajax-response&sub=create&type=10&token=' + token + '&lang=zh_CN'

    mpwx_cover_url = upload_img(init.cover['origin_file_path'])
    
    print(init.cover['origin_file_path'])
    file_html_content = file_html_content + add_qr_html()
    file_html_content = re.sub(r'[\n]', '', file_html_content)
    file_html_content = re.sub(r'<p>', '<p style="margin-top: 20px; margin-bottom: 20px;">', file_html_content)
    
    print(file_html_content)
    data = {

        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': t,
        'AppMsgId': '',
        'count': (len(qsj_folder_arr) + 1),
        'title0': title,
        'content0': file_html_content,
        'digest0': '',
        'author0': '喵爸',
        'fileid0': '',
        'cdn_url0': mpwx_cover_url,
        'music_id0': '',
        'video_id0': '',
        'show_cover_pic0': '0',
        'shortvideofileid0': '',
        'vid_type0': '',
        'copyright_type0': '0',
        'need_open_comment0': '1',
        'only_fans_can_comment0': '0',
        'sourceurl0': url,
        'fee0': '0'

    }

    for i in range(0, len(qsj_folder_arr)):

        qsj_file_pre = file_parent_path + os.path.sep + 'tmp' + os.path.sep + qsj_folder_arr[i]['folder'] + os.path.sep
        qsj_file_html_path = qsj_file_pre + 'index_mpwx.html'
        qsj_index_html_file = open(qsj_file_html_path, 'r', encoding='utf-8')
        qsj_file_html_content = qsj_index_html_file.read()
        qsj_index_html_file.close()
        qsj_file_html_content = re.sub(r'[\n]', '', qsj_file_html_content)
        qsj_file_html_content = re.sub(r'<p>', '<p style="margin-top: 20px; margin-bottom: 20px;">', qsj_file_html_content)

        num = str(i + 1)
        data['title' + num] = '喵妈 | ' + qsj_folder_arr[i]['folder']
        data['content' + num] = qsj_file_html_content
        data['author' + num] = '喵妈'
        data['cdn_url' + num] = qsj_cover_arr[i]['cover_url']


    # print(data)


    print(post_url)
    print(data)
    login_page = session.post(post_url, data=data, headers=headers);
    session.cookies.save()

    print(login_page.text)

def add_qr_html():

    html = '<p><img src="https://mmbiz.qlogo.cn/mmbiz/uDI3FLln00YxQTVXs3RfvviaogRjYFB6ejf6pB2Xwz0mibybuwV65maDAhWzOGQhPQWIIzc0ObjHiaGk0uC1ia9I2A/0?wx_fmt=jpeg"></p>'

    return html







