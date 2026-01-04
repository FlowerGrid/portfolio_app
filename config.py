from dotenv import load_dotenv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

load_dotenv()


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    ENV_NAME = os.getenv('ENV_NAME')
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    
    # CK Editor Setup
    CKEDITOR_PKG_TYPE = 'basic'
    CKEDITOR_ENABLE_CODESNIPPET = False

    # Database
    SQLALCHEMY_ECHO = False
    CREATE_TABLES = False   # Set to True for local development
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class ProductionConfig(BaseConfig):
    IMAGE_STORAGE_BACKEND = 'gcs'
    IMAGE_STORAGE_CONTAINER = os.getenv('IMAGE_STORAGE_CONTAINER')


class DevelopmentConfig(BaseConfig):
    # Local dev setup
    DEBUG = True
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')


    IMAGE_STORAGE_BACKEND = 'local'
    IMAGE_STORAGE_CONTAINER = UPLOAD_FOLDER


class TestingConfig(BaseConfig):
    pass