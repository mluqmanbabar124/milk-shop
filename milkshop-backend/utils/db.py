import sqlite3
from werkzeug.security import generate_password_hash
import os

DB_PATH = 'milkshop.db'


def get_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=DB_PATH, init_admin=False):
    # Delete old DB if you want a clean start
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🧹 Old database deleted — creating fresh schema...")

    conn = get_db(db_path)
    cur = conn.cursor()

    cur.executescript('''
    -- USERS TABLE
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone_number TEXT,
        role TEXT,
        login_name TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    );

    -- SUPPLIERS TABLE
    CREATE TABLE suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT,
        phone TEXT
    );

    -- UNIT OF MEASUREMENT
    CREATE TABLE unit_of_measurement (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );

    -- MILK PRODUCTS
    CREATE TABLE milk_products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        weight REAL,
        unit_id INTEGER,
        supplier_id INTEGER,
        FOREIGN KEY (unit_id) REFERENCES unit_of_measurement(id),
        FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
    );

    -- MONTHLY CUSTOMERS
    CREATE TABLE monthly_customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone_number TEXT,
        house_number TEXT,
        full_address TEXT,
        product_id INTEGER,
        set_rate REAL,
        FOREIGN KEY (product_id) REFERENCES milk_products(id)
    );

    -- WALK-IN SALES
    CREATE TABLE walkin_sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        product_id INTEGER,
        name TEXT,
        rate REAL,
        amount REAL,
        unit_id INTEGER,
        FOREIGN KEY (product_id) REFERENCES milk_products(id),
        FOREIGN KEY (unit_id) REFERENCES unit_of_measurement(id)
    );

    -- MONTHLY SUPPLY RECORDS
    CREATE TABLE monthly_supply (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monthly_customer_id INTEGER,
        product_id INTEGER,
        date TEXT NOT NULL,
        set_rate REAL,
        milk_received INTEGER DEFAULT 0,
        FOREIGN KEY (monthly_customer_id) REFERENCES monthly_customers(id),
        FOREIGN KEY (product_id) REFERENCES milk_products(id)
    );
    ''')

    conn.commit()

    if init_admin:
        try:
            pw_hash = generate_password_hash('1234')
            cur.execute('INSERT INTO users (name, login_name, password_hash, role) VALUES (?, ?, ?, ?)',
                        ('Admin', 'admin', pw_hash, 'admin'))
            conn.commit()
            print("✅ Default admin created (username: admin, password: 1234)")
        except Exception as e:
            print("⚠️ Error creating admin:", e)

    conn.close()
    print("✅ Database initialized successfully!")


if __name__ == "__main__":
    init_db(init_admin=True)
