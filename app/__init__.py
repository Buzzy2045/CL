import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)

    # Import blueprint setelah app dan db dibuat
    from .routes import main as main_blueprint
    from .routes.auth import auth as auth_blueprint
    from .routes.questionnaire import questionnaire_bp

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(questionnaire_bp, url_prefix='/questionnaire')

    return app
