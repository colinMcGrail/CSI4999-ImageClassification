import streamlit as st
import base64
import sqlite3

custom_css = """
    <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
        body {
            # background-color: #462762;
            color: white;
        }
        .form-container {
            background-color: #462762;  /* Set the background color for the form container */
            padding: 20px;
            border-radius: 10px;
            width: 100%;
        }
        .form-container2 {
            background-color: #462762;  /* Set the background color for the form container */
            padding: 1px;
            border-radius: 0px;
            width: 100%;
        }
        .stApp {
            # background-color: #462762;
            # color: white;
        }
        .title {
            font-size: 40px;
            text-align: center;
            font-weight: bold;
            margin-top: -60px;
        }
        .stTextInput, .stFormSubmitButton {
            font-size: 18px;
        }
        .stButton>button {
            background-color: #462762;
            color: #ffffff;
            border-radius: 5px;
            border: 1px solid transparent;
        }
        .stButton>button:hover {
            background-color: #ffffff;
            color: #000000;
            border-radius: 5px;
            border: 1px solid #462762;
        }
</style>
"""

# Inject the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

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
