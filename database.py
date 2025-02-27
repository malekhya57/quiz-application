from flask import Flask
from config import SQLALCHEMY_DATABASE_URI
from models import db, Question

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    db.init_app(app)
    with app.app_context():
        db.create_all()
        seed_questions()  # Add this line to populate DB

def seed_questions():
    """Populate database with 20 general knowledge questions if empty."""
    if Question.query.count() == 0:  # Only insert if DB is empty
        sample_questions = [
            {"question_text": "What is the capital of France?", "option_a": "Berlin", "option_b": "Madrid", "option_c": "Paris", "option_d": "Rome", "correct_answer": "C"},
            {"question_text": "Which planet is known as the Red Planet?", "option_a": "Earth", "option_b": "Mars", "option_c": "Jupiter", "option_d": "Saturn", "correct_answer": "B"},
            {"question_text": "Who wrote 'Hamlet'?", "option_a": "Shakespeare", "option_b": "Hemingway", "option_c": "Tolkien", "option_d": "Austen", "correct_answer": "A"},
            {"question_text": "What is the largest ocean on Earth?", "option_a": "Atlantic", "option_b": "Indian", "option_c": "Pacific", "option_d": "Arctic", "correct_answer": "C"},
            {"question_text": "What is the hardest natural substance on Earth?", "option_a": "Gold", "option_b": "Iron", "option_c": "Diamond", "option_d": "Quartz", "correct_answer": "C"},
            {"question_text": "Which is the longest river in the world?", "option_a": "Amazon", "option_b": "Nile", "option_c": "Yangtze", "option_d": "Mississippi", "correct_answer": "B"},
            {"question_text": "What is the currency of Japan?", "option_a": "Yen", "option_b": "Won", "option_c": "Peso", "option_d": "Euro", "correct_answer": "A"},
            {"question_text": "How many continents are there?", "option_a": "5", "option_b": "6", "option_c": "7", "option_d": "8", "correct_answer": "C"},
            {"question_text": "What gas do plants absorb during photosynthesis?", "option_a": "Oxygen", "option_b": "Carbon Dioxide", "option_c": "Hydrogen", "option_d": "Nitrogen", "correct_answer": "B"},
            {"question_text": "Which country is famous for pizza and pasta?", "option_a": "France", "option_b": "Germany", "option_c": "Italy", "option_d": "Spain", "correct_answer": "C"},
            {"question_text": "Who painted the Mona Lisa?", "option_a": "Van Gogh", "option_b": "Picasso", "option_c": "Leonardo da Vinci", "option_d": "Rembrandt", "correct_answer": "C"},
            {"question_text": "Which animal is known as the King of the Jungle?", "option_a": "Tiger", "option_b": "Lion", "option_c": "Elephant", "option_d": "Cheetah", "correct_answer": "B"},
            {"question_text": "What is the national flower of Japan?", "option_a": "Tulip", "option_b": "Cherry Blossom", "option_c": "Rose", "option_d": "Orchid", "correct_answer": "B"},
            {"question_text": "Which planet has the most moons?", "option_a": "Saturn", "option_b": "Jupiter", "option_c": "Mars", "option_d": "Neptune", "correct_answer": "A"},
            {"question_text": "What is the largest land animal?", "option_a": "Elephant", "option_b": "Giraffe", "option_c": "Rhino", "option_d": "Hippo", "correct_answer": "A"},
            {"question_text": "Which country is known as the Land of the Rising Sun?", "option_a": "China", "option_b": "Japan", "option_c": "Korea", "option_d": "Thailand", "correct_answer": "B"},
            {"question_text": "What is the smallest country in the world?", "option_a": "Monaco", "option_b": "Vatican City", "option_c": "San Marino", "option_d": "Liechtenstein", "correct_answer": "B"},
            {"question_text": "Which chemical element has the symbol O?", "option_a": "Oxygen", "option_b": "Gold", "option_c": "Osmium", "option_d": "Olbium", "correct_answer": "A"},
            {"question_text": "How many sides does a hexagon have?", "option_a": "4", "option_b": "5", "option_c": "6", "option_d": "7", "correct_answer": "C"},
            {"question_text": "What is the capital of Australia?", "option_a": "Sydney", "option_b": "Canberra", "option_c": "Melbourne", "option_d": "Perth", "correct_answer": "B"},
        ]

        for q in sample_questions:
            new_question = Question(**q)
            db.session.add(new_question)
        db.session.commit()
        print("✅ Database seeded with 20 questions.")
