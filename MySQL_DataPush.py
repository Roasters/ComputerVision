import pymysql
conn = pymysql.connect(host="192.168.56.107", user="root", password="1234", db="mission03", charset="utf8") # Connect to DB
cur = conn.cursor() # Create a cursor

sql = "CREATE TABLE IF NOT EXISTS missionTable(userId INT, userName CHAR(5), startYear SMALLINT)"
cur.execute(sql)
while True:
    ID = int(input("Enter the ID: "))
    if ID == 0:
        break
    name = input("Enter the name: ")
    year = int(input("Enter the year: "))
    sql = "INSERT INTO missionTable VALUES({}, '{}', {})".format(ID, name, year)
    cur.execute(sql)

cur.close()
conn.commit()
conn.close()  # Close the DB