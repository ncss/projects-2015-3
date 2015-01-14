from connection import cursor, conn

with open('schema.sql') as file:
    query = file.read()

    cursor.executescript(query)
    conn.commit()

conn.close()