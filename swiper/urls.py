"""swiper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from social import api as social_api
from user import api as user_api

urlpatterns = [
    # user应用
    # 用户登录注册方面
    path('admin/', admin.site.urls),
    # 获取验证码
    path('api/user/get_vcode',user_api.get_vcode),
    # 检查校验验证码
    path('api/user/check_vcode',user_api.check_vcode),
    # 微博第三方登录操作;
    path('api/weibo/wb_auth',user_api.wb_auth),
    # 微博跳转回调
    path('api/weibo/wb_callback',user_api.wb_callback),
    # 个人信息方面
    # 获取个人资料信息
    path('api/user/get_profile',user_api.get_profile),
    # 设置个人资料信息
    path('api/user/set_profile',user_api.set_profile),
    # 上传个人形象
    path('api/user/upload_avatar', user_api.upload_avatar),

    # 社交应用
    # 推荐列表路由
    path('api/social/get_rcmd_users',social_api.get_rcmd_users),
    # 喜欢某人
    path('api/social/like',social_api.like),
    # 超级喜欢某人
    path('api/social/superlike',social_api.superlike),
    # 不喜欢某人
    path('api/social/dislike',social_api.dislike),
    # 后悔滑动
    path('api/social/rewind',social_api.rewind),
    # 谁喜欢我
    path('api/social/who_liked_me',social_api.who_liked_me),
    # 用户好友列表
    path('api/social/friend_list',social_api.friend_list),
    # 热度排行
    path('api/social/hot_rank', social_api.hot_rank),
]
