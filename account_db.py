import sqlite3

conn = sqlite3.connect("account.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE real_estate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    income_per_hour REAL
);
            """)
conn.commit()
cursor.execute("""CREATE TABLE businesses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    income_per_hour REAL
);
            """)
conn.commit()
cursor.execute("""CREATE TABLE vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    image_path TEXT
);
            """)
conn.commit()
cursor.execute("""CREATE TABLE collections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL
);
            """)
conn.commit()
cursor.execute("""CREATE TABLE crypto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL
); """)
conn.commit()
conn.close()