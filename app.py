from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from getpass import getpass
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# Initialize the databases
def init_db():
    conn = sqlite3.connect('Admin_KPSTR.db')
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS Admin_KPSTR(
                   id INTEGER PRIMARY KEY,
                   username TEXT UNIQUE NOT NULL,
                   password TEXT NOT NULL)
                   ''')
    conn.commit()
    conn.close()

    conn = sqlite3.connect('usersKPSTR.db')
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS usersKPSTR(
                   id INTEGER PRIMARY KEY,
                   username TEXT UNIQUE NOT NULL,
                   password TEXT NOT NULL)
                   ''')
    conn.commit()
    conn.close()


# Routes
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/admin/register', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('Admin_KPSTR.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Admin_KPSTR WHERE username = ?", (username,))
        if cursor.fetchone() is not None:
            return "Username already exists. Please choose a different username."
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("INSERT INTO Admin_KPSTR(username, password) VALUES(?,?)", (username, hashed_password))
            conn.commit()
            conn.close()
            return "Admin registration successful!"

    return render_template('register_admin.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('Admin_KPSTR.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Admin_KPSTR WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user is not None:
            stored_hashed_password = user[2]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
                session['admin'] = username
                return f"Welcome dearest, {username}! KPSTR is so delighted to have you here :)"
            else:
                return "Invalid password. Kindly re-enter the correct password."
        else:
            return "Invalid username. Kindly enter the correct customer username."

    return render_template('login_admin.html')


@app.route('/user/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('usersKPSTR.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usersKPSTR WHERE username = ?", (username,))
        if cursor.fetchone() is not None:
            return "Username already exists. Please choose a different username."
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("INSERT INTO usersKPSTR(username, password) VALUES(?,?)", (username, hashed_password))
            conn.commit()
            conn.close()
            return "Customer registration successful!"

    return render_template('register_user.html')


@app.route('/user/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('usersKPSTR.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usersKPSTR WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user is not None:
            stored_hashed_password = user[2]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
                session['user'] = username
                return f"Welcome dearest, {username}! KPSTR is so delighted to have you explore :)"
            else:
                return "Invalid password. Kindly re-enter the correct password."
        else:
            return "Invalid username. Kindly enter the correct customer username."

    return render_template('login_user.html')


@app.route('/logout')
def logout():
    session.pop('admin', None)
    session.pop('user', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
