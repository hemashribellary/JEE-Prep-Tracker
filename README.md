# JEE Prep Tracker

🚀 **Live at: https://jee-prep-tracker-jjlf.onrender.com**


I built this web app to track my JEE preparation. I was logging sessions in a notebook and it was getting hard to see patterns — which subjects I was weak in, which topics kept coming up in mistakes, how much time I was actually spending. So I decided to build something to do that automatically.

## What it does

- Log a practice session — subject, topic, how many questions I attempted and got right, time spent
- Log a mistake — what the question was, whether it was a conceptual mistake, calculation error, or silly mistake
- Dashboard with charts showing accuracy by subject and time distribution
- Automatically shows weak topics (anything below 60% accuracy)
- Mistake review page with colour coded badges

## Tech stack

Python + Flask + SQLite + SQLAlchemy + Bootstrap 5 + Chart.js + Jinja2

Deployed on Render.com

## How to run it

```
git clone https://github.com/hemashribellary/JEE-Prep-Tracker.git
cd JEE-Prep-Tracker
pip install flask flask-sqlalchemy gunicorn
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

## Project structure

```
├── app.py            — Flask routes and analytics
├── database.py       — Session and Mistake models
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── log_session.html
│   ├── log_mistake.html
│   └── mistakes.html
└── static/
    ├── style.css
    └── charts.js
```

## Background

I'm in Class 12 at Narayana Olympiad School in Bengaluru, preparing for both JEE and CBSE boards. JEE prep on top of school is roughly 20–25 extra hours a week. I wanted to use what I was learning in CS to actually help with that preparation, so I built this over about 10 weeks as a self-directed project.

This is my second CS project — the first was a phishing URL detector using machine learning.