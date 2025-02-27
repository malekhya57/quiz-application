import os

DB_USERNAME = "postgres"
DB_PASSWORD = "2002"
DB_HOST = "localhost"
DB_NAME = "quizdb"

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "b3i45noi4n5ou43b5ou43n543n5u3"  # Change this
JWT_SECRET_KEY = "bb4j234v5yu43v5u4v5ihb5ih4b54"  # For authentication
