import json
from common.stat import OK
# 从django处引入,不仅引入我们项目需要,还引入了其默认的参数项
from django.conf import settings
# 仅仅引入我们项目配置文件的中的内容,仅仅为我们配置的参数项
from swiper import settings
from django.http import HttpResponse



def render_json(data=None,code=OK):
    '''对json数据的封装,使其成为符合自己的设置'''
    result = {
        'data':data,
        'code':code
    }
    # 考虑不同的形式(正式状态和调试状态)
    # 根据DEBUG的调试状态产生结果;
    if settings.DEBUG:
        json_result = json.dumps(result,ensure_ascii=False,indent=4,sort_keys=True)
    else:
        json_result = json.dumps(result,ensure_ascii=False,separators=(',',':'))

    return HttpResponse(json_result)