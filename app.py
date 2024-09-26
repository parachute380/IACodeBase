from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from getpass import getpass
import bcrypt;
from templates.vendorDetails import vendor_menu


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


@app.route('/businessChoice', methods=['GET', 'POST'])
def business_menu():
    if request.method == 'POST':
        choice = request.form['choice']
        db_name = request.form['db_name']

        if choice == '1':
            return redirect(url_for('add_vendor', db_name=db_name))
        elif choice == '2':
            return redirect(url_for('edit_vendor', db_name=db_name))  # You may want to add vendor_id for editing
        elif choice == '3':
            return redirect(url_for('delete_vendor', db_name=db_name))  # You may want to add vendor_id for deletion
        elif choice == '4':
            return redirect(url_for('view_vendors', db_name=db_name))
        elif choice == '5':
            return redirect(url_for('home'))
        else:
            return "Invalid choice. Please try again."

    return render_template('business_menu.html')


@app.route('/vendor/add/<db_name>', methods=['GET', 'POST'])
def add_vendor(db_name):
    if request.method == 'POST':
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Fetch data from the form
        name = request.form['name']
        contact_info = request.form['contact_info']
        website = request.form['website']
        item_descriptions = request.form['item_descriptions']
        images = request.form['images']
        shipping_costs = float(request.form['shipping_costs'])
        payment_terms = request.form['payment_terms']
        lead_time = request.form['lead_time']
        return_policy = request.form['return_policy']
        payment_history = request.form['payment_history']

        # Insert into the database
        cursor.execute('''
        INSERT INTO vendors (
            name, contact_info, website, item_descriptions, images, 
            shipping_costs, payment_terms, lead_time, return_policy, payment_history
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, contact_info, website, item_descriptions, images,
              shipping_costs, payment_terms, lead_time, return_policy, payment_history))

        conn.commit()
        conn.close()
        return render_template('vendor_added.html', name=name)  # Success page
    return render_template('add_vendor.html')  # Render the form on GET request



def edit_vendor(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    vendor_id = int(input("Enter Vendor ID to edit: "))

    name = input("Enter Vendor Name: ")
    contact_info = input("Enter Contact Number: ")
    website = input("Enter Website URL: ")
    item_descriptions = input("Enter Item Descriptions: ")
    images = input("Enter Images (comma-separated paths): ")
    lead_time = input("Enter Lead Time of Production: ")
    shipping_costs = float(input("Enter Shipping Costs: "))
    payment_terms = input("Enter Payment Terms: ")
    return_policy = input("Enter Return Policy: ")
    payment_history = input("Enter Payment History: ")

    cursor.execute('''
    UPDATE vendors SET 
        name = ?, contact_info = ?, website = ?, item_descriptions = ?, images = ?, 
        shipping_costs = ?, payment_terms = ?, lead-time = ?, return_policy = ?, payment_history = ?
    WHERE id = ?
    ''', (name, contact_info, website, item_descriptions, images, shipping_costs,
          payment_terms, return_policy, payment_history, vendor_id))

    conn.commit()
    conn.close()
    print("Vendor Details updated successfully!")


def delete_vendor(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    vendor_id = int(input("Enter Vendor ID to delete: "))

    cursor.execute('DELETE FROM vendors WHERE id = ?', (vendor_id,))

    conn.commit()
    conn.close()
    print("Vendor deleted successfully!")

def view_vendors(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM vendors')
    vendors = cursor.fetchall()

    for vendor in vendors:
        print(f"ID: {vendor['id']}")
        print(f"Name: {vendor['name']}")
        print(f"Contact Info: {vendor['contact_info']}")
        print(f"Website: {vendor['website']}")
        print(f"Item Descriptions: {vendor['item_descriptions']}")
        print(f"Images: {vendor['images']}")
        print(f"Shipping Costs: {vendor['shipping_costs']}")
        print(f"Payment Terms: {vendor['payment_terms']}")
        print(f"Lead Time of Production: {vendor['lead_time']}")
        print(f"Return Policy: {vendor['return_policy']}")
        print(f"Payment History: {vendor['payment_history']}")
        print('-' * 40)

    conn.close()


def main():
    businesses = {
        '1': 'Khatipatang.db',
        '2': 'Sajili.db',
        '3': 'Ratnakari.db'
    }

    while True:
        print("\nSelect a Business:")
        print("1. Khatipatang")
        print("2. Sajili")
        print("3. Ratnakari")
        print("4. Exit")
        choice = input("Choose an option:")

        if choice in businesses.keys():
            db_name = businesses[choice]
            print(f"\nYou selected business: {db_name}")
            business_menu(db_name)  # Now correctly passing db_name as an argument
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    app.run(debug=True)


def business_menu(db_name):
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Vendor Management")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register_user(db_name)
        elif choice == '2':
            if login_user(db_name):
                vendor_menu(db_name)
        elif choice == '3':
            vendor_menu(db_name)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")
