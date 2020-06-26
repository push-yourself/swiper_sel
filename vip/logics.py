from common import stat

def need_permission(view_func):
    '''权限检查'''
    def check(request,*args,**kwargs):
        # 检查当前用户是否具有所操作的函数对应的权限
        # 将函数名称赋值给权限名称
        perm_name = view_func.__name__
        if request.user.vip.has_perm(perm_name):
            view_func(request,*args,**kwargs)
        else:
            raise stat.PermissonLimit
    return check
