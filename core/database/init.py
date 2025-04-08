# app/sqlite_init.py

import sqlite3
import os

DB_PATH = os.getenv("DATABASE_PATH", "./data/flight.db")

def init_db(mode="prod"):

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Création table customers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        title TEXT,
        lastname TEXT,
        firstname TEXT,
        postal_code TEXT,
        city TEXT,
        email TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchases (
        purchase_identifier TEXT PRIMARY KEY,
        product_id TEXT,
        quantity INTEGER,
        price REAL,
        currency TEXT,
        date TEXT,
        customer_id INTEGER,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    """)
    conn.commit()
    conn.close()
