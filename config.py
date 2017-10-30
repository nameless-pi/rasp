# Flask
# DEBUG = True
# PORT = 5555
# HOST = "localhost"
# SECRET_KEY = "a1841b5ef57d8de68b17203721a8b094f05e1e319bf23aeb"

# SQLAlchemy
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

# MYSQL - TROCAR NOMES
mysql_db_username = "root"
mysql_db_password = "root"
mysql_db_name = "rasp"
mysql_db_hostname = "localhost"

# MySQL + SQLAlchemy
SQLALCHEMY_DATABASE_URI = ("mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}"
							.format(DB_USER=mysql_db_username, DB_PASS=mysql_db_password,
									DB_ADDR=mysql_db_hostname, DB_NAME=mysql_db_name))
