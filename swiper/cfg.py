'''程序逻辑配置和第三方平台配置'''

# 云之讯短信配置
#1.云之讯API接口
from urllib.parse import urlencode

YZX_API = 'https://open.ucpaas.com/ol/sms/sendsms'
#2.云之讯对接配置信息
YZX_ARGS = {
 "sid":"7aff728e27f63cf7262cd6153ee858b1",
 "token":"89a16f69458e552cd6b90a7ec5bf7345",
 "appid":"7fcaf20b5aac40008474ba3b84e66e42",
 "templateid":"549632",
 "param":"None",
 "mobile":"None",
 "uid":"2d92c6132139467b989d087c84a365d8"
}

# 微博第三方登录接口
WB_APP_KEY = '3531485379'
WB_APP_SECRET = '4ed4cda6b8250e96e1a33f25e59cda7b'
WB_CALLBACK = 'http://127.0.0.1:8000/weibo/callback'
# 第一步: Authorize 接口
WB_AUTH_API = 'https://api.weibo.com/oauth2/authorize'
WB_AUTH_ARGS = {
    'client_id': WB_APP_KEY,
    'redirect_uri': WB_CALLBACK,
    'display': 'default'
}
WB_AUTH_URL = '%s?%s' % (WB_AUTH_API, urlencode(WB_AUTH_ARGS))

# 2.AccessToken接口调用
WB_ACCESS_TOKEN_API = 'https://api.weibo.com/oauth2/access_token'
WB_ACCESS_TOKEN_ARGS = {
    'client_id': WB_APP_KEY,
    'client_secret': WB_APP_SECRET,
    'grant_type': 'authorization_code',
    'redirect_uri': WB_CALLBACK,
    'code': None,
}
# 3.获取用户信息
WB_USER_SHOW = 'https://api.weibo.com/2/users/show.json'
WB_USER_SHOW_ARGS = {
    'access_token':None,
    'uid':None
}


#REDIS 相关配置( 封装操作)
REDIS = {
    'host':'127.0.0.1',
    'port':'6379',
    'db':'3',
    'password':'123456'
}


# 反悔相关配置
DAILY_REWIND = 3    # 每日反悔次数
REWIND_TIMEOUT = 5 * 60  # 可反悔的滑动记录秒数