from flask import render_template
from . import main
from flask import request, jsonify
from app.models import db, Questionnaire, Question

@main.route('/')
def home():
    return "Hello, Flask is running!"

@main.route('/admin/create_questionnaire', methods=['POST'])
def create_questionnaire():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    if not title:
        return jsonify({"message": "Title required"}), 400
    new_q = Questionnaire(title=title, description=description)
    db.session.add(new_q)
    db.session.commit()
    return jsonify({"message": "Questionnaire created", "id": new_q.id}), 201

@main.route('/admin/add_question', methods=['POST'])
def add_question():
    data = request.get_json()
    q_id = data.get('questionnaire_id')
    text = data.get('text')
    q_type = data.get('question_type')
    if not all([q_id, text, q_type]):
        return jsonify({"message": "Missing data"}), 400
    new_q = Question(questionnaire_id=q_id, text=text, question_type=q_type)
    db.session.add(new_q)
    db.session.commit()
    return jsonify({"message": "Question added"}), 201