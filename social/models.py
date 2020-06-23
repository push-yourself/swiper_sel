from django.db import models

# Create your models here.
from django.db.models import Q

from common import stat


class Swiper(models.Model):
    '''
        滑动记录
        考虑滑动记录表中,需要哪些字段:
            (1)自己的用户ID ;
            (2)被滑动的用户ID ;
            (3)滑动的记录类型;
            (4)当时滑动的时间;
            ...
    '''
    STYPE = (
        ('like','喜歡'),
        ('superlike','超级喜欢'),
        ('dislike','不喜欢'),
    )
    objects = models.Manager()

    uid = models.IntegerField(verbose_name='滑动的用户ID')
    sid = models.IntegerField(verbose_name='被滑动的ID')
    stype = models.CharField(max_length=10,verbose_name='滑動窗口的記錄類型',choices=STYPE)
    stime = models.DateField(auto_now_add=True,verbose_name='滑动时时间')

    # 创建方法.需要被各个实例
    @classmethod
    def is_liked(cls,uid,sid):
        '''
            检查是否喜欢过某人:
                1.喜欢包含'喜欢'和'超级喜欢'
                2.需要在滑动记录表中去过滤自己ID以及滑动的用户ID并且滑动类型在于喜欢|超级喜欢,
                  判断是否存在
        '''
        return cls.objects.filter(uid=uid,sid=sid,
                                  stype__in=['like', 'superlike']).exists()

    @classmethod
    def swiper(cls, uid, sid, stype):
        '''
            判断滑动操作:
            1.检查滑动操作是否在滑动类型中,不在抛出错误;
            2.对于判断滑动的用户是否为已经划过的用户,如果是,抛出滑动重复错误
        '''
        if stype not in ['like', 'superlike', 'display']:
            raise stat.SwipeTypeErr
        # 判断好友关系表中是否存在当前用户
        if cls.objects.filter(uid=uid, sid=sid).exists():
            raise stat.SwipeRepeatErr
        return cls.objects.create(uid=uid, sid=sid, stype=stype)

    @classmethod
    def who_liked_me(cls,uid):
        return cls.objects.filter(sid=uid,stype__in=['like', 'superlike'])\
            .values_list('uid',flat=True)





class Friend(models.Model):
    '''
        好友关系表:
            考虑字段:
                1.自己的user_id
                2.好友的user_id
    '''
    objects = models.Manager()
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    @classmethod
    def make_friends(cls,uid,sid):
        '''创建好友关系'''
        uid1,uid2 = (sid,uid) if uid > sid else (uid,sid)
        # 判断是否为好友关系,没有则创建;用意在于防止用户频繁的刷新操作;
        # 防止数据库中出现相同记录；
        cls.objects.get_or_create(uid1=uid1,uid2=uid2)

    @classmethod
    def friend_ids(cls,uid):
        '''查询自己所有好友ID '''
        condition = Q(uid1=uid) | Q(uid2=uid)
        friend_relations = cls.objects.filter(uid1=condition)
        uid_list = []
        for relation in friend_relations:
            friend_id = relation.uid2 if relation.uid1 == uid else relation.uid1
            uid_list.append(friend_id)
        return uid_list