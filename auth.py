"""authentication string"""

import os

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

CONNECTION_STRING = f"mongodb://{username}:{password}@{host}:{port}/"
