from redis import Redis
from swiper.cfg import REDIS
import pickle
from redis import Redis as _Redis

# REDIS配置
rds = Redis(**REDIS)


class Redis(_Redis):
    '''Redis封装'''
    def set(self,name,value,ex=None,px=None,nx=False,xx=False):
        # pickle 序列化
        '''
        Set the value at key ``name`` to ``value``
        :param name:
        :param value:
        :param ex: ``ex`` sets an expire flag on key ``name`` for ``ex`` seconds.
        :param px: ``px`` sets an expire flag on key ``name`` for ``px`` milliseconds.
        :param nx: ``nx`` if set to True, set the value at key ``name`` to ``value`` only
        :param xx: ``xx`` if set to True, set the value at key ``name`` to ``value`` only
        :return:
        '''
        pickled_data = pickle.dumps(value,pickle.HIGHEST_PROTOCOL)
        super().set(name,pickled_data,ex,px,nx,xx)
    def get(self,name,default=None):
        """
        :param name:key值
        :param default:没有则默认default
        :return:
        """
        pickled_data = super().get(name)
        if not pickled_data:
            return default
        else:
            # 如果不是None
            try:
                # 反序列化操作
                return pickle.loads(pickled_data)
            except (TypeError,pickle.UnpicklingError):
                # 不能反序列化,则不做改变
                return pickled_data