from django.core.cache import cache
from django.http import HttpRequest,JsonResponse
from django.shortcuts import render, redirect
import requests

from common.stat import OK, VCODE_ERR, AVILD_VCODE, ACCESS_TOKEN_ERR, USER_INFO_ERR, USER_DATA_ERR, PROFILE_DATA_ERR
from libs.http import render_json
from user.models import User
from common import keys, stat
from swiper import cfg
from swiper.cfg import WB_AUTH_URL
from user import logics
# Create your views here.
from user.forms import UserForm, ProfileForm
from user.models import User

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
        # 发送成功返回OK状态码:考虑如何与用户返回数据,采用Json返回;
        # return JsonResponse({
        #     'code':stat.OK,
        #     'data':None
        # })
        return render_json(data=None,code=OK)
    else:
        # 失败返回VCODE_ERR状态码
        # return JsonResponse({
        #     'code':stat.VCODE_ERR,
        #     'data':None
        # })
        return render_json(data=None, code=VCODE_ERR)

def check_vcode(request:HttpRequest):
    '''进行验证并且进行登录注册'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')# 存在用户未提交vcode状态;
    # 先获取缓存,查看
    cached_vcode = cache.get(keys.VCODE_KEY % phonenum)
    # 存在用户未提交vcode状态解决方案:vcode\cache_vcode为空并且相等;
    if vcode and cached_vcode and vcode == cached_vcode:
        # 进行登录或者注册操作,需要判断是否注册过,或者判断用户是否已在登录状态
        # 根据查询用户判断登录或者注册操作
        try:
            # 查询用户,如果用户没有注册,需要进行判断
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
        # 返回时以JSON格式返回,考虑返回信息包括哪些内容,如何封装后使用
        # An HTTP response class that consumes data to be serialized to JSON
        # 默认情况下，JsonResponse的传入参数是个字典类型
        # return JsonResponse({
        #     'code':stat.OK,
        #     'data':user.to_dict()
        # })
        return render_json(data=user.to_dict(), code=OK)
    else:
        # 如果存在null,则返回code代码1001
        # return JsonResponse({
        #     # 验证码无效,返回AVILD_VCODE状态码
        #     'code':stat.AVILD_VCODE,
        #     'data':None
        # })
        return render_json(data=None, code=AVILD_VCODE)

def wb_auth(request):
    '''用户授权页'''

    return redirect(cfg.WB_AUTH_URL)


def wb_callback(request):
    '''
        微博回调接口:
            考虑需要哪些东西:
                (1)code:用于第二步调用oauth2/access_token接口，获取授权后的access token。
    '''
    # 获取code值
    code = request.GET.get('code')
    access_token,wb_uid = logics.get_access_token(code)
    # 判断回调值信息,如果没值,返回标志数;有值将调取用户信息
    if not access_token:
        return render_json(data=None, code=ACCESS_TOKEN_ERR)
    # 获取用户信息
    user_info = logics.get_user_info(access_token,wb_uid)
    if not user_info:
        # 没值返回标志码
        return render_json(data=None, code=USER_INFO_ERR)
    # 执行登录或者注册操作
    try:
        # 基于唯一表示phonenum来查询用户信息
        user = User.objects.get(phonenum=user_info['phonenum'])
    except User.DoesNotExist:
        # 没有该用户,进行注册,"命名关键字形参"
        user = User.objects.create(**user_info)
    # 将session信息通过uid进行保存至服务器,保存的原因在于保留会话
    request.session['uid'] = user.id
    # 默认情况下，JsonResponse的传入参数是个字典类型
    return render_json(data=user.to_dict(), code=OK)


def get_profile(request:HttpRequest):
    '''获取用户资料'''
    user = request.user
    # request对象,新增user属性
    profile_data = user.profile.to_dict()
    return render_json(data=profile_data, code=OK)

def set_profile(request):
    '''
        修改个人资料
            考虑修改什么?
                基础上,request.POST.get('key')将所有的字段进行修改;
                缺点:过于繁琐,不易整理,没有数据检查和清洗过程;
            优化:使用form表单进行操作;[forms模块]
            Django提供类Form来处理提交form表单信息,并与模型进行绑定
    '''
    user_form = UserForm(request.POST)
    profile_form = ProfileForm(request.POST)

    # 获取form表单信息之后,查看form字段是否合法
    if not user_form.is_valid():
        # 用户信息提交有错误
        return render_json(data=None, code=USER_DATA_ERR)
    if not profile_form.is_valid():
        # 交友信息提交有错误
        return render_json(data=None, code=PROFILE_DATA_ERR)
    # form表单信息合法之后,调用clean_data()方法
    # 保存用户的信息
    user = request.user
    # 字典类型的更新数据操作
    # user_form.cleaned_data:查看form对象信息,字典格式
    user.__dict__.update(user_form.cleaned_data)
    #save()方法。
    # 这个方法根据表单绑定的数据创建并保存数据库对象。 ModelForm的子类可以接受
    # 现有的模型实例作为关键字参数instance；如果提供此功能，则save()将更新该实例。
    # 如果没有提供，save() 将创建模型的一个新实例
    user.save()
    # 保存交友资料的数据
    user.profile.__dict__.update(profile_form.cleaned_data)
    return render_json()








