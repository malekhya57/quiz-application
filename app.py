from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from config import SECRET_KEY, JWT_SECRET_KEY, SQLALCHEMY_DATABASE_URI
from database import init_db
from models import db
from routes.auth import auth_blueprint
from routes.quiz import quiz_blueprint
from routes.admin import admin_blueprint
import os
from flask_cors import CORS




app = Flask(__name__, template_folder="templates", static_folder="static")

app.config["SECRET_KEY"] = SECRET_KEY
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)
init_db(app)

jwt = JWTManager(app)

app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(quiz_blueprint, url_prefix="/quiz")
app.register_blueprint(admin_blueprint, url_prefix="/admin")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/user/dashboard")
def user_dashboard():
    return render_template("user_dashboard.html")

@app.route("/quiz/take")
def take_quiz():
    return render_template("quiz.html")

@app.route("/quiz/user_results")
def user_results():
    return render_template("results.html")

@app.route("/admin/login")
def admin_login():
    return render_template("admin_login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5001)), debug=True)
