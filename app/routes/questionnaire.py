from flask import Blueprint, request, jsonify
from app.models import db, QuestionnaireResponse, Answer, Questionnaire, Question
from datetime import datetime

questionnaire_bp = Blueprint('questionnaire', __name__)

@questionnaire_bp.route('/submit', methods=['POST'])
def submit_response():
    data = request.get_json()
    user_id = data.get('user_id')
    course_id = data.get('course_id')
    questionnaire_id = data.get('questionnaire_id')
    answers = data.get('answers')

    if not all([user_id, course_id, questionnaire_id, answers]):
        return jsonify({"message": "Missing data"}), 400

    response = QuestionnaireResponse(
        user_id=user_id,
        course_id=course_id,
        questionnaire_id=questionnaire_id,
        submitted_at=datetime.utcnow() 
    )
    db.session.add(response)
    db.session.flush()  # supaya dapat ID sebelum commit

    for ans in answers:
        answer = Answer(
            response_id=response.id,
            question_id=ans['question_id'],
            answer_text=ans.get('answer_text'),
            answer_value=ans.get('answer_value')
        )
        db.session.add(answer)

    db.session.commit()
    return jsonify({"message": "Response submitted successfully"}), 201
