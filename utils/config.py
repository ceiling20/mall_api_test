import os
BASE_URL = os.getenv("BASE_URL","http://localhost:8080")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")   # 改成你 mall 数据库的密码
DB_NAME = os.getenv("DB_NAME", "mall")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
TIMEOUT = int(os.getenv("TIMEOUT","10"))