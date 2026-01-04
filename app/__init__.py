"""
App Package
"""
from .blueprints.main import main_bp
from .blueprints.admin import admin_bp
from config import ProductionConfig, DevelopmentConfig, TestingConfig
from .db import init_db
from .db_helpers import get_admin
from dotenv import load_dotenv
from flask import Flask, current_app, url_for, render_template
from flask_ckeditor import CKEditor
import os
from werkzeug.exceptions import HTTPException

# import traceback; traceback.print_stack()

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ckeditor = CKEditor()

def create_app():

    app = Flask(
        __name__,
        static_folder=os.path.join(BASE_DIR, 'static'),
        static_url_path='/static'
        )

    ckeditor.init_app(app)

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(main_bp, url_prefix='/')

    # App Configuration
    env = os.getenv('ENV_NAME', 'development')
    if env == 'production':
        app.config.from_object('config.ProductionConfig')
    elif env == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    # app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    # app.config['ENV_NAME'] = os.getenv('ENV_NAME')
    # app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
    
    # # CK Editor Setup
    # app.config['CKEDITOR_PKG_TYPE'] = 'basic'
    # app.config['CKEDITOR_ENABLE_CODESNIPPET'] = False

    # Database
    # app.config['SQLALCHEMY_ECHO'] = False
    # app.config['CREATE_TABLES'] = False   # Set to True for local development
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    # Local dev setup
    from .routes import dev_routes
    dev_routes.register_dev_routes(app)
    # app.config['DEBUG'] = app.config['ENV_NAME'] == 'local'
    # app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')

    if app.config['ENV_NAME'] == 'production':
        from .storage.gcs import GCSImageStorage
        # app.config['IMAGE_STORAGE_BACKEND'] = 'gcs'
        # app.config['IMAGE_STORAGE_CONTAINER'] = os.getenv('IMAGE_STORAGE_CONTAINER')
        app.extensions['image_storage'] = GCSImageStorage(app)
    else:
        from .storage.local import LocalImageStorage
        # app.config['IMAGE_STORAGE_BACKEND'] = 'local'
        # app.config['IMAGE_STORAGE_CONTAINER'] = app.config['UPLOAD_FOLDER']
        app.extensions['image_storage'] = LocalImageStorage(app)


    init_db(app)

    from .cli import init_cli


    @app.errorhandler(HTTPException)
    def error_page(error):
        return render_template('main/error-page.html', error=error), error.code


    @app.context_processor
    def inject_logo_url():
        # user_logo_path = os.path.join(BASE_DIR, 'static', 'uploads', 'users', 'user-logo.png')
        admin = get_admin()
        if admin:
            user_logo = admin.logo_img

            if user_logo:
                return {
                    'logo_url': user_logo
                }
        else:
            return {
                'logo_url': url_for('static', filename='images/default-logo.png')
            }
        

    init_cli(app)


    return app



