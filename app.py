from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных
db = SQLAlchemy(app)

# Модель задачи (таблица Agent)
class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Имя {self.name}>"

# Создаем таблицу в базе данных
with app.app_context():
    db.create_all()

### 📌 CRUD-МАРШРУТЫ

# 📌 Главная страница: список агентов
@app.route('/')
@app.route('/agents')
def get_agents():
    agents = Agent.query.all()  # Получаем всех агентов из базы
    return render_template('agents.html', agents=agents)

# 📌 Фильтрация
@app.route('/agents/filter', methods=['POST'])
def filter_agents():
    level = request.form.get('level')  # Получаем уровень из формы
    if level:
        secret_agents = Agent.query.filter_by(level=level).all()
        return render_template('agents.html', agents=secret_agents)
    return redirect(url_for('get_agents'))

# 📌 Добавление нового агента
@app.route('/add', methods=['GET', 'POST'])
def add_agent():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        level = request.form['level']
        if name.strip():  # Проверяем, что строка не пустая
            new_agent = Agent(name=name, phone=phone, email=email, level=level)
            db.session.add(new_agent)
            db.session.commit()
        return redirect(url_for('get_agents'))
    return render_template('add_agent.html')

# 📌 Редактирование агента
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_agent(id):
    agent = Agent.query.get_or_404(id)  # Получаем агента по ID
    if request.method == 'POST':
        new_name = request.form['name']
        new_phone = request.form['phone']
        new_email = request.form['email']
        new_level = request.form['level']
        if new_name.strip():
            agent.name = new_name
            agent.phone = new_phone
            agent.email = new_email
            agent.level = new_level
            db.session.commit()
        return redirect(url_for('get_agents'))
    return render_template('edit_agent.html', agent=agent)

# 📌 Удаление агента
@app.route('/delete/<int:id>')
def delete_agent(id):
    agent = Agent.query.get_or_404(id)  # Получаем агента по ID
    db.session.delete(agent)  # Удаляем из базы
    db.session.commit()  # Подтверждаем изменения
    return redirect(url_for('get_agents'))

# 📌 Просмотр агентов
@app.route('/agent/<int:id>')
def view_agent(id):
    agent = Agent.query.get(id)  # Получаем агента по ID
    if agent is None:
        return redirect(url_for('get_agents'))
    return render_template('agent.html', agent=agent)


# Запуск сервера
if __name__ == "__main__":
    app.run(debug=True)