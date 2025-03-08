from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sqlite3
import json

app = FastAPI()

# Sample PC builds (25+ builds stored in SQLite)
PC_BUILDS = [
    {"id": 1, "name": "Budget Gaming Build", "cpu": "AMD Ryzen 5 5600X", "gpu": "NVIDIA GTX 1660 Super", "ram": "16GB DDR4", "storage": "512GB NVMe SSD", "psu": "550W Bronze", "price": 800},
    {"id": 2, "name": "High-End Gaming Build", "cpu": "Intel Core i9-12900K", "gpu": "NVIDIA RTX 4090", "ram": "32GB DDR5", "storage": "2TB NVMe SSD", "psu": "850W Gold", "price": 3500},
    # Add 23 more builds...
]

# Initialize database
def init_db():
    conn = sqlite3.connect("pc_builds.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS builds (
            id INTEGER PRIMARY KEY,
            name TEXT,
            cpu TEXT,
            gpu TEXT,
            ram TEXT,
            storage TEXT,
            psu TEXT,
            price INTEGER
        )
    """)
    conn.commit()
    
    # Insert sample builds if not exists
    cursor.execute("SELECT COUNT(*) FROM builds")
    if cursor.fetchone()[0] == 0:
        for build in PC_BUILDS:
            cursor.execute("""
                INSERT INTO builds (id, name, cpu, gpu, ram, storage, psu, price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (build["id"], build["name"], build["cpu"], build["gpu"], build["ram"], build["storage"], build["psu"], build["price"]))
        conn.commit()
    conn.close()

init_db()

# API to fetch builds
@app.get("/builds", response_model=List[dict])
def get_builds():
    conn = sqlite3.connect("pc_builds.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM builds")
    builds = [{"id": row[0], "name": row[1], "cpu": row[2], "gpu": row[3], "ram": row[4], "storage": row[5], "psu": row[6], "price": row[7]} for row in cursor.fetchall()]
    conn.close()
    return builds
