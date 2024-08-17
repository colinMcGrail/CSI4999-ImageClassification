import sqlite3 as sql

con = sql.connect('../data.db')
cur = con.cursor()

cur.execute("INSERT INTO users(username, password, role) VALUES (?,?,?)", ['osteoarthritis', None, 'AI'])
con.commit()
