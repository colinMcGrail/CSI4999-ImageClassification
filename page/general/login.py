import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from library.pagedefs import login_page
import sqlite3

st.title('Login')

con = sqlite3.connect("data.db")
cur = con.cursor()

if st.session_state.flag == "newuser":
    st.success("Account created successfully! You can now log in.")

form = st.form("login")
username = form.text_input("Username")
password = form.text_input("Password", type="password")

if form.form_submit_button("Log in"):
    res = cur.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    userRole = res.fetchone()
    if userRole:
        st.session_state.user = username
        st.session_state.role = userRole[0]
        st.session_state.flag = None
        st.rerun()
    else:
        st.error("Invalid Username Or Password")
if form.form_submit_button("Sign up"):
    st.session_state.flag = "signup"
    st.rerun()
