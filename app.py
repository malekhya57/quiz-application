from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from database import init_db
from config import SECRET_KEY, JWT_SECRET_KEY
from models import db
from routes import quiz_blueprint
from auth import auth_blueprint

app = Flask(__name__, template_folder="templates", static_folder="static")

# Load configurations
app.config["SECRET_KEY"] = SECRET_KEY
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

# Initialize extensions
jwt = JWTManager(app)
init_db(app)

# Register blueprints (routes)
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(quiz_blueprint, url_prefix="/quiz")

# Serve Frontend Pages
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quiz")
def quiz_page():
    return render_template("quiz.html")

@app.route("/admin")
def admin_page():
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)
