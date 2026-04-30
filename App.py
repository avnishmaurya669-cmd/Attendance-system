from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(_name_)
app.secret_key = "secret"

def get_db():
    return sqlite3.connect("database.db")

# Home/Login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if user == "avnish" and password == "123":
            session['user'] = user
            session['role'] = role
            return redirect('/dashboard')

    return render_template("login.html")

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template("dashboard.html", role=session['role'])
    return redirect('/')

# Add Student
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    db = get_db()
    db.execute("INSERT INTO students(name) VALUES(?)", (name,))
    db.commit()
    return redirect('/dashboard')

# Attendance
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    db = get_db()
    if request.method == 'POST':
        student_id = request.form['student_id']
        status = request.form['status']
        db.execute("INSERT INTO attendance(student_id, status) VALUES(?,?)", (student_id, status))
        db.commit()

    students = db.execute("SELECT * FROM students").fetchall()
    return render_template("attendance.html", students=students)

# Books
@app.route('/books', methods=['GET', 'POST'])
def books():
    db = get_db()
    if request.method == 'POST':
        book = request.form['book']
        db.execute("INSERT INTO books(name) VALUES(?)", (book,))
        db.commit()

    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("books.html", books=books)

app.run(debug=True)
