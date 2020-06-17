import random

import requests

from common import keys
from swiper import cfg

# Django缓存
from django.core.cache import cache


def gen_randcode(length: int) -> str:
    '''产生指定长度的随机码'''
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
    print('验证码:',vcode)
    # 使用copy()方法实现与普通根据键进行使用;
    # [原型模式]:在配置文件中copy出一份进行修改,而不去处理原有配置文件;

    # 通过Django缓存保存验证码,
    # 通过标识来设计Key值操作,确定起数据的唯一性;表示不同的操作类型
    # 由于Key比较零散,可将不同的Key进行集中操作,作为全局使用;
    # 并设置验证码的过期时间;
    cache.set(keys.VCODE_KEY % phone, vcode,180)
    # 不修改全局变量的前提下,对复制出来的东西进行操作
    args = cfg.YZX_ARGS.copy()
    # 通过云之讯接口进行修改配置
    args['mobile'] = phone
    args['param'] = vcode
    # python中的dict类型要转换为json格式的数据需要用到json库
    # <json> = json.dumps(<dict>)
    # <dict> = json.loads(<json>)
    # 在通过requests.post()进行POST请求时，传入报文的参数有两个，一个是data，一个是json
    # 1. requests.post(url, data=json.dumps(data))
    # 2. json参数会自动将字典类型的对象转换为json格式
    # response = requests.post(cfg.YZX_API, json=cfg.YZX_ARGS)
    response = requests.post(cfg.YZX_API, json=args)
    # 判断响应状态码是200
    '''
        常用测试响应方法:
            (1)查看响应状态码:response.status_code
            (2)查看响应内容:response.text
            (3)封装为json格式:response.json()
    '''
    # return response
    # 检查最终的返回值
    if response.status_code == 200:
        result = response.json()
        # print(result['code'])# 105140
        if result['code'] == '000000':
            return True
    return False


def get_access_token(code):
    '''获取微博的授权令牌'''
    # 从全局变量处复制一套参数配置出来
    args = cfg.WB_ACCESS_TOKEN_ARGS.copy()
    args['code'] = code
    # 向微博的授权服务器上提交接口地址与参数信息
    # 微博服务端需要接收配置信息以及回调接口
    response = requests.post(cfg.WB_ACCESS_TOKEN_API,data=args)
    # 检查最终的返回值,若存在,查看提交状态
    if response.status_code == 200:
        result = response.json()
        # 回调函数的返回值
        # {
        # "access_token": "ACCESS_TOKEN",
        # "expires_in": 1234,
        # "remind_in": "798114",
        # "uid": "12341234"
        # }
        access_token = result['access_token']
        wb_uid = result['uid']
        return access_token,wb_uid
    return None,None


def get_user_info(access_token,wb_uid):
    # 将用户展示参数信息复制一份用作处理
    args = cfg.WB_USER_SHOW_ARGS.copy()
    args['access_token'] = access_token
    args['uid'] = wb_uid
    # 从微博服务器上获取用户信息
    response = requests.get(cfg.WB_USER_SHOW,params=args)
    # 检查最终的返回值
    if response.status_code == 200:
        result = response.json()
        # 将返回信息匹配orm中用户模型[需要判断哪些是我们需要的信息]
        user_info = {
            'phonenum':'WB_%s'%wb_uid,
            'nickname':result['screen_name'],
            'sex':'female' if result['gender']=='f' else 'male',
            'avatar':result['avatar_hd'],
            'location':result['location'].split(' ')[0],
        }
        return user_info
    return None






