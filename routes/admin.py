from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from models import db, TestSession, Question, User

admin_blueprint = Blueprint("admin", __name__)

@admin_blueprint.route("/dashboard", methods=["GET"])
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.admin_login"))
    sessions = TestSession.query.all()
    results = []
    for s in sessions:
        user = User.query.get(s.user_id)
        results.append({
            "session_id": s.id,
            "username": user.username if user else "Unknown",
            "score": s.score,
            "total": s.total_questions,
            "timestamp": s.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    return render_template("admin_dashboard.html", results=results)

@admin_blueprint.route("/questions", methods=["GET"])
def manage_questions():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.admin_login"))
    
    questions = Question.query.all()  
    return render_template("admin_questions.html", questions=questions)

@admin_blueprint.route("/add_question", methods=["POST"])
def add_question():
    if not session.get("admin_logged_in"):
        return jsonify({"message": "Unauthorized"}), 403
    data = request.json
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

@admin_blueprint.route("/delete_question/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    if not session.get("admin_logged_in"):
        return jsonify({"message": "Unauthorized"}), 403
    
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"message": "Question not found"}), 404
    
    db.session.delete(question)
    db.session.commit()
    
    return jsonify({"message": "Question deleted successfully"}), 200


@admin_blueprint.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "admin":
            session["admin_logged_in"] = True
            return redirect(url_for("admin.admin_dashboard"))
        else:
            return render_template("admin_login.html", error="Invalid credentials")
    return render_template("admin_login.html")

@admin_blueprint.route("/logout", methods=["GET"])
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin.admin_login"))
