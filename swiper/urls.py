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

from user import api as user_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/get_vcode',user_api.get_vcode),
    path('api/user/check_vcode',user_api.check_vcode),
    path('api/weibo/wb_auth',user_api.wb_auth),
    path('api/user/get_profile',user_api.get_profile),
    path('api/user/set_profile',user_api.set_profile),
]
