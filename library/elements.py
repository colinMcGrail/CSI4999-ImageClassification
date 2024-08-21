import streamlit as st
from uuid import uuid4
import sqlite3
from PIL import Image
from streamlit_extras.image_selector import image_selector
from library.evalutils import *
from streamlit_extras.no_default_selectbox import selectbox

@st.dialog("Crop image")
def imageCropper(image):
    st.write("For best results, please crop out any irrelevant parts of the image, trying to keep the result as square as possible.")
    width, height = image.size
    select = image_selector(image=image, width=width, height=height)

    if st.button("Submit", key="speceval"):
        st.session

@st.fragment  
def specialistPage(image, ptname):
    
    diagnosis = None
    comments = None
    bool = False
    st.success(str(image))
    
    container = st.container(border=True)
    container.success(str(image))

    diagnosis = None
    comments = None
    
    diagnosis = container.text_input("Diagnosis:")
    comments = container.text_area("Comments:")

    if container.button("Submit", key="specpage1") and diagnosis:
        st.session_state.image = image
        print(str(st.session_state.image))
        print(str(image))
        st.session_state.ptname = ptname
        st.session_state.diagnosis = diagnosis
        st.session_state.comments = comments
        st.session_state.data = "write"
        st.rerun()
    if container.button("Use model instead", key="specpage2"):
        st.session_state.data = "AI"
        st.session_state.image = image
        st.session_state.ptname = ptname
        st.rerun()


def specialistPageGuard():
    image = st.session_state.image
    ptname = st.session_state.ptname
    st.session_state.image = None
    st.session_state.ptname = None
    
    specialistPage(image, ptname)

@st.fragment()
def imageUploader(role):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    res = cur.execute("SELECT name FROM users WHERE role = 'patient';")
    names = []
    for name in res.fetchall():
        names.append(name[0])

    with  st.container(border=True):
        file = st.file_uploader("Select image")

        if file: 
            image = Image.open(file).convert('RGB')       
            st.image(image)     
        ptname = selectbox("Enter name of patient:", names, no_selection_label="")
        if st.button("Submit", key="imageuploader"):
            res = cur.execute("SELECT username FROM users WHERE name = ?;", [ptname])
            ptuser = res.fetchone()[0]
            if role == "specialist":
                st.session_state.data = "spec"
                st.session_state.image = image
                st.session_state.ptname = ptname
                st.rerun()
            elif role == "physician":
                st.session_state.data = "AI"
                st.session_state.image = image
                st.session_state.ptname = ptname
                st.rerun()


def AIfuncGuard(modelname):

    image = st.session_state.image
    ptname = st.session_state.ptname

    st.session_state.data = None
    st.session_state.image = None
    st.session_state.ptname = None

    AIfunc(modelname, image, ptname)

@st.fragment()
def AIfunc(modelname, image, ptname):

    con = sqlite3.connect("data.db")
    cur = con.cursor()
    
    res = cur.execute("SELECT username FROM users where name =?", [ptname])
    username = res.fetchone()[0]

    name = evaluateImage(image, modelname, username)

    st.session_state.data = "imagePage"
    st.session_state.filename = name
    st.rerun()

def submitfuncGuard(modelname):
    image = st.session_state.image
    name = st.session_state.ptname
    diagnosis = st.session_state.diagnosis
    comments = st.session_state.comments

    st.session_state.image = None
    st.session_state.ptname = None
    st.session_state.diagnosis = None
    st.session_state.comments = None
    st.session_state.data = None

    submitfunc(modelname, image, name, diagnosis, comments)

@st.fragment()
def submitfunc(modelname, image, name, diagnosis, comments):


    filename = saveimg(image, modelname)

    con = sqlite3.connect("data.db")
    cur = con.cursor()
    
    res = cur.execute("SELECT username FROM users where name =?", [name])
    username = res.fetchone()[0]


    evalid = str(uuid4())
    cur.execute("INSERT INTO evals(id, issuer, rating, comments) VALUES (?,?,?,?)", [evalid, st.session_state.user, diagnosis, comments])
    cur.execute("INSERT INTO images(filename, patient, doctor, type, AI_eval, human_eval) VALUES (?,?,?,?,?,?)", [filename, username, st.session_state.user, modelname, None, evalid])
    con.commit()
    st.success("Evaluation submitted?")

def imagePage():

    filename = st.session_state.filename
    st.session_state.filename = None

    con = sqlite3.connect("data.db")
    cur = con.cursor()

    res = cur.execute("SELECT * FROM images WHERE filename=?", [filename])
    results = res.fetchone()

    path = "image/" + filename

    st.image(path)

    if results[4] is not None:
        aicon = st.container(border=True)
        aieval = cur.execute("SELECT * FROM evals WHERE id=?", [results[4]]).fetchone()

        aicon.subheader("Model evaluation: %s" %aieval[2])

    if results[5] is not None:
        doccon = st.container(border=True)
        doceval = cur.execute("SELECT * FROM evals WHERE id=?", [results[5]]).fetchone()
        
        doccon.subheader("Professional diagnosis: %s" %doceval[2])
        
        if doceval[3] is not None:
            doccon.text(doceval[3])

    elif st.session_state.role == "specialist":
        specialistReview(results[0])

@st.fragment
def specialistReview(imagekey):
    
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    container = st.container(border=True)
    comments = None
    
    diagnosis = container.text_input("Diagnosis:")
    comments = container.text_area("Comments:")

    if container.button("Submit"):
        if diagnosis is not None:
            evalid = str(uuid4())
            cur.execute("INSERT INTO evals(id, issuer, rating, comments) VALUES (?,?,?,?)", [evalid, st.session_state.user, diagnosis, comments])
            cur.execute("UPDATE images SET human_eval=? WHERE filename=?", [evalid, imagekey])
            con.commit()
            st.session_state.data = "imagePage"
            st.session_state.filename = imagekey
            st.success("WHAT")
            st.rerun()
        else:
            st.success("what")

    


    

    


