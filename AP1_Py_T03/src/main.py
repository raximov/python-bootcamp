# main.py
from flask import Flask, render_template
from web.module import game_blueprint  # Импортируем наш blueprint

app = Flask(__name__)
# Если вы не хотите добавлять префикс – регистрируйте без него:
app.register_blueprint(game_blueprint)

@app.route('/')
def index():
    return render_template('index.html')

# Выведите все зарегистрированные маршруты для отладки:
with app.app_context():
    for rule in app.url_map.iter_rules():
        print(rule)

if __name__ == '__main__':
    app.run(debug=True)
