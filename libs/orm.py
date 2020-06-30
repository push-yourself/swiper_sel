from datetime import datetime, date

from common.keys import MODEL_KEY
from libs.cache import  rds
from django.db.models import query
from django.db.models import Model
# 动态增加缓存处理
# 对get进行封装
def get(self,*args,**kwargs):# 保留原有参数
    '''带缓存处理的objects.get方法'''
    # 从缓存中获取数据
    # 获取类名
    # self相当于User.objects
    # self.model = User.objects.model
    # 判断如果是别的缓存
    pk = kwargs.get('pk') or kwargs.get('id')
    if pk is not None:
        key = MODEL_KEY %(self.model.__class__.__name__,pk)
        # 从缓存中取出数据
        model_obj = rds.get(key)
        # 检查model本身的类型
        if isinstance(model_obj,self.model):
            print('从缓存中获取 Model')
            return model_obj
    # 缓存没有,从数据库取出
    model_obj = self._get(*args,**kwargs)
    print('从数据库中获取 Model')
    # 将取出的数据写入缓存
    key = MODEL_KEY % (self.model.__name__,model_obj.pk)
    print('存储至缓存')
    rds.set(key,model_obj)
    return model_obj

# 对save()方法的封装,注意create()也是通过save()进行保存
def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
    # 使用原来save函数写入数据库
    self._save(force_insert,force_update,using,update_fields)
    # 将Model对象保存至缓存
    # self 相当于user,获取类名
    key = MODEL_KEY % (self.__class__.__name__,self.pk)
    rds.set(key,self)

def to_dict(self,*ignore_fields):
    '''将model_obj封装为一个字典'''
    attr_dict = {}
    # 遍历属性
    for field in self.__class__._meta.fields:
        key = field.attrname
        # 如果key在其中的话,则跳过
        if key in ignore_fields:
            continue
        value = getattr(self,key)
        # 如果存在date\datetime的类型,对其进行强转;
        if isinstance(value,(date,datetime)):
            value = str(value)
        attr_dict[key] = value
    return attr_dict

# 动态操作数据:Monkey_Patch的方式操作底层源码
def patch_orm():
    '''通过Monkey_Patch的方式增加缓存'''
    # 为了不覆盖原有get方法,对原有get方法进行重命名操作
    query.QuerySet._get = query.QuerySet.get
    query.QuerySet.get = get
    # 替换save方法
    Model._save = Model.save
    Model.save = save

    # Model中的to_dict方法进行封装
    Model.to_dict = to_dict


