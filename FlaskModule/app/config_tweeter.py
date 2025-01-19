
from flask import Flask

from FlaskApiTweeter import  main

def create_app_tweeter():
    app = Flask(__name__)
    app.register_blueprint(main)  # Enregistrer le blueprint
    return app