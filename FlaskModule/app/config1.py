from flask import Flask

from FlaskApi import main  # import blueprint main

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)  # Enregistrer le blueprint
    return app

# app/__init__.py



