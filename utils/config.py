import os
BASE_URL = os.getenv("BASE_URL","https://jsonplaceholder.typicode.com")
TIMEOUT = int(os.getenv("TIMEOUT","10"))