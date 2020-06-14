from django.core.cache import cache
from django.http import HttpRequest,JsonResponse
from django.shortcuts import render
import requests

from common import keys, stat
from user import logics
# Create your views here.
from user.models import User

'''
GET:获取数据,一般对服务器的数据没有修改;
POST:创建或者修改数据,
PUT:强调需要修改服务器上的数据;
DELETE:删除服务器上的数据;
reuqest.GET/POST/COOKIES/session
request.META['HTTP_USER_AGENT']  查找user_agent
'''


def get_vcode(request:HttpRequest):
    '''
    获取短信验证码
    '''
    #1.获取用户参数:请求
    #2.GET与POST的使用场景
    # 获取用户手机号
    phonenum = request.GET.get("phonenum")
    # 发送验证码,并检查是否发送成功:
    if logics.send_vcode(phonenum):
        # 发送成功返回OK状态码
        return JsonResponse({
            'code':stat.OK,
            'data':None
        })
    else:
        # 失败返回VCODE_ERR状态码
        return JsonResponse({
            'code':stat.VCODE_ERR,
            'data':None
        })


def check_vcode(request:HttpRequest):
    '''进行验证并且进行登录注册'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')# 存在用户未提交vcode状态;

    cached_vcode = cache.get(keys.VCODE_KEY % phonenum)
    # 存在用户未提交vcode状态解决方案:vcode\cache_vcode为空并且相等;
    if vcode and cached_vcode and vcode == cached_vcode:
        # 进行登录或者注册操作,需要判断是否注册过,或者判断用户是否已在登录状态
        # 查询用户,如果用户没有注册,需要进行判断
        # 根据查询用户判断登录或者注册操作
        try:
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            # 如果不存在,则需要进行注册
            user = User.objects.create(
                phonenum = phonenum,
                nickname = phonenum,# 可随机生成,现在昵称作为手机号
            )
        # 登录操作,将浏览器端的信息记录下来,通过session进行保存;
        # 记录用户ID,并将用户信息传给服务端
        request.session['uid'] = user.id
        return JsonResponse({
            'code':stat.OK,
            'data':user.to_dict()
        })
    else:
        # 如果存在null,则返回code代码1001
        return JsonResponse({
            # 验证码无效,返回AVILD_VCODE状态码
            'code':stat.AVILD_VCODE,
            'data':None
        })







