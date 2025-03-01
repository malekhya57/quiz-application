# Quiz Application 🎓

Welcome to the **Quiz Application**! This is a web-based platform that allows users to register, log in, take quizzes, and view their results. Admins can manage questions and view user results through a dedicated admin dashboard.

## 🚀 Features

- **User Authentication:** Register and log in as a user.
- **Admin Panel:** Manage questions and view user results.
- **Quizzes:** Take quizzes with random questions.
- **Results:** View quiz scores and history.
- **Responsive UI:** Built with Bootstrap for a sleek and modern look.

## 📂 Project Structure

```
quiz-application/
├── app.py             # Main application entry point
├── config.py          # Configuration settings
├── database.py        # Database setup and seeding
├── models.py          # Database models
├── requirements.txt   # Project dependencies
├── routes/            # Flask blueprints
│   ├── admin.py       # Admin routes
│   ├── auth.py        # Authentication routes
│   ├── quiz.py        # Quiz routes
├── static/            # Static files (CSS, JS)
│   ├── style.css      # Custom styles
│   ├── script.js      # JavaScript functions
├── templates/         # HTML templates
│   ├── base.html      # Base template
│   ├── login.html     # User login page
│   ├── register.html  # User registration page
│   ├── quiz.html      # Quiz page
│   ├── results.html   # Results page
│   ├── admin_*.html   # Admin pages
```

## 🛠 Installation

1. Clone the repository:

```
git clone https://github.com/malekhya57/quiz-application.git
```

2. Navigate to the project directory:

```
cd quiz-application
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

4. Set up the database:

```
python app.py
```

## 🚀 Usage

Run the application:

```
python app.py
```

Open your browser and go to:

```
http://127.0.0.1:5000
```

## 🛡 Security Tips

- Change default admin credentials in `database.py`.
- Use HTTPS for production.

## 📜 License

This project is open-source and available under the MIT License.

**Happy quizzing! 🧠**
