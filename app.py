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
    sessions = Session.query.order_by(Session.date.desc()).all()
    mistakes = Mistake.query.order_by(Mistake.date.desc()).all()
    return render_template('dashboard.html', sessions=sessions, mistakes=mistakes)


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