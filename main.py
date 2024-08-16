import streamlit as st
from pagedefs import *
from gendefs import *

if "role" not in st.session_state:
    st.session_state.role = None

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = None

if "authentication_status" not in st.session_state:
    st.session_state.authentication_status = None

page_dict = {}

if st.session_state.page == 'signup':
    pg = st.navigation([signup_page])
elif st.session_state['authentication_status'] is None or False:
        pg = st.navigation([login_page])
else:
    page_dict["Account and Settings"] = generalPages
    if st.session_state.role in ["Doctor", "Specialist"]:
        page_dict["Models"] = modelPages
    if st.session_state.role == "Patient":
        page_dict["Need better name"] = patientPages
    if st.session_state.role == "Doctor":
        page_dict["Need better name"] = doctorPages
    if st.session_state.role == "Specialist":
        page_dict["Need better name"] = specialistPages
    pg = st.navigation(page_dict)  

pg.run()
