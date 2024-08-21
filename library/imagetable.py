import streamlit as st
import base64
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, DataReturnMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import sqlite3

def getEval(id):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM evals WHERE id=?", [id])
    return res.fetchone()

def getName(username):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    res = cur.execute("SELECT name FROM users WHERE username=?", [username])
    return res.fetchone()[0]

def imgto64(image):
    pathstr = "image/" + image
    with open(pathstr, "rb") as img:
        data = "data:image/png;base64," + base64.b64encode(img.read()).decode('utf-8')
        return data



def makeimagetable(results, exclude=['index'], key=None):

    thumbnail_renderer = JsCode("""
    class ThumbnailRenderer {
    init(params) {
    this.eGui = document.createElement('img');
    this.eGui.setAttribute('src', params.data.Image);
    this.eGui.setAttribute('width', 'auto');
    this.eGui.setAttribute('height', '30');
    }
    getGui() {
    return this.eGui;
    }
    }
    """)


    dict = {
        "index": [],
        "Image": [],
        "Patient Name": [],
        "Doctor Name": [],
        "Condition": [],
        "Predicted Diagnosis": [],
        "Diagnosis": []
    }

    for image in results:
        dict["index"].append(image[0])
        dict["Image"].append(imgto64(image[0]))
        dict["Patient Name"].append(getName(image[1]))
        dict["Doctor Name"].append("Dr. " + getName(image[2]).split(' ')[-1])
        dict["Condition"].append(image[3])

        aieval = getEval(image[4])
        if aieval is not None:
            dict["Predicted Diagnosis"].append(aieval[2])
        else:
            dict["Predicted Diagnosis"].append(None)
    

        humeval = getEval(image[5])
        if humeval is not None:
            dict["Diagnosis"].append(humeval[2])
        else:
            dict["Diagnosis"].append(None)

    df = pd.DataFrame(data=dict)

    options_builder = GridOptionsBuilder.from_dataframe(df)
    options_builder.configure_column('Image', cellRenderer=thumbnail_renderer)

    for column in exclude:
        options_builder.configure_column(column, hide=True)

    grid_options = options_builder.build()

    grid_return = AgGrid(df,
                        grid_options,
                        theme="streamlit",
                        update_on=["rowClicked"],
                        allow_unsafe_jscode=True,
                        key = key
                        ) 

    if grid_return.event_data is not None:
        try:
            st.session_state.filename = (str(grid_return.event_data['data']['index']))
            st.session_state.data = "imagePage"
            st.rerun()
        except KeyError:
            st.session_state.filename = None
        

