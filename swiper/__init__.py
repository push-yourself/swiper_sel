import pymysql

pymysql.install_as_MySQLdb() # Monkey Patch


from libs.orm import patch_orm
patch_orm()