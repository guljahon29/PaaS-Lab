
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('students.db')
    return conn

@app.route('/')
def home():
    conn = get_db()
    students = conn.execute('SELECT * FROM students').fetchall()
    total = len(students)
    average = sum(s[4] for s in students) / total if total else 0
    conn.close()
    return render_template('index.html',
                           students=students,
                           total=total,
                           average=average)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        group = request.form['group']
        subject = request.form['subject']
        score = int(request.form['score'])

        conn = get_db()
        conn.execute(
            'INSERT INTO students (name, group_name, subject, score) VALUES (?, ?, ?, ?)',
            (name, group, subject, score)
        )
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template('add_student.html')

if __name__ == '__main__':
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        group_name TEXT,
        subject TEXT,
        score INTEGER
    )''')
    conn.commit()
    conn.close()
    app.run(debug=True)
