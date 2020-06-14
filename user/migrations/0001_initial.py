# Generated by Django 2.2.12 on 2020-06-14 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
            ],
        ),
    ]
