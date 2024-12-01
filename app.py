from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from getpass import getpass
import bcrypt;
from vendorDetails import vendor_menu


app = Flask(__name__)
app.secret_key = 'your_secret_key'


# Initialize the databases
def init_db():
    # Initialize the admin database
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

    # Initialize the users database
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

    # Initialize the business databases
    for db_name in ['Khatipatang.db', 'Sajili.db', 'Ratnakari.db']:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            contact_info TEXT,
            website TEXT,
            item_descriptions TEXT,
            images TEXT,
            shipping_costs REAL,
            payment_terms TEXT,
            lead_time TEXT,
            return_policy TEXT,
            payment_history TEXT
        )
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
        vendor_id = request.form.get('vendor_id')  # Retrieve Vendor ID if provided

        if choice == '1':  # Add Vendor
            return redirect(url_for('add_vendor', db_name=db_name))
        elif choice == '2':  # Edit Vendor
            if not vendor_id:
                return "Vendor ID is required for editing."
            return redirect(url_for('edit_vendor', db_name=db_name, vendor_id=vendor_id))
        elif choice == '3':  # Delete Vendor
            if not vendor_id:
                return "Vendor ID is required for deletion."
            return redirect(url_for('delete_vendor', db_name=db_name, vendor_id=vendor_id))
        elif choice == '4':  # View Vendors
            return redirect(url_for('view_vendors', db_name=db_name))
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
        return redirect(url_for('view_vendors', db_name=db_name))
    return render_template('add_vendor.html', db_name=db_name)


@app.route('/vendor/edit/<db_name>/<int:vendor_id>', methods=['GET', 'POST'])
def edit_vendor(db_name, vendor_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    if request.method == 'POST':
        # Fetch updated data from the form
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

        # Update the vendor in the database
        cursor.execute('''
        UPDATE vendors
        SET name = ?, contact_info = ?, website = ?, item_descriptions = ?, images = ?,
            shipping_costs = ?, payment_terms = ?, lead_time = ?, return_policy = ?, payment_history = ?
        WHERE id = ?
        ''', (name, contact_info, website, item_descriptions, images,
              shipping_costs, payment_terms, lead_time, return_policy, payment_history, vendor_id))
        conn.commit()
        conn.close()

        return redirect(url_for('view_vendors', db_name=db_name))

    # Fetch vendor details for GET request
    cursor.execute('SELECT * FROM vendors WHERE id = ?', (vendor_id,))
    vendor = cursor.fetchone()
    conn.close()

    if not vendor:
        return "Vendor not found.", 404

    # Convert vendor row into a dictionary for easier handling in the template
    vendor_dict = {
        'id': vendor[0],
        'name': vendor[1],
        'contact_info': vendor[2],
        'website': vendor[3],
        'item_descriptions': vendor[4],
        'images': vendor[5],
        'shipping_costs': vendor[6],
        'payment_terms': vendor[7],
        'lead_time': vendor[8],
        'return_policy': vendor[9],
        'payment_history': vendor[10],
    }

    return render_template('edit_vendor.html', vendor=vendor_dict, db_name=db_name)



@app.route('/vendor/delete/<db_name>/<int:vendor_id>', methods=['POST'])
def delete_vendor(db_name, vendor_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM vendors WHERE id = ?', (vendor_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('view_vendors', db_name=db_name))


@app.route('/vendor/view/<db_name>', methods=['GET'])
def view_vendors(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM vendors')
    vendors = cursor.fetchall()
    conn.close()

    return render_template('view_vendors.html', vendors=vendors, db_name=db_name)

@app.route('/init_db')
def initialize_database():
    init_db()
    return "Databases initialized successfully!"

@app.route('/check_tables/<db_name>')
def check_tables(db_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        return f"Tables in {db_name}: {tables}"
    except sqlite3.Error as e:
        return f"Error checking tables in {db_name}: {str(e)}"

@app.route('/fix_table/<db_name>')
def fix_table(db_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            contact_info TEXT,
            website TEXT,
            item_descriptions TEXT,
            images TEXT,
            shipping_costs REAL,
            payment_terms TEXT,
            lead_time TEXT,
            return_policy TEXT,
            payment_history TEXT
        )
        ''')
        conn.commit()
        conn.close()
        return f"Vendors table created successfully in {db_name}."
    except sqlite3.Error as e:
        return f"Error creating table in {db_name}: {str(e)}"



if __name__ == "__main__":
    init_db()
    app.run(debug=True)