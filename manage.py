#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    # 当前终端设置的环境变量添加Django环境变量，并加载相关配置
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiper.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

# 如果为主函数
if __name__ == '__main__':
    main()
