import sqlite3
conn = sqlite3.connect("samsongDB") # Connect to DB
cur = conn.cursor() # Create a cursor

sql = "CREATE TABLE IF NOT EXISTS userTable(id INT, userName CHAR(5))"
cur.execute(sql)
sql = "INSERT INTO userTable VALUES(1, 'Hong')"
cur.execute(sql)
sql = "INSERT INTO userTable VALUES(1, 'Lee')"
cur.execute(sql)

cur.close()
conn.commit()
conn.close()  # Close the DB