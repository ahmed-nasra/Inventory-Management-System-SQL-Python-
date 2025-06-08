import sqlite3
from datetime import datetime

# Database setup
def init_db():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Suppliers (
            supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_name TEXT NOT NULL,
            contact_email TEXT UNIQUE,
            phone TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Warehouses (
            warehouse_id INTEGER PRIMARY KEY AUTOINCREMENT,
            warehouse_name TEXT NOT NULL,
            location TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            supplier_id INTEGER,
            unit_price REAL,
            stock_quantity INTEGER,
            warehouse_id INTEGER,
            FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id),
            FOREIGN KEY (warehouse_id) REFERENCES Warehouses(warehouse_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            order_date DATE,
            status TEXT DEFAULT 'Pending'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS OrderDetails (
            order_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id),
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_supplier(supplier_name, contact_email, phone):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.excute('INSERT INTO Suppliers (supplier_name, contact_email, phone VALUES(?,?,?)',
    (supplier_name, contact_email, phone))
    conn.commit()
    conn.close()
    print(f'Supplier {supplier_name} added successfully')

def add_warehouse(warehouse_name, location):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.excute('INSERT INTO Warehouses (warehouse_name, location) VALUES(?,?)',
    (warehouse_name, location))
    conn.commit
    conn.close
    print(f' Warehouse {warehouse_name} added successfully')

def add_product(product_name, supplier_id, unit_price, stock_quantity, warehouse_id):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    cursor.excute('SELECT supplier_id FROM Suppliers WHERE supplier_id = ?', (supplier_id))
    supplier = cursor.fetchone()
    if NOT Supplier:
        print('Supplier is not found')
        conn.close
        return

    cursor.excute('SELECT warehouse_id FROM Warehouses WHERE warehouse_id = ?', (warehouse_id))
    warehouse = cursor.fetchone()
    if NOT Warehouses:
        print('Warehouse is not found')
        conn.close
        return

    cursor.excute('INSERT INTO Products (product_name, supplier_id, unit_price, stock_quantity, warehouse_id) VALUES(?,?,?,?,?)',
    (product_name, supplier_id, unit_price, stock_quantity, warehouse_id))
    conn.commit()
    conn.close()
    print(f'Product {product_name} added successfully')

# Place an order
def place_order(customer_name, product_quantities):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
# Create order
    order_date = datetime.now()
    cursor.execute('INSERT INTO Orders (customer_name, order_date) VALUES (?, ?)',
                  (customer_name, order_date))
    order_id = cursor.lastrowid

# Add order details and update stock
    for product_id, quantity in product_quantities:
        cursor.execute('SELECT stock_quantity FROM Products WHERE product_id = ?', (product_id,))
        product = cursor.fetchone()
        if not product or product[0] < quantity:
            print(f"Insufficient stock for product ID {product_id}.")
            conn.rollback()
            conn.close()
            return

        cursor.execute('INSERT INTO OrderDetails (order_id, product_id, quantity) VALUES (?, ?, ?)',
        (order_id, product_id, quantity))
        cursor.execute('UPDATE Products SET stock_quantity = stock_quantity - ? WHERE product_id = ?',
        (quantity, product_id))
    
    cursor.execute('UPDATE Orders SET status = ? WHERE order_id = ?', ('Completed', order_id))
    conn.commit()
    conn.close()
    print(f"Order {order_id} placed successfully for {customer_name}.")

# View inventory status
def view_inventory():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.product_id, p.product_name, s.supplier_name, p.unit_price, p.stock_quantity, w.warehouse_name
        FROM Products p
        JOIN Suppliers s ON p.supplier_id = s.supplier_id
        JOIN Warehouses w ON p.warehouse_id = w.warehouse_id
    ''')
    
    products = cursor.fetchall()
    print("\nCurrent Inventory:")
    for product in products:
        print(f"ID: {product[0]}, Product: {product[1]}, Supplier: {product[2]}, Price: ${product[3]:.2f}, "
              f"Stock: {product[4]}, Warehouse: {product[5]}")
    
    conn.close()

def main_menu():
    while True:
        print('\n *** Inventory Management System ***')
        print('1. add supplier')
        print('2. add warehouse')
        print('3. add product')
        print('4. place order')
        print('5. view inventory')
        print('6. Exit')

        choice = int(input(Enter your choice))

        if choice == 1:
            supplier_name = input('Enter supplier name')
            contact_email = input('Enter contact email')
            phone = int(input('Enter phone number'))
            add_supplier(supplier_name, contact_email, phone)

        elif choice == 2:
            warehouse_name = input('Enter warehouse name')
            location = input('Enter warehouse location')
            add_warehouse(warehouse_name, location)

        elif choice == 3:
            product_name = input('Enter product name')
            supplier_id = int(input('Enter supplier name'))
            unit_price = float(input('Enter price per unit'))
            stock_quantity = int(input('Enter stock quantity'))
            warehouse_id = int(input('Enter warehouse ID'))
            add_product(product_name, supplier_id, unit_price, stock_quantity, warehouse_id)

        elif choice == 4:
            customer_name = input('Enter customer name')
            product_quantities = int(input('Enter product quantities'))
            place_order(customer_name, product_quantities)

        elif choice == 5:
            view_inventory()

        elif choice == 6:
            print('Exit')
            break

        else:
            print('Invalid choice')
