from config import SQLALCHEMY_DATABASE_URI
from werkzeug.security import generate_password_hash
from models import db, Admin, Question

def seed_admin():
    if not Admin.query.filter_by(username="admin").first():
        new_admin = Admin(username="admin", password=generate_password_hash("admin"))
        db.session.add(new_admin)
        db.session.commit()
        print("✅ Admin seeded with username 'admin' and password 'admin'.")

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config.get("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
        seed_questions()  
        seed_admin()      

def seed_questions():
    """Populate database with 25 simple questions if empty."""
    if Question.query.count() == 0:
        sample_questions = [
            {"question_text": "What is 2 + 2?", "option_a": "4", "option_b": "5", "option_c": "3", "option_d": "6", "correct_answer": "A"},
            {"question_text": "What is 10 - 3?", "option_a": "5", "option_b": "7", "option_c": "6", "option_d": "8", "correct_answer": "B"},
            {"question_text": "What is 5 x 3?", "option_a": "8", "option_b": "15", "option_c": "10", "option_d": "20", "correct_answer": "B"},
            {"question_text": "What is 16 ÷ 4?", "option_a": "2", "option_b": "3", "option_c": "4", "option_d": "5", "correct_answer": "C"},
            {"question_text": "What is the square of 3?", "option_a": "6", "option_b": "9", "option_c": "3", "option_d": "12", "correct_answer": "B"},
            {"question_text": "If all roses are flowers and some flowers fade quickly, can we say some roses fade quickly?", "option_a": "Yes", "option_b": "No", "option_c": "Maybe", "option_d": "Not enough info", "correct_answer": "D"},
            {"question_text": "Which number logically follows this series: 2, 4, 6, 8, ?", "option_a": "9", "option_b": "10", "option_c": "11", "option_d": "12", "correct_answer": "B"},
            {"question_text": "What comes next in the pattern: O, T, T, F, F, S, S, ?", "option_a": "E", "option_b": "N", "option_c": "T", "option_d": "M", "correct_answer": "A"},
            {"question_text": "Which one of the five is least like the other four? Dog, Cat, Snake, Hamster, Rabbit", "option_a": "Dog", "option_b": "Snake", "option_c": "Cat", "option_d": "Rabbit", "correct_answer": "B"},
            {"question_text": "What is the next number in the sequence: 1, 1, 2, 3, 5, 8, ?", "option_a": "10", "option_b": "11", "option_c": "13", "option_d": "15", "correct_answer": "C"},
            {"question_text": "What is the capital city of France?", "option_a": "London", "option_b": "Berlin", "option_c": "Paris", "option_d": "Madrid", "correct_answer": "C"},
            {"question_text": "Which planet is known as the Red Planet?", "option_a": "Mars", "option_b": "Venus", "option_c": "Jupiter", "option_d": "Saturn", "correct_answer": "A"},
            {"question_text": "What is the boiling point of water (in °C)?", "option_a": "90", "option_b": "95", "option_c": "100", "option_d": "105", "correct_answer": "C"},
            {"question_text": "What is the largest mammal in the world?", "option_a": "Elephant", "option_b": "Blue Whale", "option_c": "Giraffe", "option_d": "Hippopotamus", "correct_answer": "B"},
            {"question_text": "Which ocean is the largest?", "option_a": "Atlantic", "option_b": "Indian", "option_c": "Pacific", "option_d": "Arctic", "correct_answer": "C"},
            {"question_text": "In which continent is Brazil located?", "option_a": "Asia", "option_b": "South America", "option_c": "Africa", "option_d": "Europe", "correct_answer": "B"},
            {"question_text": "Who wrote the play 'Romeo and Juliet'?", "option_a": "Charles Dickens", "option_b": "William Shakespeare", "option_c": "Leo Tolstoy", "option_d": "Mark Twain", "correct_answer": "B"},
            {"question_text": "What is the chemical symbol for water?", "option_a": "H2O", "option_b": "O2", "option_c": "CO2", "option_d": "HO", "correct_answer": "A"},
            {"question_text": "How many days are there in a leap year?", "option_a": "365", "option_b": "366", "option_c": "364", "option_d": "367", "correct_answer": "B"},
            {"question_text": "Which gas do plants absorb from the atmosphere?", "option_a": "Oxygen", "option_b": "Hydrogen", "option_c": "Carbon Dioxide", "option_d": "Nitrogen", "correct_answer": "C"},
            {"question_text": "Which instrument has 88 keys?", "option_a": "Guitar", "option_b": "Piano", "option_c": "Violin", "option_d": "Flute", "correct_answer": "B"},
            {"question_text": "Which is the smallest prime number?", "option_a": "1", "option_b": "2", "option_c": "3", "option_d": "5", "correct_answer": "B"},
            {"question_text": "What is the main language spoken in Spain?", "option_a": "French", "option_b": "German", "option_c": "Spanish", "option_d": "Italian", "correct_answer": "C"},
            {"question_text": "Which is the tallest mountain in the world?", "option_a": "K2", "option_b": "Kangchenjunga", "option_c": "Mount Everest", "option_d": "Lhotse", "correct_answer": "C"}
        ]
        for q in sample_questions:
            new_question = Question(**q)
            db.session.add(new_question)
        db.session.commit()
        print("✅ Database seeded with 25 simple questions.")
