import os
import random

import requests

from common import keys
from libs.qn_cloud import upload_to_qn
from swiper import cfg
from django.core.cache import cache
import logging
from tasks import celery_app

inf_logs = logging.getLogger('inf')


def gen_randcode(length: int) -> str:
    '''产生指定长度的随机码'''
    # 方式1:
    # for循环
    # s = ''
    # for i in range(length):
    #     s +=str(random.randint(9))
    # 方式2:使用列表生成字符串,减少内存消耗,一次内存生成
    list_char = [str(random.randint(0, 9)) for i in range(length)]
    return "".join(list_char)


def send_vcode(phone):
    # 随机生成验证码
    vcode = gen_randcode(6)
    # print('验证码:',vcode)
    inf_logs.info('验证码:%s' % vcode)
    # 使用copy()方法实现与普通根据键进行使用;
    # [原型模式]:在配置文件中copy出一份进行修改,而不去处理原有配置文件;

    # 通过Django缓存保存验证码,
    # 通过标识来设计Key值操作,确定起数据的唯一性;表示不同的操作类型;
    # 由于Key比较零散,可将不同的Key进行集中操作,作为全局使用;
    # 并设置验证码的过期时间;并且放入局部缓存
    # cache.set('my_key', 'myvalue', 30)#参数设置:Key类型  value 缓存时间 默认值为settings.py CACHES对应配置的TIMEOUT
    cache.set(keys.VCODE_KEY % phone, vcode, 180)
    # 不修改全局变量的前提下,对复制出来的东西进行操作
    args = cfg.YZX_ARGS.copy()
    # 通过云之讯接口进行修改配置
    args['mobile'] = phone
    args['param'] = vcode
    # 在通过requests.post()进行POST请求时，传入报文的参数有两个，一个是data，一个是json
    # 向云之讯服务器提交信息
    # POST提交信息时,先告知服务器,再发送数据,等待服务器回复200响应码
    response = requests.post(cfg.YZX_API, json=args)
    # 检查最终的返回值
    if response.status_code == 200:
        result = response.json()
        if result['code'] == '000000':  # 云之讯返回值判断:000000为OK
            return True
    return False


def get_access_token(code):
    '''获取微博的授权令牌'''
    # 从全局变量处复制一套参数配置出来
    args = cfg.WB_ACCESS_TOKEN_ARGS.copy()
    args['code'] = code
    # 向微博的授权服务器上提交接口地址与参数信息
    # 微博服务端需要接收配置信息以及回调接口
    response = requests.post(cfg.WB_ACCESS_TOKEN_API, data=args)
    # 检查最终的返回值,若存在,查看提交状态
    if response.status_code == 200:
        result = response.json()
        # 回调函数的返回值格式:
        # {
        # "access_token": "ACCESS_TOKEN",
        # "expires_in": 1234,
        # "remind_in": "798114",
        # "uid": "12341234"
        # }
        access_token = result['access_token']
        wb_uid = result['uid']
        return access_token, wb_uid
    return None, None


def get_user_info(access_token, wb_uid):
    # 将用户展示参数信息复制一份用作处理
    args = cfg.WB_USER_SHOW_ARGS.copy()
    args['access_token'] = access_token
    args['uid'] = wb_uid
    # 从微博服务器上获取用户信息
    response = requests.get(cfg.WB_USER_SHOW, params=args)
    # 检查最终的返回值
    if response.status_code == 200:
        result = response.json()
        # 将返回信息匹配orm中用户模型[需要判断哪些是我们需要的信息]
        user_info = {
            'phonenum': 'WB_%s' % wb_uid,
            'nickname': result['screen_name'],
            'sex': 'female' if result['gender'] == 'f' else 'male',
            'avatar': result['avatar_hd'],
            'location': result['location'].split(' ')[0],
        }
        return user_info
    return None


def save_upload_file(user, upload_avatar):
    '''临时保存上传的头像信息'''
    # 命名文件名,为区分不同用户
    filename = 'Avatar-%s' % user.id
    # 保存文件路径
    filepath = '/tmp/%s'%filename
    # fp指的是文件指针file point
    # 按照块进行处理
    with open(filepath,'wb') as fp:
        for chunk in upload_avatar.chunks():
            fp.write(chunk)
    return filename,filepath

# 封装任务，用Celery上传至七牛云
@celery_app.task
def handle_avatar(user,upload_avatar):
    # 考虑用户上传之后，无感知，取做其他的事情，采用异步进行操作
    # 上传至本地(IO操作存在耗时严重)
    filename,filepath = save_upload_file(user,upload_avatar)
    # 上传至七牛云(网络IO耗时比较严重)
    avatar_url = upload_to_qn(filename,filepath)

    # 保存avatar_url,至数据库
    user.avatar = avatar_url
    user.save()
    # 保存后删除;删除本地的临时文件
    os.remove(filepath)