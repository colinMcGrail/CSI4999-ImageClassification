import streamlit as st
import sqlite3

from library.imagetable import makeimagetable, getName
from library.stylesheet import custom_css
from library.elements import imagePage

st.markdown(custom_css, unsafe_allow_html=True)


def mainpage():

    name = getName(st.session_state.user).split(' ')[-1]

    st.header("Welcome, Dr. %s." %name)

    st.subheader("Your evaluations:")

    con = sqlite3.connect("data.db")
    cur = con.cursor()
    res = cur.execute("SELECT id FROM evals WHERE issuer=?", [st.session_state.user]) #Gets list of evaluations by user
    results = res.fetchall()

    images = []

    for eval in results:
        image = cur.execute("SELECT * FROM images WHERE human_eval=?", [eval[0]]) # gets list
        images.append(image.fetchone())

    makeimagetable(images, ['index'], 1)

    st.subheader("Unevaluated images:")


    res = cur.execute("SELECT * FROM images WHERE human_eval IS NULL")
    results = res.fetchall()

    makeimagetable(results, ['index', 'Diagnosis'], 2)


if st.session_state.data == "imagePage":
    st.session_state.data = None
    imagePage()
else:
    mainpage()

