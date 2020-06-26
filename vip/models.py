from django.db import models

# Create your models here.

# 注意:表与表之间尽可能不要使用外键;
# 对于表设计时,不能添加为添加字段来去扩充;
# 单行的内容也有一定的限制,不利于扩充
class Vip(models.Model):
    '''会员表'''
    '''
        name        leve        price    days
        ------------------------------------
         铜牌          1          10      30
    '''
    objects = models.Manager()
    name = models.CharField(max_length=10,unique=True,verbose_name='会员名称')
    level = models.IntegerField(default=0,verbose_name='会员等级')
    price = models.FloatField(default=0.0,verbose_name='当前会员对应的价格')
    days = models.IntegerField(default=0,verbose_name='购买的天数')

    def has_perm(self,per_name):
        '''检查当前VIP是否具有某个权限'''
        #only():只获取id
        perm = Permission.objects.filter(name=per_name).only('id').first()
        VipPermRelation.objects.filter(vip_id=self.id,perm_id=perm.id).exists()


class Permission(models.Model):
    '''权限表'''
    objects = models.Manager()
    name = models.CharField(max_length=20,unique=True,verbose_name='权限名称')
    desc = models.TextField(verbose_name='权限描述')

class VipPermRelation(models.Model):
    '''会员和权限关系表'''
    '''
    会员      权限
    -------------
    一级权限    超级喜欢
    二级权限    返回三次
    二级权限    ....
    三级权限    ....
    '''
    objects = models.Manager()
    vip_id = models.IntegerField(verbose_name='会员ID')
    perm_id = models.IntegerField(verbose_name='权限的ID')


# 如何确定用户\VIP之间的关系:首先明确1:N关系 ---
# 一个用户可对一个VIP权限,一个VIP权限可以对应多个用户










