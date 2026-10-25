from flask import Flask, render_template, request

app = Flask(__name__)

# Глобальный словарь для хранения записей: ключ - заголовок, значение - текст
notes_dict = {}

@app.route('/')
def index():
    return render_template('index.html')

# Новый маршрут для дневника
@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        # Получаем данные из формы
        title = request.form.get('title')
        content = request.form.get('content')
        
        # Если оба поля заполнены, сохраняем в словарь
        if title and content:
            notes_dict[title] = content
            
    # Передаем словарь в шаблон для отображения
    return render_template('notes.html', notes=notes_dict)

if __name__ == '__main__':
    app.run(debug=True)