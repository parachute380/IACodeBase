import sqlite3
from getpass import getpass
import bcrypt


def init_db():
    conn = sqlite3.connect('VendorDetails.db')
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
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        contact_info INTEGER,
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


def add_vendor(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    name = input("Enter Supplier Name: ")
    contact_info = input("Enter Contact Number: ")
    website = input("Enter Website URL: ")
    item_descriptions = input("Enter Item Descriptions: ")
    images = input("Enter Images (comma-separated paths): ")
    shipping_costs = float(input("Enter Shipping Costs: "))
    payment_terms = input("Enter Payment Method: ")
    lead_time = input("Enter Lead Time of Production: ")
    return_policy = input("Enter Return Policy: ")
    payment_history = input("Enter Payment History: ")

    cursor.execute('''
    INSERT INTO vendors (
        name, contact_info, website, item_descriptions, images, 
        object_specifications, min_order_quantity, shipping_costs, 
        payment_terms, payment_schedules, return_policy, payment_history
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, contact_info, website, item_descriptions, images,
          object_specifications, min_order_quantity, shipping_costs,
          payment_terms, payment_schedules, return_policy, payment_history))

    conn.commit()
    conn.close()
    print("Vendor added successfully!")


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

    cursor.execute('DELETE FROM VendorDetails WHERE id = ?', (vendor_id,))

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


def vendor_menu(db_name):
    while True:
        print("\nVendor Details Management:")
        print("1. Add Vendor")
        print("2. Edit Vendor")
        print("3. Delete Vendor")
        print("4. View Vendors")
        print("5. Back")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_vendor(db_name)
        elif choice == '2':
            edit_vendor(db_name)
        elif choice == '3':
            delete_vendor(db_name)
        elif choice == '4':
            view_vendors(db_name)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


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
