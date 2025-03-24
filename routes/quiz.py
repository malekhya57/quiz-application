import random
from flask import Blueprint, request, jsonify, session
from models import db, Question, Result
from decorators import login_required

quiz_blueprint = Blueprint("quiz", __name__)

@quiz_blueprint.route("/get_random_questions", methods=["GET"])
@login_required
def get_random_questions():
    questions = Question.query.all()
    # Select 10 questions (or all if fewer)
    selected = random.sample(questions, 10) if len(questions) >= 10 else questions
    result = []
    for q in selected:
        result.append({
            "id": q.id,
            "question_text": q.question_text,
            "options": {"A": q.option_a, "B": q.option_b, "C": q.option_c, "D": q.option_d}
        })
    return jsonify(result)

@quiz_blueprint.route("/submit_quiz", methods=["POST"])
@login_required
def submit_quiz():
    payload = request.get_json()
    answers = payload.get("answers")
    total = payload.get("total")
    
    if not isinstance(answers, list):
        return jsonify({"message": "Invalid data format, expected a list of answers"}), 400

    score = 0
    for answer in answers:
        question = Question.query.get(answer.get("question_id"))
        if not question:
            continue
        if question.correct_answer == answer.get("selected_answer"):
            score += 1

    # Save the result using the provided total number of questions
    new_result = Result(user_id=session["user_id"], score=score, total_questions=total)
    db.session.add(new_result)
    db.session.commit()

    return jsonify({"score": score, "total": total})


@quiz_blueprint.route("/results_data", methods=["GET"])
@login_required
def get_results_data():
    user_id = session["user_id"]
    results = Result.query.filter_by(user_id=user_id).all()
    output = []
    for r in results:
        output.append({
            "id": r.id,
            "score": r.score,
            "total": r.total_questions,
            "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(output)