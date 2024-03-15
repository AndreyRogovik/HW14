from dotenv import load_dotenv
import os


load_dotenv()

APP_HOST = os.getenv("APP_HOST")
APP_PORT = int(os.getenv("APP_PORT"))


MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_SERVER = os.getenv("MAIL_SERVER")


DATABASE_URL = os.getenv("DATABASE_URL")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


REDIS_HOST = 'localhost'
REDIS_PORT = int(os.getenv("REDIS_PORT"))


CLOUD_NAME = os.getenv("CLOUD_NAME")
API_KEY = int(os.getenv("API_KEY"))
API_SECRET = os.getenv("API_SECRET")
