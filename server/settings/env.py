import os 
from dotenv import load_dotenv

load_dotenv()


DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')


EMAIL_BACKEND = str(os.getenv('EMAIL_BACKEND'))
EMAIL_HOST = str(os.getenv('EMAIL_HOST'))
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
SECRET_KEY = str(os.getenv('SECRET_KEY'))