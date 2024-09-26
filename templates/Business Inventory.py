import sqlite3

# Initialize the database with tables for raw materials, WIP, finished goods, and clients
def init_inventory_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create Raw Materials Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS raw_materials (
        id INTEGER PRIMARY KEY,
        material_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        supplier TEXT,
        cost REAL
    )
    ''')

    # Create WIP Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS wip (
        id INTEGER PRIMARY KEY,
        item_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        progress_percentage REAL
    )
    ''')

    # Create Finished Goods Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS finished_goods (
        id INTEGER PRIMARY KEY,
        item_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        client_id INTEGER,
        FOREIGN KEY(client_id) REFERENCES clients(id)
    )
    ''')

    # Create Clients Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        contact_info TEXT
    )
    ''')

    conn.commit()
    conn.close()

# CRUD operations for Raw Materials
def add_raw_material(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    material_name = input("Enter Raw Material Name: ")
    quantity = int(input("Enter Quantity: "))
    supplier = input("Enter Supplier Name: ")
    cost = float(input("Enter Cost: "))

    cursor.execute('''
    INSERT INTO raw_materials (material_name, quantity, supplier, cost)
    VALUES (?, ?, ?, ?)
    ''', (material_name, quantity, supplier, cost))

    conn.commit()
    conn.close()
    print("Raw material added successfully!")

def edit_raw_material(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    material_id = int(input("Enter Raw Material ID to edit: "))
    material_name = input("Enter new Raw Material Name: ")
    quantity = int(input("Enter new Quantity: "))
    supplier = input("Enter new Supplier Name: ")
    cost = float(input("Enter new Cost: "))

    cursor.execute('''
    UPDATE raw_materials SET material_name = ?, quantity = ?, supplier = ?, cost = ?
    WHERE id = ?
    ''', (material_name, quantity, supplier, cost, material_id))

    conn.commit()
    conn.close()
    print("Raw material updated successfully!")

def delete_raw_material(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    material_id = int(input("Enter Raw Material ID to delete: "))
    cursor.execute('DELETE FROM raw_materials WHERE id = ?', (material_id,))

    conn.commit()
    conn.close()
    print("Raw material deleted successfully!")

def view_raw_materials(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM raw_materials')
    materials = cursor.fetchall()

    for material in materials:
        print(f"ID: {material[0]}, Name: {material[1]}, Quantity: {material[2]}, Supplier: {material[3]}, Cost: {material[4]}")

    conn.close()

# Work in Progress (WIP) Update
def add_wip(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    item_name = input("Enter WIP Item Name: ")
    quantity = int(input("Enter Quantity: "))
    progress_percentage = float(input("Enter Progress Percentage (0-100): "))

    cursor.execute('''
    INSERT INTO wip (item_name, quantity, progress_percentage)
    VALUES (?, ?, ?)
    ''', (item_name, quantity, progress_percentage))

    conn.commit()
    conn.close()
    print("WIP added successfully!")

def update_wip(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    wip_id = int(input("Enter WIP ID to update: "))
    progress_percentage = float(input("Enter new Progress Percentage (0-100): "))

    cursor.execute('''
    UPDATE wip SET progress_percentage = ? WHERE id = ?
    ''', (progress_percentage, wip_id))

    conn.commit()
    conn.close()
    print("WIP updated successfully!")

def view_wip(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM wip')
    wip_items = cursor.fetchall()

    for wip in wip_items:
        print(f"ID: {wip[0]}, Name: {wip[1]}, Quantity: {wip[2]}, Progress: {wip[3]}%")

    conn.close()

# Finished Goods and Client Management
def add_finished_goods(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    item_name = input("Enter Finished Goods Item Name: ")
    quantity = int(input("Enter Quantity: "))
    client_id = int(input("Enter Client ID: "))

    cursor.execute('''
    INSERT INTO finished_goods (item_name, quantity, client_id)
    VALUES (?, ?, ?)
    ''', (item_name, quantity, client_id))

    conn.commit()
    conn.close()
    print("Finished goods added successfully!")

def view_finished_goods(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT finished_goods.id, finished_goods.item_name, finished_goods.quantity, clients.name
    FROM finished_goods
    JOIN clients ON finished_goods.client_id = clients.id
    ''')

    finished_goods_list = cursor.fetchall()

    for fg in finished_goods_list:
        print(f"ID: {fg[0]}, Name: {fg[1]}, Quantity: {fg[2]}, Client: {fg[3]}")

    conn.close()

def add_client(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    client_name = input("Enter Client Name: ")
    contact_info = input("Enter Contact Info: ")

    cursor.execute('''
    INSERT INTO clients (name, contact_info)
    VALUES (?, ?)
    ''', (client_name, contact_info))

    conn.commit()
    conn.close()
    print("Client added successfully!")

def view_clients(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM clients')
    clients = cursor.fetchall()

    for client in clients:
        print(f"ID: {client[0]}, Name: {client[1]}, Contact Info: {client[2]}")

    conn.close()

# Main menu to manage the inventory
def inventory_menu(db_name):
    while True:
        print("\nInventory Management System:")
        print("1. Add Raw Material")
        print("2. Edit Raw Material")
        print("3. Delete Raw Material")
        print("4. View Raw Materials")
        print("5. Add WIP")
        print("6. Update WIP")
        print("7. View WIP")
        print("8. Add Finished Goods")
        print("9. View Finished Goods")
        print("10. Add Client")
        print("11. View Clients")
        print("12. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_raw_material(db_name)
        elif choice == '2':
            edit_raw_material(db_name)
        elif choice == '3':
            delete_raw_material(db_name)
        elif choice == '4':
            view_raw_materials(db_name)
        elif choice == '5':
            add_wip(db_name)
        elif choice == '6':
            update_wip(db_name)
        elif choice == '7':
            view_wip(db_name)
        elif choice == '8':
            add_finished_goods(db_name)
        elif choice == '9':
            view_finished_goods(db_name)
        elif choice == '10':
            add_client(db_name)
        elif choice == '11':
            view_clients(db_name)
        elif choice == '12':
            break
        else:
            print("Invalid choice. Please try again.")

# Initialize the inventory database and run the menu
if __name__ == "__main__":
    db_name = "business_inventory.db"
    init_inventory_db(db_name)
    inventory_menu(db_name)
