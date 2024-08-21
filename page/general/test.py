import sqlite3
import streamlit as st

con = sqlite3.connect("data.db")
cur = con.cursor()

if st.button("images"):
    st.success(str(cur.execute("SELECT * FROM images").fetchall()))

if st.button("users"):
    st.success(str(cur.execute("SELECT * FROM users").fetchall()))

if st.button("evals"):
    st.success(str(cur.execute("SELECT * FROM evals").fetchall()))
