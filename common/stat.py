'''
    保存程序逻辑中的状态吗
'''
# 发送OK
OK = 0
# 发送验证码失败
VCODE_ERR = 1000
# 发送无效验证码
AVILD_VCODE = 1001
# 授权码接口错误
ACCESS_TOKEN_ERR = 1002
# 用户信息接口错误
USER_INFO_ERR = 1003
# 用户未登录
LOGIN_REQUIRED = 1004

# 用户数据提交错误
USER_DATA_ERR = 1005

# 用户交友资料错
PROFILE_DATA_ERR = 1006


SwipeTypeErr =  1007    # 滑动类型错误
SwipeRepeatErr = 1008 # 重复滑动错误