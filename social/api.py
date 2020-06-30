from django.shortcuts import render

from libs.cache import rds
from libs.http import render_json

# Create your views here.
from social import logics
from social.logics import set_score
from social.models import Swiper, Friend
from user.models import User
from vip.logics import need_permission


def get_rcmd_users(request):
    '''获取推荐用户'''
    users = logics.rcmd(request.user)
    result = [user.to_dict() for user in users]
    return render_json(result)

# @set_score
def like(request):
    '''
        右滑喜欢:
            1.对于出现的对象要先获取ID,目的在于判断;
            2.判断方式需要考虑是否在对方有喜欢自己,如果存在,则用户右滑,则可以建立好友关系;
    '''
    sid = int(request.POST.get('sid' ))
    is_matched = logics.like_someone(request.user,sid)
    logics.set_score(sid,'like')
    # rds.zincrby('xxx',5,sid)# 对于新功能,还是做好使用装饰器来操作
    logics.set_score(sid, 'superlike')
    return render_json({
        'matched':is_matched
    })


# @set_score
def dislike(request):
    '''左滑不喜欢'''
    sid = int(request.POST.get('sid'))
    logics.dislike_someone(request.user, sid)
    logics.set_score(sid, 'dislike')
    return render_json()


# 注意:多层装饰器按照自上而下顺序
@need_permission
# @set_score
def superlike(request):
    '''上划超级喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.superlike_someone(request.user,sid)
    return render_json({
        'matched': is_matched
    })



@need_permission
def rewind(request):
    '''
        后悔:
            接口设计时的一些原则
            1. 客户端传来的任何东西不可信，所有内容都需要验证
            2. 接口的参数和返回值应保持吝啬原则，不要把与接口无关的东西传过去
            3. 服务器能够直接获取的数据，不要由客户端传递
    '''
    logics.rewind_swiped(request.user)
    return render_json()


@need_permission
def who_liked_me(request):
    '''查看谁喜欢我'''
    user_id_list = Swiper.who_liked_me(request.user.id)
    user = User.objects.filter(id__in=user_id_list)
    return render_json(user)

def friend_list(request):
    '''好友列表'''
    friend_id_list = Friend.friend_ids(request.user.id)
    users = User.objects.filter(id__in=friend_id_list)
    result = [user.to_dict() for user in users]
    return render_json(result)

# 展示[前50:注意：考虑可扩展性]的积分排行
#1.考虑数据结构{1:{头像  姓名   得分},2:{}}
def hot_rank(request):
    '''用户积分排行榜'''
    rank_data = {}
    rank_data = logics.top_n(50)
    return render_json(rank_data)

