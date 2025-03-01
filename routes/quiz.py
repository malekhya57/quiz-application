import random
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Question, UserAnswer, TestSession

quiz_blueprint = Blueprint("quiz", __name__)

@quiz_blueprint.route("/get_random_questions", methods=["GET"])
@jwt_required()
def get_random_questions():
    questions = Question.query.all()
    selected = random.sample(questions, 15) if len(questions) >= 15 else questions
    result = []
    for q in selected:
        result.append({
            "id": q.id,
            "question_text": q.question_text,
            "options": {"A": q.option_a, "B": q.option_b, "C": q.option_c, "D": q.option_d}
        })
    return jsonify(result), 200

@quiz_blueprint.route("/submit_quiz", methods=["POST"])
@jwt_required()
def submit_quiz():
    data = request.json  
    user_identity = get_jwt_identity()
    user_id = user_identity["id"]
    if not isinstance(data, list):
        return jsonify({"message": "Invalid data format, expected a list"}), 400

    score = 0
    for answer in data:
        question = Question.query.get(answer.get("question_id"))
        if not question:
            continue
        selected = answer.get("selected_answer")
        is_correct = (question.correct_answer == selected)
        if is_correct:
            score += 1
        ua = UserAnswer(
            user_id=user_id,
            question_id=question.id,
            selected_answer=selected,
            is_correct=is_correct
        )
        db.session.add(ua)
    test_session = TestSession(user_id=user_id, score=score, total_questions=len(data))
    db.session.add(test_session)
    db.session.commit()
    return jsonify({"score": score, "total": len(data)}), 200

@quiz_blueprint.route("/results", methods=["GET"])
@jwt_required()
def get_results():
    user_identity = get_jwt_identity()
    user_id = user_identity["id"]
    sessions = TestSession.query.filter_by(user_id=user_id).all()
    results = []
    for s in sessions:
        results.append({
            "id": s.id,
            "score": s.score,
            "total": s.total_questions,
            "timestamp": s.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(results), 200
