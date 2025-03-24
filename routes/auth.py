from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("Username and password required")
            return redirect(url_for("auth.register"))
        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return redirect(url_for("auth.register"))
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        # Return an HTML snippet with JavaScript alert and redirect
        return '''
            <script>
                alert("User registered successfully. Please log in.");
                window.location.href="/auth/login";
            </script>
        '''
    return render_template("register.html")

@auth_blueprint.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("user_dashboard"))
        else:
            flash("Invalid credentials")
            return render_template("login.html")
    return render_template("login.html")

@auth_blueprint.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect(url_for("auth.login_page"))
