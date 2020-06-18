from django.shortcuts import render

from libs.http import render_json

# Create your views here.

def get_rcmd_users(request):
    '''获取推荐用户'''
    pass

def like(request):
    '''右滑喜欢'''
    pass

def superlike(request):
    '''上划超级喜欢'''
    pass

def dislike(request):
    '''左滑不喜欢'''
    pass


def rewind(request):
    '''后悔'''
    pass

def who_liked_me(request):
    '''谁喜欢我'''
    pass

def friend_list(request):
    '''好友列表'''
    pass