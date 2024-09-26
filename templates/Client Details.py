import sqlite3
from getpass import getpass
import bcrypt


def init_db():
    conn = sqlite3.connect('ClientDetails.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vendors (
        client_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        phone_number INTEGER,
        email_address TEXT,
        item_name TEXT,
        quantity_ordered INTEGER,
        shipping_address TEXT,
        shipping_cost INTEGER,
        payment_terms TEXT,
        customised BOOLEAN,
        order_specifications TEXT,
        lead_time INTEGER,
        delivery_date INTEGER,
        order_history TEXT,
        return_policy TEXT
        
    )
    ''')
    conn.commit()
    conn.close()


def register_user(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    username = input("Enter username: ")
    password = getpass("Enter password: ")

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is not None:
        print("Username already exists. Please choose a different username.")
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("User registered successfully!")

    conn.close()


def login_user(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    username = input("Enter username: ")
    password = getpass("Enter password: ")

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user is not None:
        stored_hashed_password = user['password']
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
            print(f"Welcome, {username}!")
            return True
        else:
            print("Invalid password.")
    else:
        print("Invalid username.")
    conn.close()
    return False


def add_clients(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    name = input("Enter Client Name: ")
    phone_number = input("Enter Phone Number: ")
    email_address = input("Enter Email Address: ")
    item_name = input("Enter Item Name: ")
    quantity_ordered = input("Enter Quantity Ordered")
    shipping_address = float(input("Enter Shipping Address: "))
    shipping_cost = input("Enter Shipping Cost:")
    payment_terms = input("Enter Payment Method: ")
    customised = input("Enter If Customised or Not: ")
    order_specifications = input("Enter Return Policy: ")
    lead_time = input("Enter Lead Time of Production:")
    order_history = input("Enter Payment History: ")
    delivery_date = input("Enter Date of Delivery: ")
    return_policy = input("Enter Return Policy:")

    cursor.execute('''
    INSERT INTO vendors (
        name, phone_number, email_address, item_name, quantity_ordered, 
        shipping_address, shipping_cost, payment_terms, customised, order_specifications,
        lead_time, order_history, delivery_date, return_policy
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, phone_number, email_address, item_name, quantity_ordered,
          shipping_address, shipping_cost, payment_terms, customised, return_policy,
          order_specifications, lead_time, order_history, delivery_date))

    conn.commit()
    conn.close()
    print("Client Details added successfully!")


def edit_clients(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    client_id = int(input("Enter Client ID to edit: "))

    name = input("Enter Client Name: ")
    phone_number = input("Enter Phone Number: ")
    email_address = input("Enter Email Address: ")
    item_name = input("Enter Item Name: ")
    quantity_ordered = input("Enter Quantity Ordered")
    shipping_address = float(input("Enter Shipping Address: "))
    shipping_cost = input("Enter Shipping Cost:")
    payment_terms = input("Enter Payment Method: ")
    customised = input("Enter If Customised or Not: ")
    order_specifications = input("Enter Return Policy: ")
    lead_time = input("Enter Lead Time of Production:")
    order_history = input("Enter Payment History: ")
    delivery_date = input("Enter Date of Delivery: ")
    return_policy = input("Enter Return Policy:")

    cursor.execute('''
        INSERT INTO vendors (
            name, phone_number, email_address, item_name, quantity_ordered, 
            shipping_address, shipping_cost, payment_terms, customised, order_specifications,
            lead_time, order_history, delivery_date, return_policy
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, phone_number, email_address, item_name, quantity_ordered,
              shipping_address, shipping_cost, payment_terms, customised, return_policy,
              order_specifications, lead_time, order_history, delivery_date))

    conn.commit()
    conn.close()
    print("Client Details updated successfully!")


def delete_clients(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    client_id = int(input("Enter Client ID to delete: "))

    cursor.execute('DELETE FROM clients WHERE id = ?', (vendor_id,))

    conn.commit()
    conn.close()
    print("Client details deleted successfully!")


def view_clients(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM clients')
    clients = cursor.fetchall()

    for client in clients:
        print(f"ID: {client['id']}")
        print(f"Name: {client['name']}")
        print(f"Phone Number: {client['phone_number']}")
        print(f"Email Address: {client['email_address']}")
        print(f"Item Name: {client['item_name']}")
        print(f"Quantity Ordered: {client['quantity_ordered']}")
        print(f"Shipping Address: {client['shipping_address']}")
        print(f"Shipping Cost: {client['shipping_cost']}")
        print(f"Payment Terms: {client['payment_terms']}")
        print(f"Customised? {client['customised']}")
        print(f"Order Specifications: {client['order_specifications']}")
        print(f"Lead Time of Production: {client['lead_time']}")
        print(f"Delivery Date: {client['delivery_date']}")
        print(f"Order History: {client['order_history']}")
        print(f"Return Policy: {client['return_policy']}")
        print('-' * 40)

    conn.close()


def client_menu(db_name):
    while True:
        print("\nVendor Details Management:")
        print("1. Add Client")
        print("2. Edit Client")
        print("3. Delete Client")
        print("4. View Clients")
        print("5. Back")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_clients(db_name)
        elif choice == '2':
            edit_clients(db_name)
        elif choice == '3':
            delete_clients(db_name)
        elif choice == '4':
            view_clients(db_name)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


def business_menu(db_name):
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Vendor Management")
        print("4. Client Management")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register_user(db_name)
        elif choice == '2':
            if login_user(db_name):
                client_menu(db_name)
        elif choice == '3':
            vendor_menu(db_name)
        elif choice == '4':
            client_menu(db_name)
        elif choice == '5' :
            break
        else:
            print("Invalid choice. Please try again.")

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
        choice = input("Enter your choice: ")

        if choice in businesses:
            business_menu(businesses[choice])
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
