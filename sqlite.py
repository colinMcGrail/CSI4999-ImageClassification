import sqlite3 as sql

con = sql.connect('data.db')
cur = con.cursor()

cur.execute(
'''CREATE TABLE users
   (username    PRIMARY KEY,
    password    NOT NULL,
    role        NOT NULL);''')

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
    type        NOT NULL,
    AI_eval,
    human_eval,
    FOREIGN KEY (patient) REFERENCES user(username),
    FOREIGN KEY (AI_eval) REFERENCES evals(id),
    FOREIGN KEY (human_eval) REFERENCES evals(id));'''
)

cur.execute(
'''INSERT INTO users (username,password,role)
VALUES
    ("egDoc","physician","physician"),
    ("egSpec","specialist","specialist"),
    ("egPat","patient","patient");'''
)
