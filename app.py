
import os
import psycopg
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'local-secret-key')


def get_db():
    return psycopg.connect(os.getenv('DATABASE_URL'))


@app.route('/')
def home():
    with get_db() as conn:
        students = conn.execute(
            'SELECT id, name, group_name, subject, score FROM students ORDER BY id'
        ).fetchall()

    total = len(students)
    average = sum(s[4] for s in students) / total if total else 0

    return render_template(
        'index.html',
        students=students,
        total=total,
        average=average
    )


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        group = request.form['group']
        subject = request.form['subject']
        score = int(request.form['score'])

        with get_db() as conn:
            conn.execute(
                '''INSERT INTO students
                   (name, group_name, subject, score)
                   VALUES (%s, %s, %s, %s)''',
                (name, group, subject, score)
            )

        return redirect('/')

    return render_template('add_student.html')



@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    with get_db() as conn:
        student = conn.execute(
            'SELECT id, name, group_name, subject, score FROM students WHERE id = %s',
            (student_id,)
        ).fetchone()

        if student is None:
            return 'Talaba topilmadi', 404

        if request.method == 'POST':
            name = request.form['name']
            group = request.form['group']
            subject = request.form['subject']
            score = int(request.form['score'])

            conn.execute(
                '''UPDATE students
                   SET name = %s, group_name = %s, subject = %s, score = %s
                   WHERE id = %s''',
                (name, group, subject, score, student_id)
            )
            return redirect('/')

    return render_template('edit_student.html', student=student)

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name TEXT,
                group_name TEXT,
                subject TEXT,
                score INTEGER
            )
        ''')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

