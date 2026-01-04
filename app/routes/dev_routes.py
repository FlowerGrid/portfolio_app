from flask import send_from_directory, current_app

def register_dev_routes(app):
    if app.config['ENV_NAME'] == 'local':
        @app.route('/uploads/<path:filename>')
        def uploads(filename):
            return send_from_directory(
                app.config['UPLOAD_FOLDER'],
                filename
            )