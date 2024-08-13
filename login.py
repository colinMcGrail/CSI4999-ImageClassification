import streamlit as st
import streamlit-authenticator as stauth
import dbutils
import yaml
from yaml.loader

st.title('Login')

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    role = dbutils.authenticate(username, password)
    if role:
        st.session_state.role = role
        st.rerun()
    else:
        st.error("Invalid Username Or Password")

if st.button("Sign Up"):
    st.session_state.page = 'signup'
    st.rerun()

