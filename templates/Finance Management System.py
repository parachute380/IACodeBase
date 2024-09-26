import sqlite3

# Initialize the database with tables for Costs, Revenue, and Assets
def init_finance_db():
    conn = sqlite3.connect(Financial Information.db)
    cursor = conn.cursor()

    # Create Costs Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS costs (
        id INTEGER PRIMARY KEY,
        cost_name TEXT NOT NULL,
        amount REAL NOT NULL,
    )
    ''')

    # Create Revenue Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS revenue (
        id INTEGER PRIMARY KEY,
        revenue_name TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT
    )
    ''')

    # Create Assets Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY,
        asset_name TEXT NOT NULL,
        value REAL NOT NULL,
        description TEXT
    )
    ''')

    conn.commit()
    conn.close()

# CRUD operations for Costs
def add_cost(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cost_name = input("Enter Cost Name: ")
    amount = float(input("Enter Amount: "))

    cursor.execute('''
    INSERT INTO costs (cost_name, amount)
    VALUES (?, ?, ?)
    ''', (cost_name, amount))

    conn.commit()
    conn.close()
    print("Costs added successfully!")

def edit_cost(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cost_id = int(input("Enter Cost ID to edit: "))
    cost_name = input("Enter new Cost Name: ")
    amount = float(input("Enter new Amount: "))

    cursor.execute('''
    UPDATE costs SET cost_name = ?, amount = ?, description = ?
    WHERE id = ?
    ''', (cost_name, amount, cost_id))

    conn.commit()
    conn.close()
    print("Costs updated successfully!")

def delete_cost(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cost_id = int(input("Enter Cost ID to delete: "))
    cursor.execute('DELETE FROM costs WHERE id = ?', (cost_id,))

    conn.commit()
    conn.close()
    print("Costs deleted successfully!")

def view_costs(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM costs')
    costs = cursor.fetchall()

    for cost in costs:
        print(f"ID: {cost[0]}, Name: {cost[1]}, Amount: {cost[2]}")

    conn.close()

# CRUD operations for Revenue
def add_revenue(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    revenue_name = input("Enter Revenue Name: ")
    amount = float(input("Enter Amount: "))
    description = input("Enter Description (optional): ")

    cursor.execute('''
    INSERT INTO revenue (revenue_name, amount, description)
    VALUES (?, ?, ?)
    ''', (revenue_name, amount, description))

    conn.commit()
    conn.close()
    print("Revenue added successfully!")

def edit_revenue(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    revenue_id = int(input("Enter Revenue ID to edit: "))
    revenue_name = input("Enter new Revenue Name: ")
    amount = float(input("Enter new Amount: "))
    description = input("Enter new Description (optional): ")

    cursor.execute('''
    UPDATE revenue SET revenue_name = ?, amount = ?, description = ?
    WHERE id = ?
    ''', (revenue_name, amount, description, revenue_id))

    conn.commit()
    conn.close()
    print("Revenue updated successfully!")

def delete_revenue(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    revenue_id = int(input("Enter Revenue ID to delete: "))
    cursor.execute('DELETE FROM revenue WHERE id = ?', (revenue_id,))

    conn.commit()
    conn.close()
    print("Revenue deleted successfully!")

def view_revenue(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM revenue')
    revenue = cursor.fetchall()

    for rev in revenue:
        print(f"ID: {rev[0]}, Name: {rev[1]}, Amount: {rev[2]}, Description: {rev[3]}")

    conn.close()

# CRUD operations for Assets
def add_asset(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    asset_name = input("Enter Asset Name: ")
    value = float(input("Enter Asset Value: "))
    description = input("Enter Description (optional): ")

    cursor.execute('''
    INSERT INTO assets (asset_name, value, description)
    VALUES (?, ?, ?)
    ''', (asset_name, value, description))

    conn.commit()
    conn.close()
    print("Asset added successfully!")

def edit_asset(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    asset_id = int(input("Enter Asset ID to edit: "))
    asset_name = input("Enter new Asset Name: ")
    value = float(input("Enter new Asset Value: "))
    description = input("Enter new Description (optional): ")

    cursor.execute('''
    UPDATE assets SET asset_name = ?, value = ?, description = ?
    WHERE id = ?
    ''', (asset_name, value, description, asset_id))

    conn.commit()
    conn.close()
    print("Asset updated successfully!")

def delete_asset(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    asset_id = int(input("Enter Asset ID to delete: "))
    cursor.execute('DELETE FROM assets WHERE id = ?', (asset_id,))

    conn.commit()
    conn.close()
    print("Asset deleted successfully!")

def view_assets(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM assets')
    assets = cursor.fetchall()

    for asset in assets:
        print(f"ID: {asset[0]}, Name: {asset[1]}, Value: {asset[2]}, Description: {asset[3]}")

    conn.close()

# Financial Report: Summarize total costs, revenue, and assets
def financial_report(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Total Costs
    cursor.execute('SELECT SUM(amount) FROM costs')
    total_cost = cursor.fetchone()[0] or 0

    # Total Revenue
    cursor.execute('SELECT SUM(amount) FROM revenue')
    total_revenue = cursor.fetchone()[0] or 0

    # Total Asset Value
    cursor.execute('SELECT SUM(value) FROM assets')
    total_assets = cursor.fetchone()[0] or 0

    conn.close()

    print(f"Total Costs: {total_cost}")
    print(f"Total Revenue: {total_revenue}")
    print(f"Total Asset Value: {total_assets}")

# Main menu to manage finances
def finance_menu(db_name):
    while True:
        print("\nFinance Management System:")
        print("1. Add Cost")
        print("2. Edit Cost")
        print("3. Delete Cost")
        print("4. View Costs")
        print("5. Add Revenue")
        print("6. Edit Revenue")
        print("7. Delete Revenue")
        print("8. View Revenue")
        print("9. Add Asset")
        print("10. Edit Asset")
        print("11. Delete Asset")
        print("12. View Assets")
        print("13. Financial Report")
        print("14. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_cost(db_name)
        elif choice == '2':
            edit_cost(db_name)
        elif choice == '3':
            delete_cost(db_name)
        elif choice == '4':
            view_costs(db_name)
        elif choice == '5':
            add_revenue(db_name)
        elif choice == '6':
            edit_revenue(db_name)
        elif choice == '7':
            delete_revenue(db_name)
        elif choice == '8':
            view_revenue(db_name)
        elif choice == '9':
            add_asset(db_name)
        elif choice == '10':
            edit_asset(db_name)
        elif choice == '11':
            delete_asset(db_name)
        elif choice == '12':
            view_assets(db_name)
        elif choice == '13':
            financial_report(db_name)
        elif choice == '14':
            break
        else:
            print("Invalid choice. Please try again.")

# Initialize the finance database and run the menu
if __name__ == "__main__":
    db_name = "finance_management.db"
    init_finance_db(db_name)
    finance_menu(db_name)
