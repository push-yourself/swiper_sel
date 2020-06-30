import datetime
import time

from django.http import response

from common import keys, stat
from libs.cache import rds
from social.models import Swiper, Friend
from swiper import cfg
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
    # 取出超级喜欢过自己,但是没有被自己滑动过的用户的ID[ORM取出]
    # who_superlike_me =  Swiper.objects.filter(sid=user.id,stype='superlike')\
    #                                     .exclude(uid__in=sid_list)\
    #                                     .values_list('uid',flat=True)

    # 使用redis获取
    # superliked_me_id_list = rds.zrange(keys.SUPERLIKED_KEY % user.id,0,19)
    superliked_me_id_list = [int(uid) for uid in rds.zrange(keys.SUPERLIKED_KEY % user.id, 0, 19)]
    superliked_me_users = User.objects.filter(id__in=superliked_me_id_list)
    # 当不足20个的时候:
    other_count = 20 - len(superliked_me_users)
    if other_count > 0:
        # 注意:对于滑动过的用户ID在sid_ist中的用户,取切片
        # 筛选出匹配的用户,根据性别,城市位置,以及最早出生和最晚出生；
        other_users = User.objects.filter(
            sex=profile.dating_sex,
            location=profile.dating_location,
            birthday__gte=earliest_birthday,
            birthday__lte=latest_birthday
        ).exclude(id__in=sid_list)[:20]
        # 不足20,则将取出的和超级喜欢的拼凑(Set的运算操作)
        users = superliked_me_users | other_users
    else:
        users = superliked_me_users
    return users


def like_someone(user, sid):
    '''喜欢某人'''
    # 添加滑动记录,由于滑动方式多样,对滑动进行封装
    Swiper.swiper(user.id, sid, 'like')
    # 检查对方是否喜欢自己(对方喜欢自己,需要注意先后)
    if Swiper.is_liked(sid, user.id):
        # 如果对方喜欢自己,则匹配成好友
        Friend.make_friends(user.id, sid)
        return True
    else:
        return False


def superlike_someone(user, sid):
    '''超级喜欢
       自己超级喜欢过对方,则一定会出现在对方的推荐列表中
    '''
    # 使用有序集合存储[注意与列表,集合之间的区别]
    # 将自己的ID写入对方的优先推荐队列
    Swiper.swiper(user.id, sid, 'superlike')
    rds.zadd(keys.SUPERLIKED_KEY % sid, user.id, time.time())
    # 检查对方是否喜欢自己(对方喜欢自己,需要注意先后)
    if Swiper.is_liked(sid, user.id):
        # 如果对方超级喜欢自己,则匹配成好友
        Friend.make_friends(user.id, sid)
        rds.zrem(keys.SUPERLIKED_KEY % user.id, sid)
        return True
    else:
        return False


def dislike_someone(user, sid):
    '''不喜欢某人'''
    Swiper.swiper(user.id, sid, 'dislike')
    # 如果对方超级喜欢过你，将对方从你的超级喜欢列表中删除
    rds.zrem(keys.SUPERLIKED_KEY % user.id, sid)


def rewind_swiped(user):
    '''
    1.获取反悔次数      ---存储位置
    2.返回一次滑动记录    ---              找到最近一次的滑动记录;[返回的记录只能为5min之内]
    3.每天允许反悔3次    ---               需要对当天返回次数进行记录;并作出检查确定哪一次是最近一次;
    4.返回记录只能是5min以内   ---          找到最近的滑动记录,检查反悔记录是否为5mins以内,判断当前时间与滑动时的时间操作；

    5.检查上一次滑动是否匹配为好友,如果是,则需要先删除好友记录;
    6.如果上一次是超级喜欢,将自身uid从对方的右滑推荐队列中删除

    7.删除滑动记录；     ---               需要更新滑动记录
    '''
    # 获取今天的反悔次数
    # 默认0次反悔次数,参数最好写入配置文件；
    rewind_times = rds.get(keys.REWWIND_KEY % user.id, 0)
    # 检查是否达到限制次数
    if rewind_times >= cfg.DAILY_REWIND:
        raise stat.RewindLimit
    # 根据时间找到最近的一次的滑动记录:filter的内容无顺序;
    # 取最近的一次滑动的方法:last(),latest()对比区别
    latest_swiped = Swiper.objects.filter(uid=user.id).latest('stime')
    # 检查返回记录在五分钟以内:当前时间与滑动时间的差值
    now = datetime.datetime.now()
    if (now-latest_swiped.stime).total_seconds() >= cfg.REWIND_TIMEOUT:
        raise stat.RewindTimeout

    # 检查上一次滑动是否匹配成好友
    if latest_swiped.stype in ['like','superlike']:
        # 如果是好友,删除好友关系
        Friend.break_off(user.id,latest_swiped.sid)
        # 如果上一次超级喜欢,将自身uid从对方的优先推荐队列中删除
        if latest_swiped.stype == 'superlike':
            rds.zrem(keys.SUPERLIKED_KEY % latest_swiped.sid,user.id)

    # 如果反悔的话,需要还原用户的滑动积分
    score = -cfg.SWIPE_SCORE[latest_swiped.stype]# 查找反悔的滑动积分
    rds.zincrby(keys.HOT_RANK_KEY,score,latest_swiped.sid)
    # 删除滑动记录
    latest_swiped.delete()
    # 更新当天的滑动次数
    rds.set(keys.REWWIND_KEY % user.id,rewind_times+1)
    # 更新过期过期时间(次日零点过期),需要计算过期时间,由于date在月末临界点,不够安全,采用timedelta()
    next_zero = datetime.datetime(now.year,now.month,now.day) + datetime.timedelta()
    remain_seconds = next_zero - now
    rds.set(keys.REWWIND_KEY % user.id,rewind_times + 1,remain_seconds)


def set_score(uid,stype):
    # def demo(request,*args,**kwargs):
    #     '''调整用户积分'''
    #     # 先执行原函数
    #     # 调用原函数
    #     response = view_func(request, *args, **kwargs)
    #     # 获取函数名
    # stype = view_func.__name__
    #获取积分
    score = cfg.SWIPE_SCORE[stype]
    # 获取被滑动用户id
    # sid = int(request.POST.get('sid'))
    rds.zincrby(keys.HOT_RANK_KEY,score,uid)
    return response
    # return demo

def top_n(num):
    '''取出排行榜前N的用户信息'''
    # 从Redis中取出排行数据
    rank_data = rds.zrevrange(keys.HOT_RANK_KEY,0,num-1,withscores=True)
    # 对数据进行清洗，转为int
    cleaned = [[int(uid),int(score)] for uid,score in rank_data]
    # uid_list = [item[0] for item in cleaned]
    # 根据用户批量提取用户,[推荐下面的推倒方式使用](取法1)
    uid_list = [uid for uid,_ in cleaned]
    users = User.objects.filter(id__in=uid_list)# in方法排行会导致原有顺序发生错乱，
    # 因此可以使用sorted方法根据uid_list的索引进行排序
    users = sorted(users,key=lambda user:uid_list.index(user.id))

    ignore_fields = ['phonenum','sex','birthday','location','vip_id','vip_expired']
    # 组装成之前设定的返回值
    result = {}
    for idx,user in enumerate(users):
        score = cleaned[idx][1]
        u_dict = user.to_dict(*ignore_fields)
        u_dict['score'] = score
        # users的排序是根据排名而来，
        result[idx+1] = u_dict
    return result
    #(取法2：)
    # User.objects.in_bulk(uid_list)

