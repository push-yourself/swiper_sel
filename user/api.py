from django.http import HttpRequest,JsonResponse
from django.shortcuts import render
import requests
from user import logics
# Create your views here.

'''
GET:获取数据,一般对服务器的数据没有修改;
POST:创建或者修改数据,
PUT:强调需要修改服务器上的数据;
DELETE:删除服务器上的数据;
reuqest.GET/POST/COOKIES/session
request.META['HTTP_USER_AGENT']  查找user_agent
'''


def get_vcode(request:HttpRequest):
    '''获取短信验证码'''
    #1.获取用户参数:请求
    #2.GET与POST的使用场景
    # 获取用户手机号
    phonenum = request.GET.get("phonenum")
    # 发送验证码,并检查是否发送成功:
    if logics.send_vcode(phonenum):
        return JsonResponse({
            'code':0,
            'data':None
        })
    else:
        return JsonResponse({
            'code':0,
            'data':None
        })







def check_vcode(request):
    '''进行验证并且进行登录注册'''







