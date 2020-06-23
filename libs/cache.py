from redis import Redis
from swiper.cfg import REDIS

# REDIS配置
rds = Redis(**REDIS)