from django import forms
'''
    就像模型类的属性映射到数据库的字段一样，表单类的字段会映射到HTML 的<input>表单的元素。
    （ModelForm 通过一个Form 映射模型类的字段到HTML 表单的<input> 元素；
    class NameForm(forms.Form):
        your_name = forms.CharField(label='Your name', max_length=100)
    注释:
        max_length:
            作用:
                在HTML 的<input> 上放置一个maxlength="100" ,阻止用户的不合理输入;
                Django 收到浏览器发送过来的表单时，它将验证数据的长度;
        is_valid():
            为所有的字段运行验证的程序,若所有字段合法,则返回True;
            同时将表单的数据放到cleaned_data 属性中;
        is_bound 属性:
            一个表单是否具有绑定的数据
        在View层中的使用:
        def get_name(request):
            # 如果这是一个POST请求,我们就需要处理表单数据
            if request.method == 'POST':
                # 创建一个表单实例,并且使用表单数据填充request请求:
                form = NameForm(request.POST)
                # 检查数据有效性:
                if form.is_valid():
                    # 在需要时，可以在form.cleaned_date中处理数据
                    # ...
                    # 重定向到一个新的URL:
                    return HttpResponseRedirect('/thanks/') 
                    
                    
    从模型创建表单(表单类与模型类的结合使用)   :
    # 自定义表单类,内部关联Article模型
    class ArticleForm(ModelForm):
...     class Meta:
...         model = Article
...         fields = ['pub_date', 'headline', 'content', 'reporter']

    form = ArticleForm()
    article = Article.objects.get(pk=1)
    
'''
class TestForm(forms.Form):
    '''创建form信息,会校验用户提交的信息'''
    SEX = (
        ('male','男'),
        ('female','女')
    )
    name = forms.CharField(max_length=5)
    sex = forms.ChoiceField(choices=SEX)
    age = forms.IntegerField()
    login_date = forms.DecimalField()

POST = {
    'name':'bobo',
    'sex':'男性',
    'age':'25岁',
    'login_date':'2011/1/1'
}

form = TestForm(POST)
# is_valid()
print(form.is_valid())

# 查看form对象信息,字典格式
# form.cleaned_data与is_valid之间相互存在依赖,is_valid之后,才会生成cleaned_data;

# form.errors   查看错误原因,对于缺失的数据,同样会进行报错,多余字段,不做检查;


