# Generated by Django 2.2.12 on 2020-06-26 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dating_sex', models.CharField(choices=[('male', '男性'), ('female', '女性')], max_length=8, verbose_name='匹配的性别')),
                ('dating_location', models.CharField(choices=[('北京', '北京'), ('上海', '上海'), ('广州', '广州'), ('深圳', '深圳')], max_length=20, verbose_name='目标城市')),
                ('min_dating_age', models.IntegerField(default=18, verbose_name='最小交友年龄')),
                ('max_dating_age', models.IntegerField(default=50, verbose_name='最大交友年龄')),
                ('min_distance', models.IntegerField(default=1, verbose_name='最小查找范围')),
                ('max_distance', models.IntegerField(default=30, verbose_name='最大查找范围')),
                ('vibration', models.BooleanField(default=True, verbose_name='开启震动')),
                ('only_matched', models.BooleanField(default=True, verbose_name='只让匹配的人看我的相册')),
                ('auto_play', models.BooleanField(default=True, verbose_name='自动播放视频')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonenum', models.CharField(max_length=15, unique=True, verbose_name='手机号')),
                ('nickname', models.CharField(max_length=20, verbose_name='昵称')),
                ('sex', models.CharField(choices=[('male', '男性'), ('female', '女性')], max_length=8, verbose_name='性别')),
                ('birt_day', models.DateField(default='1990-1-1', verbose_name='出生日')),
                ('avatar', models.CharField(max_length=256, verbose_name='个人形象')),
                ('location', models.CharField(choices=[('北京', '北京'), ('上海', '上海'), ('广州', '广州'), ('深圳', '深圳')], max_length=20, verbose_name='常居地')),
                ('vip_id', models.IntegerField(default=1, verbose_name='用户对应的VIP')),
                ('vip_expired', models.DateTimeField(default='2000-1-1', verbose_name='会员过期时间')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
