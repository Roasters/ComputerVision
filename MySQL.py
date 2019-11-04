import pymysql
conn = pymysql.connect(host="192.168.56.107", user="root", password="1234", db="mission03", charset="utf8") # Connect to DB
cur = conn.cursor() # Create a cursor

sql = "SELECT * FROM missionTable"
cur.execute(sql)

print(" 사번   이름  입사연도")
print("-" * 22)
while True:
    row = cur.fetchone()
    if row:
        print("{:4d} {:>5s} {:5d}".format(row[0], row[1], row[2]))
    else: break

print("-" * 22)

cur.close()
conn.close()