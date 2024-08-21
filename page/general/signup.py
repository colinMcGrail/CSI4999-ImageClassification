import streamlit as st
import sqlite3

st.title('Sign Up')

con = sqlite3.connect("data.db")
cur = con.cursor()

form = st.form("signup")
username = form.text_input("Username")
name = form.text_input("Name")
password = form.text_input("Password", type="password")
role = form.selectbox("Role", [None, "Patient", "Physician", "Specialist"])



if form.form_submit_button("Sign up"):
    if username and password and role and name:
        try:
            cur.execute("INSERT INTO users (username,password,role,name) VALUES(?,?,?,?)", (username, password, role.lower(), name))
            con.commit()
            st.session_state.flag = "newuser"
            st.rerun()
        except sqlite3.IntegrityError:
            st.error("Username already exists. Please choose another.")
    else:
        st.error("Please fill in all fields.")
if form.form_submit_button("Back to login"):
    st.session_state.flag = None
    st.rerun()

