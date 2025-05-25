from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Model User (Mahasiswa)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    prodi = db.Column(db.String(50), nullable=False)
    perguruan_tinggi = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # Relasi: user bisa isi banyak questionnaire response
    responses = db.relationship('QuestionnaireResponse', backref='user', lazy=True)

# Model Dosen
class Lecturer(db.Model):
    __tablename__ = 'lecturers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Relasi: dosen punya banyak course
    courses = db.relationship('Course', backref='lecturer', lazy=True)

# Model Mata Kuliah
class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturers.id'), nullable=False)
    # Relasi: course punya banyak questionnaire response
    responses = db.relationship('QuestionnaireResponse', backref='course', lazy=True)

# Model Questionnaire
class Questionnaire(db.Model):
    __tablename__ = 'questionnaires'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Relasi: questionnaire punya banyak question
    questions = db.relationship('Question', backref='questionnaire', lazy=True, cascade='all, delete-orphan')

# Model Question (pertanyaan dalam questionnaire)
class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaires.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False)  # contoh: rating, text, multiple-choice

# Model QuestionnaireResponse (jawaban dari mahasiswa)
class QuestionnaireResponse(db.Model):
    __tablename__ = 'questionnaire_responses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaires.id'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Relasi: response punya banyak jawaban detail
    answers = db.relationship('Answer', backref='response', lazy=True, cascade='all, delete-orphan')

# Model Answer (jawaban per pertanyaan)
class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    response_id = db.Column(db.Integer, db.ForeignKey('questionnaire_responses.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=True)
    answer_value = db.Column(db.Integer, nullable=True)  # untuk rating misal

    question = db.relationship('Question')

# Contoh fungsi tambah user
def add_user(nim, name, prodi, perguruan_tinggi, semester, email, password_hash):
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
    return new_user

# Contoh fungsi tambah kuisioner (admin)
def add_questionnaire(title, description):
    new_q = Questionnaire(title=title, description=description)
    db.session.add(new_q)
    db.session.commit()
    return new_q

# Contoh fungsi tambah question ke kuisioner
def add_question(questionnaire_id, text, question_type):
    question = Question(
        questionnaire_id=questionnaire_id,
        text=text,
        question_type=question_type
    )
    db.session.add(question)
    db.session.commit()
    return question
