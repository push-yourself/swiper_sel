from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

from common import stat
from user.models import User


class AuthorizeMiddleware(MiddlewareMixin):
    '''登陆验证中间件'''
    # 创建白名单,对其path进行控制;
    WHITE_LIST = [
        '/api/user/get_vcode',
        '/api/user/check_vcode',
        '/weibo/wb_auth',
        '/weibo/callback',
    ]

    def process_request(self, request):
        # 在处理url之前进行逻辑处理,常用于URL的处理
        # request.path   获取当前请求地址;
        if request.path in self.WHITE_LIST:
            # 如果在白名单中,不需要进行处理;
            return    #直接放行
        # 对于登录状态下的进行检查校验
        # 查看请求中的session值
        uid = request.session.get('uid')
        if not uid:
            return JsonResponse({'code': stat.LOGIN_REQUIRED, 'data': None})
        # 获取当前用户
        request.user = User.objects.get(id=uid)
