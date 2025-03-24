from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
from models import db, Question, Result, User
from werkzeug.security import check_password_hash
from functools import wraps

admin_blueprint = Blueprint("admin", __name__)

def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
         if not session.get("admin_logged_in"):
              return redirect(url_for("admin.admin_login"))
         return f(*args, **kwargs)
    return decorated_function

@admin_blueprint.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        from models import Admin  # import here to avoid circular import
        admin_user = Admin.query.filter_by(username=username).first()
        if admin_user and check_password_hash(admin_user.password, password):
            session["admin_logged_in"] = True
            session["admin_username"] = admin_user.username
            return redirect(url_for("admin.admin_dashboard"))
        else:
            flash("Invalid credentials")
            return render_template("admin_login.html")
    return render_template("admin_login.html")

@admin_blueprint.route("/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    session.pop("admin_username", None)
    return redirect(url_for("admin.admin_login"))

@admin_blueprint.route("/dashboard", methods=["GET"])
@admin_login_required
def admin_dashboard():
    results = Result.query.all()
    dashboard_results = []
    for r in results:
        user = User.query.get(r.user_id)
        dashboard_results.append({
            "result_id": r.id,
            "username": user.username if user else "Unknown",
            "score": r.score,
            "total": r.total_questions,
            "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    return render_template("admin_dashboard.html", results=dashboard_results)

@admin_blueprint.route("/questions", methods=["GET"])
@admin_login_required
def manage_questions():
    questions = Question.query.all()
    return render_template("admin_questions.html", questions=questions)

@admin_blueprint.route("/add_question", methods=["POST"])
@admin_login_required
def add_question():
    data = request.get_json()
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
@admin_login_required
def delete_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"message": "Question not found"}), 404
    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question deleted successfully"}), 200
