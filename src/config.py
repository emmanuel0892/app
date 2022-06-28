from distutils.debug import DEBUG


class configuracionApp():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'autos_db'

config = {
    'configuracion': configuracionApp
}