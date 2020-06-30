import os

from django.core.cache import cache

from django.http import HttpRequest
from django.shortcuts import render, redirect
from common.stat import *
from libs.http import render_json
from libs.cache import rds
from common import keys
from libs.qn_cloud import upload_to_qn
from swiper import cfg
from user import logics
from user.forms import UserForm, ProfileForm
from user.models import User
import logging


info_logs = logging.getLogger('inf')

# Create your views here.
def get_vcode(request: HttpRequest):
    '''获取短信验证码'''
    # 获取客户端请求GET请求提交的数据
    phonenum = request.GET.get("phonenum", )
    # 发送验证码,并检查是否发送成功:
    if logics.send_vcode(phonenum):
        return render_json(data=None, code=OK)
    else:
        return render_json(data=None, code=VCODE_ERR)


def check_vcode(request: HttpRequest):
    '''进行验证并且进行登录注册'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')  # 存在用户未提交vcode状态;
    # # 从缓存取出验证码cache.get('Key')
    cached_vcode = cache.get(keys.VCODE_KEY % phonenum)
    # 存在用户未提交vcode状态解决方案:vcode\cache_vcode为空并且相等;
    if vcode and cached_vcode and vcode == cached_vcode:
        # 进行登录或者注册操作,需要判断是否注册过,或者判断用户是否已在登录状态
        try:
            # 查询用户,如果用户没有注册,需要进行判断
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            # 如果不存在,则需要进行注册
            user = User.objects.create(
                phonenum=phonenum,
                nickname=phonenum  # 可随机生成,现在昵称作为手机号
            )
        # 记录至日志文件
        info_logs.info('User(%s) login in ' % (user.id))
        # 记录用户ID,并将用户信息传给服务端
        request.session['uid'] = user.id
        return render_json(data=user.to_dict(), code=OK)
    else:
        return render_json(data=None, code=AVILD_VCODE)


def wb_auth(request):
    '''1.用户授权页跳转'''
    return redirect(cfg.WB_AUTH_URL)


def wb_callback(request):
    '''2.微博回调接口'''
    # 获取code值
    code = request.GET.get('code', )
    access_token, wb_uid = logics.get_access_token(code)
    # 判断回调值信息,如果没值,返回标志数;有值将调取用户信息
    if not access_token:
        return render_json(data=None, code=ACCESS_TOKEN_ERR)
    # 回调值存在,需要获取用户信息
    user_info = logics.get_user_info(access_token, wb_uid)
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
    return render_json(data=user.to_dict(), code=OK)


def get_profile(request: HttpRequest):
    '''获取用户资料'''
    # request对象,新增user属性
    # 考虑性能问题:request.user.profile都是需要从磁盘中进行读取
    key = keys.PROFILE_KEY % request.user.id
    profile_data = rds.get(key)
    if profile_data is None:
        # 缓存与数据库的操作
        profile_data = request.user.profile.to_dict()
        # 将取出的数据添加至缓存
        rds.set(key, profile_data)
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
    # save()方法。
    # 这个方法根据表单绑定的数据创建并保存数据库对象。 ModelForm的子类可以接受
    # 现有的模型实例作为关键字参数instance；如果提供此功能，则save()将更新该实例。
    # 如果没有提供，save() 将创建模型的一个新实例
    user.save()
    # 修改缓存(缓存更新的方法)
    key = keys.PROFILE_KEY % request.user.id
    rds.set(key, user.to_dict('vip_id','vip_expired'))

    user.profile.__dict__.update(profile_form.cleaned_data)
    return render_json()


def upload_avatar(request:HttpRequest):
    '''上传个人头像
    '''
    # 获取文件
    avatar = request.FILES.get('avatar')
    logics.handle_avatar.delay(request.user,avatar)
    return render_json()



