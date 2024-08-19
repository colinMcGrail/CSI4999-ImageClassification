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

def imgto64(path):
    extension = path.split('.')[-1]
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode('utf-8'), extension




st.subheader("Your evaluations:")

con = sqlite3.connect("data.db")
cur = con.cursor()

res = cur.execute("SELECT * FROM images WHERE human_eval IS NULL")
results = res.fetchall()

index = []
path = []
username = []
model = []
AIrating = []
HumRating = []

for image in results:
    pathstr = "image/" + image[2] + "/" + image[0]
    index.append(pathstr)
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

dfdict = {}

dfdict["index"] = index
dfdict["Image"] = path
dfdict["Username"] = username
dfdict["Condition"] = model
dfdict["Predicted Diagnosis"] = AIrating
dfdict["Diagnosis"] = HumRating

df = pd.DataFrame(data=dfdict)

options_builder = GridOptionsBuilder.from_dataframe(df)

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

options_builder.configure_column('Image', cellRenderer=thumbnail_renderer)
options_builder.configure_column('index', hide=True)


grid_options = options_builder.build()

grid_return = AgGrid(df,
                    grid_options,
                    theme="streamlit",
                    update_on=["rowClicked"],
                    allow_unsafe_jscode=True,
                    ) 

if grid_return.event_data is not None:
    st.session_state.flag = "imgpage"
    st.session_state.data = (str(grid_return.event_data['data']['index']))
    st.rerun()
