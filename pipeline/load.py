import sqlite3
from typing import List, Dict

def run_loading(data_list: List[Dict], db_path: str = "data/pipeline_database.db"):
    print(" Starting Loading Phase...")
    
    # Connects to the database file (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create target table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            country TEXT,
            age INTEGER
        )
    """)
    
    # Insert records using UPSERT logic (Update if exists, insert if new)
    cursor.executemany("""
        INSERT INTO users (id, first_name, last_name, email, country, age)
        VALUES (:id, :first_name, :last_name, :email, :country, :age)
        ON CONFLICT(id) DO UPDATE SET
            first_name=excluded.first_name,
            last_name=excluded.last_name,
            email=excluded.email,
            country=excluded.country,
            age=excluded.age
    """, data_list)
    
    conn.commit()
    
    # Verification check print
    cursor.execute("SELECT COUNT(*) FROM users")
    total_rows = cursor.fetchone()[0]
    
    conn.close()
    print(f" Load Complete! Total active records in SQL Warehouse: {total_rows}")
