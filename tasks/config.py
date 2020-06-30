# Celery相关配置

# 通用配置
timezone = 'Asia/Shanghai'
accept_content = ['pickle', 'json']# 可接收的内容
worker_redirect_stdouts_level = 'INFO'
# 任务相关配置
broker_url = 'redis://127.0.0.1:6379/3'
broker_pool_limit = 100  # Borker 连接池, 默认是10
task_serializer = 'pickle'# 任务的序列化采用pickle

# 结果相关
result_backend = 'redis://127.0.0.1:6379/3'
result_serializer = 'pickle'
result_expires = 3600  # 任务过期时间
result_cache_max = 10000  # 任务结果最大缓存数量