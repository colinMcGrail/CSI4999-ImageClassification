import sqlite3

def init_connection():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    return conn, c

def create_users_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, role TEXT, password TEXT)''')
    conn.commit()
    conn.close()

def add_user_to_db(username, role, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, role, password) VALUES (?, ?, ?)", (username, role, password))
    conn.commit()
    conn.close()

def authenticate(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return user[0]
    else:
        return None
