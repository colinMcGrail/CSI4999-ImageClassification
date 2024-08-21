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


custom_css = """
    <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
        body {
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

if st.session_state.flag == 'signup':
    pg = st.navigation([signup_page])
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
