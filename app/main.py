from flask import Flask
from models import db
from routes.auth import auth_bp  # your blueprint

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
