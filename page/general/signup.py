import streamlit as st
import sqlite3
from streamlit_extras.no_default_selectbox import selectbox

custom_css = """
    <style>
    #MainMenu {visibility: hidden;}
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
        st.title {
            font-size: 40px;
            text-align: center;
            font-weight: bold;
            # margin-top: -60px;
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

st.markdown('<div class="form-container">', unsafe_allow_html=True)  # Start of custom styled container
st.markdown('</div>', unsafe_allow_html=True)  # End of custom styled container

st.title('MedImage Classifier')

st.markdown('<div class="form-container2">', unsafe_allow_html=True)  # Start of custom styled container
st.markdown('</div>', unsafe_allow_html=True)  # End of custom styled container

st.subheader('Sign Up')

con = sqlite3.connect("data.db")
cur = con.cursor()

with st.form("signup", clear_on_submit=True):
    username = st.text_input("Username")
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")
    role = selectbox("Role", ["Patient", "Physician", "Specialist"], no_selection_label="")

    col1, col2, col3 = st.columns([1,1.5,4.5])


    with col1:
        if st.form_submit_button("Sign up"):
            if username and password and role and name:
                try:
                    cur.execute("INSERT INTO users (username,password,role,name) VALUES(?,?,?,?)", (username, password, role.lower(), name))
                    con.commit()
                    st.session_state.flag = "newuser"
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Username already exists. Please choose another.")
            else:
                st.error("Please fill in all fields.")

    with col2:
        if st.form_submit_button("Back to login"):
            st.session_state.flag = None
            st.rerun()

