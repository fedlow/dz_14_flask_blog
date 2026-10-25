from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# --- Настройка базы данных SQLite ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- Модель Notes (пока без subtitle) ---
class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(200), nullable=True)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Note {self.title}>'

# --- Маршруты ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        title = request.form.get('title')
        subtitle = request.form.get('subtitle')  # 🆕
        content = request.form.get('content')
        
        if title and content:
            new_note = Notes(title=title, subtitle=subtitle, text=content)  # 🆕
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('notes'))
    
    # Выгружаем все записи из БД (сначала новые)
    all_notes = Notes.query.order_by(Notes.id.desc()).all()
    return render_template('notes.html', notes=all_notes)

if __name__ == '__main__':
    app.run(debug=True)