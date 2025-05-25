from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    # import dan register blueprint main
    from .routes import main
    app.register_blueprint(main)

    # import dan register blueprint auth dengan prefix /auth
    from .routes.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    return app

