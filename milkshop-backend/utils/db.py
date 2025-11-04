
import sqlite3
from werkzeug.security import generate_password_hash
import os

def get_db(db_path='milkshop.db'):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path='milkshop.db', init_admin=False):
    need_create = not os.path.exists(db_path)
    conn = get_db(db_path)
    cur = conn.cursor()

    cur.executescript('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS milk_supply (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        milk_type TEXT,
        liters REAL,
        rate REAL,
        total_amount REAL
    );

    CREATE TABLE IF NOT EXISTS walkin_sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        customer_name TEXT,
        liters REAL,
        rate REAL,
        total_amount REAL
    );

    CREATE TABLE IF NOT EXISTS monthly_customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact TEXT,
        milk_type TEXT,
        rate_per_liter REAL,
        active INTEGER DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS monthly_supply (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        date TEXT NOT NULL,
        liters REAL,
        FOREIGN KEY (customer_id) REFERENCES monthly_customers(id)
    );

    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT,
        amount REAL,
        note TEXT
    );
    ''')

    conn.commit()

    # create default admin on first create and when requested
    if init_admin and need_create:
        try:
            pw_hash = generate_password_hash('1234')
            cur.execute('INSERT OR IGNORE INTO users (username, password_hash) VALUES (?,?)', ('admin', pw_hash))
            conn.commit()
        except Exception as e:
            print('Error creating admin user:', e)

    conn.close()

