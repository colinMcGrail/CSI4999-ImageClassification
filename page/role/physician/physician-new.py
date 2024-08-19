import streamlit as st
import base64
import pandas as pd
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
query = "SELECT * FROM images WHERE human_eval IS NULL"

df = pd.read_sql_query(query,con)

st.success(df.columns)

colcon = {
#"Image": st.column_config.ImageColumn()
}

st.dataframe(data=df)
