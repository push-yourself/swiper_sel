
import random

import requests

from swiper import cfg


def gen_randcode(length:int)->str:
    '''产生指定长度的随机码'''
    # for循环
    # s = ''
    # for i in range(length):
    #     s +=str(random.randint(9))
    # 方式2:使用列表生成字符串,减少内存消耗,一次内存生成
    list_char = [str(random.randint(0,9)) for i in range(length)]
    return "".join(list_char)

# 测试
# print(gen_randcode(5))


def send_vcode(phone):
    vcode = gen_randcode(6)
    # 使用copy()方法实现与普通根据键进行使用;
    # [原型模式]:在配置文件中copy出一份进行修改,而不去处理原有配置文件;
    args = cfg.YZX_ARGS.copy()
    args['mobile'] = phone
    args['param'] = vcode
    response = requests.post(cfg.YZX_API,json=cfg.YZX_ARGS)
    if response.status_code == 200:
        result = response.json()
        if result['code'] == '000000':
            return True
    return False

