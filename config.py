import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:password@localhost/task_manager")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
