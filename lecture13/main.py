import datetime

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello')
@app.route('/hello/<name>')
def hello(name='Anonymous'):
    return render_template('hello.html', name=name)


@app.route('/add', methods=['GET', 'POST'])
def add():
    message = date = task = ''
    if request.method == 'POST':
        date = request.form.get('date', '')
        task = request.form.get('task', '')
        print(date, task)
        try:
            if not date or not task:
                raise ValueError
            date = datetime.datetime.strptime(date, '%d.%m.%y')

            db = sqlite3.connect('todo.db')
            cursor = db.cursor()
            cursor.execute('insert into tasks (date, task) values (?, ?)', (date, task))
            db.commit()
            cursor.close()
            db.close()

            return redirect('/')
        except ValueError:
            message = 'Incorrect input'
    return render_template('add.html', date=date, task=task, message=message)


if __name__ == '__main__':
    app.run(debug=True)
