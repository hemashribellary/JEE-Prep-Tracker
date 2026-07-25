from flask import Flask, render_template, request, redirect, url_for
from database import db, Session, Mistake
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'jee_tracker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    from collections import defaultdict
    sessions = Session.query.order_by(Session.date.desc()).all()
    mistakes = Mistake.query.order_by(Mistake.date.desc()).all()

    # Overall totals
    total_attempted = sum(s.questions_attempted for s in sessions)
    total_correct   = sum(s.questions_correct for s in sessions)
    total_time      = sum(s.time_spent for s in sessions)
    overall_accuracy = round((total_correct / total_attempted * 100), 1) if total_attempted > 0 else 0

    # Per-subject breakdown
    subject_data = defaultdict(lambda: {'attempted': 0, 'correct': 0, 'time': 0})
    for s in sessions:
        subject_data[s.subject]['attempted'] += s.questions_attempted
        subject_data[s.subject]['correct']   += s.questions_correct
        subject_data[s.subject]['time']      += s.time_spent

    subject_accuracy = {}
    for subject, data in subject_data.items():
        if data['attempted'] > 0:
            subject_accuracy[subject] = round(data['correct'] / data['attempted'] * 100, 1)
        else:
            subject_accuracy[subject] = 0

    # Per-topic breakdown for weak topic detection
    topic_data = defaultdict(lambda: {'attempted': 0, 'correct': 0, 'subject': ''})
    for s in sessions:
        topic_data[s.topic]['attempted'] += s.questions_attempted
        topic_data[s.topic]['correct']   += s.questions_correct
        topic_data[s.topic]['subject']    = s.subject

    weak_topics = []
    for topic, data in topic_data.items():
        if data['attempted'] > 0:
            accuracy = round(data['correct'] / data['attempted'] * 100, 1)
            if accuracy < 60:
                weak_topics.append({
                    'topic': topic,
                    'subject': data['subject'],
                    'accuracy': accuracy,
                    'attempted': data['attempted']
                })
    weak_topics.sort(key=lambda x: x['accuracy'])

    return render_template('dashboard.html',
        sessions=sessions,
        mistakes=mistakes,
        total_attempted=total_attempted,
        total_correct=total_correct,
        total_time=total_time,
        overall_accuracy=overall_accuracy,
        subject_data=dict(subject_data),
        subject_accuracy=subject_accuracy,
        weak_topics=weak_topics
    )


@app.route('/log_session', methods=['GET', 'POST'])
def log_session():
    if request.method == 'POST':
        new_session = Session(
            subject=request.form['subject'],
            topic=request.form['topic'],
            questions_attempted=int(request.form['questions_attempted']),
            questions_correct=int(request.form['questions_correct']),
            time_spent=int(request.form['time_spent']),
            notes=request.form.get('notes', '')
        )
        db.session.add(new_session)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('log_session.html')

@app.route('/log_mistake', methods=['GET', 'POST'])
def log_mistake():
    if request.method == 'POST':
        new_mistake = Mistake(
            subject=request.form['subject'],
            topic=request.form['topic'],
            question=request.form['question'],
            mistake_type=request.form['mistake_type'],
            notes=request.form.get('notes', '')
        )
        db.session.add(new_mistake)
        db.session.commit()
        return redirect(url_for('mistakes'))
    return render_template('log_mistake.html')


@app.route('/mistakes')
def mistakes():
    mistakes = Mistake.query.order_by(Mistake.date.desc()).all()
    return render_template('mistakes.html', mistakes=mistakes)


@app.route('/delete_session/<int:session_id>', methods=['POST'])
def delete_session(session_id):
    session = Session.query.get_or_404(session_id)
    db.session.delete(session)
    db.session.commit()
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)