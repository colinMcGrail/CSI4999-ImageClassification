import streamlit as st
import sqlite3
from evalutils import evaluateImage

con = sqlite3.connect("data.db")
cur = con.cursor()

pred = 0

st.title('Osteoarthritis Classification')
st.header('Upload your image here')

form = st.form("Image")
file = form.file_uploader('', type=['jpeg', 'jpg', 'png'])
patientName = form.text_input("Username of patient:")

if form.form_submit_button("Evaluate"):
    if file == None:
        st.error("Please upload a file")
    elif patientName == None:
        st.error("Please specify a patient")
    else:
        res = cur.execute("SELECT * FROM users WHERE username=? AND role='patient';", [patientName])
        if res.fetchone(): 
            pred = evaluateImage(file, 'osteoarthritis', patientName)
        else:
            st.error("No such patient found.")

with st.container(border=True):

        st.subheader("Severity rating: " + str(pred))





