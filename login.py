import streamlit as st
import streamlit_authenticator as stauth
import yaml
import sqlite3
from gendefs import *
from yaml.loader import SafeLoader

st.title('Login')

with open('users.yaml') as file:
    users = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    users['credentials'],
    users['cookie']['name'],
    users['cookie']['key'],
    users['cookie']['expiry_days']
)

con, cur = makeconnection()

name, authentication_status, username = authenticator.login('main')

if authentication_status:
    st.session_state.role = cur.execute('SELECT role FROM Users WHERE username=?', [st.session_state['username']])
    st.rerun()
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

