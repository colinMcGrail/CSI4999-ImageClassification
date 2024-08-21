import sqlite3 as sql

con = sql.connect('../data.db')
cur = con.cursor()

cur.execute(
'''CREATE TABLE users
   (username    PRIMARY KEY,
    password,
    role        NOT NULL,
    name);''')

cur.execute(
'''CREATE TABLE evals
   (id      PRIMARY KEY,
    issuer  NOT NULL,
    rating,
    comments,
    FOREIGN KEY (issuer) REFERENCES users(username));''')

cur.execute(
'''CREATE TABLE images
   (filename    PRIMARY KEY,
    patient     NOT NULL,
    doctor      NOT NULL,
    type        NOT NULL,
    AI_eval,
    human_eval,
    FOREIGN KEY (patient) REFERENCES user(username),
    FOREIGN KEY (doctor) REFERENCES user(username),
    FOREIGN KEY (AI_eval) REFERENCES evals(id),
    FOREIGN KEY (human_eval) REFERENCES evals(id));'''
)

users = [
    ('osteoarthritis', None, 'AI', None),
    ('doc', 'doc', 'physician', 'Placeholder McDoctorate'),
    ('pat', 'pat', 'patient', 'Glassbones Paperskin'),
    ('dude', 'dude', 'specialist', 'THE MAN')
]

cur.executemany("INSERT INTO users(username, password, role, name) VALUES (?,?,?,?)", users)
con.commit()

