import streamlit as st
import sqlite3

from library.imagetable import makeimagetable, getName
from library.stylesheet import custom_css
from library.elements import imagePage

st.markdown(custom_css, unsafe_allow_html=True)

def mainpage():

    name = getName(st.session_state.user).split(' ')[0]

    st.header("Welcome, %s!" %name)
    
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    results = cur.execute("SELECT * FROM images WHERE patient=?", [st.session_state.user])

    makeimagetable(results, ['index', 'Patient Name'])

if st.session_state.data == "imgPage":
    st.session_state.data = None
    imagepage()
else:
    mainpage()
