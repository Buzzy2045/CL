from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Extract fields and basic validation
    nim = data.get('nim')
    name = data.get('name')
    prodi = data.get('prodi')
    perguruan_tinggi = data.get('perguruan_tinggi')
    semester = data.get('semester')
    email = data.get('email')
    password = data.get('password')

    if not all([nim, name, prodi, perguruan_tinggi, semester, email, password]):
        return jsonify({"message": "Missing required fields"}), 400

    # Check if email or nim already exist
    if User.query.filter((User.email == email) | (User.nim == nim)).first():
        return jsonify({"message": "Email or NIM already registered"}), 409

    password_hash = generate_password_hash(password)
    new_user = User(
        nim=nim,
        name=name,
        prodi=prodi,
        perguruan_tinggi=perguruan_tinggi,
        semester=semester,
        email=email,
        password_hash=password_hash
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        
        return jsonify({"message": "Login successful"}), 200
    
    return jsonify({"message": "Invalid email or password"}), 401
