from django.db import models

# Create your models here.
from django.db.models import IntegerField

from vip.models import Vip


class User(models.Model):
    objects = models.Manager()
    SEX = (
        ('male','男性'),
        ('female','女性')
    )

    LOCATION = (
        ('北京','北京'),
        ('上海','上海'),
        ('广州','广州'),
        ('深圳','深圳')
    )
    phonenum = models.CharField(verbose_name='手机号',max_length=15,unique=True)
    nickname = models.CharField(verbose_name='昵称',max_length=20)
    sex = models.CharField(verbose_name='性别',max_length=8,choices=SEX)
    birt_day = models.DateField(verbose_name='出生日',default='1990-1-1')
    # 对于图片存储一般都会存储一个网址;
    avatar = models.CharField(verbose_name='个人形象',max_length=256)
    location = models.CharField(verbose_name='常居地',max_length=20,choices=LOCATION)
    # 对于VIP新增字段
    vip_id = models.IntegerField(default=1, verbose_name='用户对应的VIP')
    vip_expired = models.DateTimeField(default='2000-1-1', verbose_name='会员过期时间')

    class Meta:
        db_table = 'user'

    @property
    def profile(self):
        # 处理方式:
        # 如果user对象没有这个_profile属性,先执行并创建:get_or_create方法的使用;
        if not hasattr(self,'_profile'):
            # 类名.方法()   这种操作需要自行传递对象地址
            self._profile,_ = Profile.objects.get_or_create(id=self.id)
            # 等同于:
            # try:
            #     profile = Profile.objects.get(id=self.id)
            # except Profile.DoesNotExists:
            #     profile = Profile.objects.create(id=self.id)
        return self._profile

    # 在1对多中通过id来实现外键关系
    @property
    def vip(self):
        if not hasattr(self,'_vip'):
            self._vip = Vip.objects.get_or_create(id=self.vip_id)
        return self._vip

    # def to_dict(self):
    #     '''将JSON对象转换为字典格式'''
    #     return {
    #         'id':self.id,
    #         'phonenum':self.phonenum,
    #         'nickname':self.nickname,
    #         'sex':self.sex,
    #         # 注意日期字段是不能够被JSON序列化;因此需要对日期进行字符串转换;
    #         'birthday':str(self.birt_day),
    #         'avatar':self.avatar,
    #         'location':self.location
    #     }

# 注意:在这里执行时第一次执行get_or_create方法即可;
# 关键点在于:方法的属性化
# user = User.objects.get(id = '123')
# user.profile.dating_sex
# user.profile.dating_location
# user.profile.max_distance


class Profile(models.Model):
    '''个人的交友资料'''
    objects = models.Manager()
    dating_sex = models.CharField(max_length=8,choices=User.SEX,verbose_name='匹配的性别')
    dating_location = models.CharField(max_length=20,choices=User.LOCATION,verbose_name='目标城市')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')
    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=30, verbose_name='最大查找范围')

    vibration = models.BooleanField(default=True, verbose_name='开启震动')
    only_matched = models.BooleanField(default=True, verbose_name='只让匹配的人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')

    # def to_dict(self):
    #     '''转换为字典格式'''
    #     return {
    #         'id': self.id,
    #         'dating_sex': self.dating_sex,
    #         'dating_location': self.dating_location,
    #         'min_dating_age': self.min_dating_age,
    #         'max_dating_age': self.max_dating_age,
    #         'min_distance': self.min_distance,
    #         'max_distance': self.max_distance,
    #         'vibration': self.vibration,
    #         'only_matched': self.only_matched,
    #         'auto_play': self.auto_play,
    #     }







