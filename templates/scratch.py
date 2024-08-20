import _sqlite3
import sqlite3
from getpass import getpass

import bcrypt


def init_db(KPSTR):
    conn = sqlite3.connect('KPSTR.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
    )
    ''')

def register_user(registrations_KPSTR, hashed_password=None):
    conn = sqlite3.connect(registrations_KPSTR.db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    username = input("Enter username")
    password = getpass("Enter password")

    #Check if the username already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is not None:
        print("Username already exists. Please choose a different username.")
    else:
       hashed password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
       cursor.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, hashed_password))
       conn.commit()
       print("Admin registration sucessful! Welcome to KPSTR!")
    conn.close()

def login_user(login_KPSTR: )
    conn = _sqlite3.connect(login_KPSTR.db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    username = input("Enter username:")
    password = getpass("Enter password:")

    #Check if user exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user is not None:
        stored_hashed_password = user['password']

        #Verify the password
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
            print("Welcome, {username}, it is great to see you here!")
        else
            print("Invalid password.")
    else:
        print("Invalid username.")

    conn.close()


def logout_admin():
     pass


def business_menu(KPSTR):
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("enter your choice:")

        if choice == '1':
            register_user(registrations_KPSTR)
        elif choice == '2':
            login_user(login_KPSTR=)
        elif choice == '3':
            logout_admin()
        else:
            print("Invalid choices. Please try again.")

def main():
    businesses = {
        '1': 'Khatipatang.db',
        '2': 'Sweet Tickles.db',
        '3': 'Ratnakari.db'
    }

#Initialize Database
for db in businesses.values():
    init_db(KPSTR=)

while True:
    print("\nSelect a Business:")
    print("1. Khatipatang")
    print("2. Sweet Tickles")
    print("3. Ratnakari")
    print("4. Exit")
    choice = input("Choose an option:")

    if choice in businesses:
        business_menu(businesses[choice])
    elif choice == '4':
        logout_admin()
    else:
        print("Invalid Choice. Please try again.")

if __name__ == "__main__":
    main()



















