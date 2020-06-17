from django import forms
from user.models import User,Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'nickname','sex','birt_day','location'
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'# 取全部属性生成控件
    # 最大最小值无法做出限制
    # 最大最小信息需要逻辑上的控制
    # 层级清洗工作:is_valid()-----clean()-----不同的清洗工作
    # 固定操作:函数名:clean_字段名
    def clean_max_dating_age(self):
        '''
            检查最大交友年龄
        '''
        # 调用父类的清洗方法
        # clean()方法:
        # 返回验证后的数据，这个数据在后面将插入到表单的 cleaned_data 字典中。
        # 在表单子类中调用clean_<fieldname>()方法，其中<fieldname>替换为表单域属性的名称。
        # 验证模型的字段 —— Model.clean_fields()
        # 验证模型的完整性 —— Model.clean()
        # 验证模型的唯一性 —— Model.validate_unique()

        # save():
        # 方法。 这个方法根据表单绑定的数据创建并保存数据库对象。 ModelForm的子类可以接受现有的模型实例作为关键字参数instance；如果提供此功能，则save()
        # 将更新该实例。 如果没有提供，save()
        # 将创建模型的一个新实例：
        cleaned = super().clean()
        if cleaned['max_dating_age'] < cleaned['min_dating_age']:
            # 通过抛异常来处理逻辑;
            # 抛出报错:Django抛错ValidationError,并且只能为ValidationError
            raise forms.ValidationError('max_dating_age 必须大于min_dating_age')
        else:
            # 这个数据在后面将插入到表单的 cleaned_data 字典中。否则Django会认为为空;
            return cleaned['max_dating_age']

    def clean_max_distance(self):
        '''检查最大距离'''
        # 调用父类的清洗方法
        cleaned = super().clean()
        if cleaned['max_distance'] < cleaned['min_distance']:
            # 抛出报错,只能为ValidationError,否则Django无法捕获
            raise forms.ValidationError('max_dating_age 必须大于min_dating_age')
        else:
            # 将原有值进行返回,否则Django会认为为空;
            return cleaned['max_distance']