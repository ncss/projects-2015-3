import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(__file__), 'database.db')
print(DB_FILE)

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

