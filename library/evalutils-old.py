from keras.models import load_model
import streamlit as st
from PIL import Image
import numpy as np
import os
import sqlite3
from uuid import uuid4


def classifyOsteoarthritis(file):
    model = load_model('models/osteoarthritis.keras')
    image = Image.open(file).convert('RGB')
    img = image.resize((224, 224))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)[0][0]
    return str(prediction)

def saveimg(file, dirname):
    extension = file.name.split('.')[-1]
    while True:        
        id = str(uuid4())
        name = id + '.' + extension
        directory = 'image/' + dirname + '/'
        path = os.path.join(directory, name)
        if not os.path.isfile(path):
            break
    with open(path, "wb") as f:
        f.write(file.getbuffer())
    return name

def evaluateImage(image, modelname, patientname):

    con = sqlite3.connect("data.db")
    cur = con.cursor()

    name = saveimg(image, modelname)

    match modelname:
        case 'Osteoarthritis':
                pred = classifyOsteoarthritis(image)
                print(pred)
        case _:
                return 137

    evalid = str(uuid4())
        
    cur.execute("INSERT INTO evals(id, issuer, rating, comments) VALUES (?,?,?,?)", [evalid, modelname, pred, None])

    cur.execute("INSERT INTO images(filename, patient, doctor, type, AI_eval, human_eval) VALUES (?,?,?,?,?,?)", [name, patientname, st.session_state.user, modelname, evalid, None])

    con.commit()

    return pred        

def imgtoArray(file):

    image = Image.open(file).convert('RGB')
    img = image.resize((224, 224))
    img_array = np.array(img)
    return img_array

def getnameofuser(username):
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    res = cur.execute("SELECT name FROM users WHERE username = ?", [username])
    name = res.fetchone()[0]

#def verifyUser(username, password = None, role = None):
#   con = sqlite3.connect("data.db")
#    cur = con.cursor()
#
#    cur.execute(select)

