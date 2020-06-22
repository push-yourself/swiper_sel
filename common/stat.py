'''
    保存程序逻辑中的状态码
'''
class LoginErr(Exception):
    '''逻辑报错'''
    code = None
    data = None

    def __init__(self,code='OK',data = None):
        self.code = code
        self.data = data

def gen_login_err(name,code):
    '''生成逻辑异常类'''
    return type(name,(LoginErr,),{'code':code})
# 发送OK
OK = 0
# 发送验证码失败
VCODE_ERR = gen_login_err('VCODE_ERR',1000)
# 发送无效验证码
AVILD_VCODE = gen_login_err('AVILD_VCODE',1001)
# 授权码接口错误
ACCESS_TOKEN_ERR = gen_login_err('ACCESS_TOKEN_ERR',1002)
# 用户信息接口错误
USER_INFO_ERR = gen_login_err('USER_INFO_ERR',1003)
# 用户未登录
LOGIN_REQUIRED = gen_login_err('LOGIN_REQUIRED',1004)
# 用户数据提交错误
USER_DATA_ERR = gen_login_err('USER_DATA_ERR',1005)
# 用户交友资料错
PROFILE_DATA_ERR = gen_login_err('PROFILE_DATA_ERR',1006)
# 滑动类型错误
SwipeTypeErr =  gen_login_err('SwipeTypeErr',1007 )
# 重复滑动错误
SwipeRepeatErr = gen_login_err('SwipeRepeatErr',1008)

