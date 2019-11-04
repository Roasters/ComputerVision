import sqlite3
conn = sqlite3.connect("samsongDB") # Connect to DB
cur = conn.cursor() # Create a cursor

sql = "SELECT * FROM userTable"
cur.execute(sql)
rows = cur.fetchall()

print(rows)

cur.close()
conn.close()  # Close the DB