import datetime

from social.models import Swiper, Friend
from user.models import User

def rcmd(user):
    '''
        推荐可滑动的用户:
        推荐思路:
            (1)考虑推荐的用户的权重:比如年龄范围\地区范围\喜好等(这些字段都可以在用户表中进行添加)
            (2)推荐的用户是否包含已经推荐过的用户信息;

    '''
    profile = user.profile
    # 获取当前时间
    today = datetime.date.today()
    # 最早出生的日期
    earliest_birthday = today - datetime.timedelta(profile.max_dating_age * 365)
    # 最晚出生的日期
    latest_birthday = today - datetime.timedelta(profile.min_dating_age * 365)

    # 取出滑过的用户的ID   flat拼接为一个列表
    sid_list = Swiper.objects.filter(uid=user.id).values_list('sid', flat=True)



    # 筛选出匹配的用户,根据性别,城市位置,以及最早出生和最晚出生；
    # 注意:对于滑动过的用户ID在sid_ist中的用户,取切片
    users = User.objects.filter(
        sex=profile.dating_sex,
        location = profile.dating_location,
        birthday__gte = earliest_birthday,
        birthday__lte = latest_birthday
    ).exclude(id__in = sid_list)[:20]

    return users



def like_someone(user,sid):
    '''喜欢某人'''
    # 添加滑动记录,由于滑动方式多样,对滑动进行封装
    Swiper.swiper(user.id,sid,'like')
    # 检查对方是否喜欢自己(对方喜欢自己,需要注意先后)
    if Swiper.is_liked(sid,user.id):
        # 如果对方喜欢自己,则匹配成好友
        Friend.make_friends(user.id,sid)
        return True
    else:
        return False