import pymysql
# 伪装作用
# sys.modules["MySQLdb"] = sys.modules["_mysql"] = sys.modules["pymysql"]
# 实际是将pymysql来传给MySQLdb键值对的值[动态替换\Monkey pache]
pymysql.install_as_MySQLdb()