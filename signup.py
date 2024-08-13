import streamlit as st
import sqlite3
import dbutils
from gendefs import *

st.title('Sign Up')

username = st.text_input("Username")
role = st.selectbox("Role", ROLES)
password = st.text_input("Password", type="password")

if st.button("Sign Up"):
    if username and password:
        try:
            dbutils.add_user_to_db(username, role, password)
            st.success("Account created successfully! You can now [log in](#).")
            st.session_state.role = role
            st.rerun()
        except sqlite3.IntegrityError:
            st.error("Username already exists. Please choose another.")
    else:
        st.error("Please fill in all fields.")

