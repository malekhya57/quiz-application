from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Question, UserAnswer

quiz_blueprint = Blueprint("quiz", __name__)

@quiz_blueprint.route("/add_question", methods=["POST"])
@jwt_required()
def add_question():
    data = request.json

    # Validate request data
    required_fields = ["question_text", "option_a", "option_b", "option_c", "option_d", "correct_answer"]
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    if data["correct_answer"] not in ["A", "B", "C", "D"]:
        return jsonify({"message": "Correct answer must be one of A, B, C, or D"}), 400

    new_question = Question(
        question_text=data["question_text"],
        option_a=data["option_a"],
        option_b=data["option_b"],
        option_c=data["option_c"],
        option_d=data["option_d"],
        correct_answer=data["correct_answer"]
    )

    db.session.add(new_question)
    db.session.commit()
    return jsonify({"message": "Question added successfully"}), 201


@quiz_blueprint.route("/get_questions", methods=["GET"])
@jwt_required()
def get_questions():
    questions = Question.query.all()
    
    return jsonify([
        {
            "id": q.id,
            "question_text": q.question_text,
            "options": {"A": q.option_a, "B": q.option_b, "C": q.option_c, "D": q.option_d},
            "correct_answer": q.correct_answer  # Optional, remove if answers shouldn't be exposed
        }
        for q in questions
    ]), 200


@quiz_blueprint.route("/submit_answer", methods=["POST"])
@jwt_required()
def submit_answer():
    data = request.json
    user_id = get_jwt_identity()  # Extract user_id from JWT

    # Validate request data
    if "question_id" not in data or "selected_answer" not in data:
        return jsonify({"message": "Missing question_id or selected_answer"}), 400

    question = Question.query.get(data["question_id"])
    if not question:
        return jsonify({"message": "Invalid question_id"}), 404

    if data["selected_answer"] not in ["A", "B", "C", "D"]:
        return jsonify({"message": "Selected answer must be A, B, C, or D"}), 400

    is_correct = question.correct_answer == data["selected_answer"]

    answer = UserAnswer(
        user_id=user_id,  # Use JWT user_id
        question_id=data["question_id"],
        selected_answer=data["selected_answer"],
        is_correct=is_correct
    )

    db.session.add(answer)
    db.session.commit()

    return jsonify({"correct": is_correct}), 200
