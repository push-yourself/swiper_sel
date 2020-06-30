# 将tasks作为模块操作
# 引入模块顺序：系统标准库、空行、第三方库、空行、自定义
import os

from celery import Celery
from tasks import config

# 加载Django环境
# 当前终端设置的环境变量添加Django环境变量，并加载相关配置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiper.settings')

celery_app = Celery('worker')
# config_from_objecct()方法：引入的模块信息传给该方法，并加载至celery_app中;
celery_app.config_from_object(config)
# 自动查找Django中定义的任务;logics中的任务
celery_app.autodiscover_tasks()





