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

    # Local dev setup
    from .routes import dev_routes
    dev_routes.register_dev_routes(app)

    if app.config['ENV_NAME'] == 'production':
        from .storage.gcs import GCSImageStorage
        app.extensions['image_storage'] = GCSImageStorage(app)
    else:
        from .storage.local import LocalImageStorage
        app.extensions['image_storage'] = LocalImageStorage(app)


    init_db(app)

    from .cli import init_cli
    init_cli(app)

    @app.errorhandler(HTTPException)
    def error_page(error):
        return render_template('main/error-page.html', error=error), error.code


    @app.context_processor
    def inject_logo_url():
        # user_logo_path = os.path.join(BASE_DIR, 'static', 'uploads', 'users', 'user-logo.png')
        admin = get_admin()
        print(admin)
        if admin:
            user_logo = admin.logo_img
            print(f'================\n>>> {user_logo}\n======================')

            if user_logo:
                return {
                    'logo_url': user_logo
                }
        else:
            return {
                'logo_url': url_for('static', filename='images/default-logo.png')
            }

    return app



