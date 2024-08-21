import streamlit as st
from library.pagedefs import *

if "role" not in st.session_state:
    st.session_state.role = None

if "user" not in st.session_state:
    st.session_state.user = None

if "flag" not in st.session_state:
    st.session_state.flag = None

if "data" not in st.session_state:
    st.session_state.data = None

page_dict = {}

if st.session_state.flag == 'signup':
    pg = st.navigation([signup_page])
elif st.session_state.flag == 'imgpage':
    pg = st.navigation([imgpage])
elif st.session_state.role is None:
    pg = st.navigation([login_page])
else:
    if st.sidebar.button("Log out"):
        logout()

    match st.session_state.role:
        case 'patient':
            page_dict["Patient"] = patientPages
        case 'physician':
            page_dict["Physician"] = physicianPages
            page_dict["Models"] = modelPages
        case 'specialist':
            page_dict["Specialist"] = specialistPages
            page_dict["Models"] = modelPages

    page_dict["Account and Settings"] = generalPages
    pg = st.navigation(page_dict)  

pg.run()
