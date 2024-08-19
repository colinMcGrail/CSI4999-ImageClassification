import streamlit as st
import base64
import sqlite3

def getEval(id):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM evals WHERE id=?", [id])
    return res.fetchone()

def imgto64(path):
    extension = path.split('.')[-1]
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode('utf-8'), extension



st.subheader("Your evaluations:")

con = sqlite3.connect("data.db")
cur = con.cursor()

res = cur.execute("SELECT * FROM images WHERE human_eval IS NULL")
results = res.fetchall()

path = []
username = []
model = []
AIrating = []
HumRating = []

for image in results:

    pathstr = "image/" + image[2] + "/" + image[0]
    im64, filetype = imgto64(pathstr)
    encoded = "data:image/" + filetype + ";base64," + im64
    path.append(encoded)
    username.append(image[1])
    model.append(image[2])
    aieval = getEval(image[3])
    humeval = getEval(image[4])
    if aieval is not None:
        AIrating.append(aieval[2])
    else:
        AIrating.append(None)
    if humeval is not None:
        HumRating.append(humeval[2])
    else:
        HumRating.append(None)

df = {}

df["Image"] = path
df["Username"] = username
df["Condition"] = model
df["Predicted Diagnosis"] = AIrating
df["Diagnosis"] = HumRating

colcon = {
"Image": st.column_config.ImageColumn()
}

st.dataframe(data=df, column_config=colcon)
