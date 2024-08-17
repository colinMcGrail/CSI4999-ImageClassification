import streamlit as st
from keras.models import load_model
from PIL import Image
import numpy as np
import sqlite3
import os
from uuid import uuid4

def classifyOsteoarthritis(file, model):
    name = saveimg(file)
    image = Image.open(file).convert('RGB')
    img = image.resize((224, 224))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return model.predict(img_array)[0][0], name

def saveimg(file):
    extension = file.name.split('.')[-1]
    while True:        
        id = str(uuid4())
        name = id + '.' + extension
        path = os.path.join('image/osteoarthritis/', name)
        if not os.path.isfile(path):
            break
    with open(path, "wb") as f:
        f.write(file.getbuffer())
    return name

def evaluateImage


con = sqlite3.connect("data.db")
cur = con.cursor()

model = load_model('models/osteoarthritis.keras')


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
            pred, name = evalu(file, model)
            cur.execute("INSERT INTO ")
        else:
            st.error("No such patient found.")







