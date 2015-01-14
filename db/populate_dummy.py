from connection import cursor, conn

with open('init.sql') as file:
    query = file.read()

    cursor.executescript(query)
    conn.commit()

conn.close()