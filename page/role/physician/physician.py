import streamlit as st
import sqlite3

from library.imagetable import makeimagetable, getName
from library.stylesheet import custom_css
from library.elements import imagePage

st.markdown(custom_css, unsafe_allow_html=True)


def basepage():

    name = getName(st.session_state.user).split(' ')[-1]

    st.header("Welcome, Dr. %s." %name)

    st.subheader("Your evaluations:")

    con = sqlite3.connect("data.db")
    cur = con.cursor()

    res = cur.execute("SELECT * FROM images WHERE doctor=?", [st.session_state.user])
    results = res.fetchall()

    makeimagetable(results, ['index', 'Doctor Name'])




if st.session_state.data == "imagePage":
    st.session_state.data = None
    imagePage()
else:
    basepage()
