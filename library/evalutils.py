from keras.models import load_model
import keras
import streamlit as st
from PIL import Image
import numpy as np
import os
import time
import sqlite3
from uuid import uuid4



def classifyOsteoarthritis(image):
    model = load_model('models/osteoarthritis.keras')
    img = image.resize((224, 224))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    pred = model.predict(img_array)[0]              
    if max(pred) == pred[0]:
        return 0
    elif max(pred) == pred[1]:
        return 1
    elif max(pred) == pred[2]:
        return 2
    elif max(pred) == pred[3]:
        return 3
    elif max(pred) == pred[4]:
        return 4

def classifyPneumonia(image):
    model = load_model('models/pneumonia_convnext.keras')
    img = image.resize((224, 224))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    prarr = model.predict(img_array)[0]
    viral, normal, bacterial = prarr[0], prarr[1], prarr[2]
    if normal > bacterial and normal > viral:
        return "Healthy"
    elif bacterial > viral:
        return "Bacterial Pneumonia"
    else:
        return "Viral Pneumonia"

def classifyBrainTumor(image):
    model = load_model('models/braintumor.keras')
    img =image.resize((256,256))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    p = model.predict(img_array)[0]
    if float(p[0]) > float(p[1]) and float(p[0]) > float(p[2]) and float(p[0]) > float(p[3]):
        return "Glioma"
    elif float(p[1]) > float(p[2]) and float(p[1]) > float(p[3]):
        return "Meningioma"
    elif  float(p[2]) > float(p[3]):
        return "Healthy"
    else:
        return "Pituitary Tumor"

def saveimg(image, dirname):

    while True:        
        id = str(uuid4())
        name = id + '.png'
        path = 'image/' + name
        if not os.path.isfile(path):
            break

    image.save(path, format="PNG")
    return name


def evaluateImage(image, modelname, patientname):

    con = sqlite3.connect("data.db")
    cur = con.cursor()

    name = saveimg(image, modelname)

    match modelname:
        case 'Osteoarthritis':
                pred = classifyOsteoarthritis(image)
        case 'Pneumonia':
                pred = classifyPneumonia(image)
        case 'Brain Tumor':
                pred = classifyBrainTumor(image)
        case _:
                return 137

    evalid = str(uuid4())
        
    cur.execute("INSERT INTO evals(id, issuer, rating, comments) VALUES (?,?,?,?)", [evalid, modelname, pred, None])

    cur.execute("INSERT INTO images(filename, patient, doctor, type, AI_eval, human_eval) VALUES (?,?,?,?,?,?)", [name, patientname, st.session_state.user, modelname, evalid, None])

    con.commit()

    return name        

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

