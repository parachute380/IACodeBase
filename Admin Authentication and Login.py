import sqlite3
from getpass import getpass
import bcrypt

def init_db():
    conn = sqlite3.connect('Admin_KPSTR.db')
    cursor = conn.cursor()
    cursor.execute(''
                   'CREATE TABLE IF NOT EXIST Admin_KPSTR('
                   'id INTEGER PRIMARY KEY,'
                   'username TEXT UNIQUE NOT NULL,'
                   'password TEXT NOT NULL'''''')
    ''')
    conn.commit()
    conn.close()

def register_admin():
    conn = sqlite3.connect('Admin_KPSTR.db')
    cursor = conn.cursor()

    username = input("Enter username:")
    password = getpass("Enter password:")

    cursor.execute("SELECT * FROM users WHERE username = ?, (username)")
    if cursor.fetchone() is not None:
        print("Username already exists. Please choose a different username.")
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

        cursor.execute("INSERT INTO users(username, password) VALUES(?,?)", (username, hashed_password))
        conn.commit()
        print("Admin registration Successful!")

    conn.close()

def login_admin():
    conn = sqlite3.connect('Admin_KPSTR.db')
    cursor = conn.cursor()

    username = input("Enter username:")
    password = getpass("Enter password:")

    cursor.execute("SELECT * FROM users WHERE username = ?", (username))
    user = cursor.fetchone()
    if user is not None:
        stored_hashed_password = user[2]

        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
            print("Welcome dearest, {username}! KPSTR is so delighted to have you here :)")
        else:
            print("Invalid password. Kindly re-enter the correct password.")
    else:
        print("Invalid username. Kindly enter the correct customer username.")

    conn.close()


def main():
    init_db()
    while True:
        print("1. Register")
        print("2.Login")
        print("3.Exit")
        choice = input("Enter your choice:")

        if choice == '1':
            register_user()
        elif choice == '2':
            login_user()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please choose from the available options.")

if __name__ == "_main_":
    main()

    
