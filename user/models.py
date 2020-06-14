from django.db import models

# Create your models here.
class User(models.Model):
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
    avatar = models.CharField(verbose_name='个人形象',max_length=256)
    location = models.CharField(verbose_name='常居地',max_length=20,choices=LOCATION)
