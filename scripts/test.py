import sqlite3 as sql

con = sql.connect('../data.db')
cur = con.cursor()

test = cur.execute("SELECT role FROM users WHERE username=?", ['osteoarthritis'])

print(str(test.fetchone()[0])) 
