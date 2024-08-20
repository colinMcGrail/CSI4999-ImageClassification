import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from pagedefs import login_page
import sqlite3

# Custom CSS to hide the Streamlit "Deploy" button and "Menu" button
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

st.title('MedImage Classifier')
st.subheader('Login')

con = sqlite3.connect("data.db")
cur = con.cursor()

if st.session_state.flag == "newuser":
    st.success("Account created successfully! You can now log in.")

# Create a form with a background color
with st.form("login", clear_on_submit=True):

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Create two columns for the buttons
    col1, col2, col3, col4,col5, col6, col7 = st.columns(7)
    col, col0=st.columns(2)

    # Place the buttons in the columns
    with col1:
        if st.form_submit_button("Log in"):
            res = cur.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
            userRole = res.fetchone()
            if userRole:
                st.session_state.user = username
                st.session_state.role = userRole[0]
                st.session_state.flag = None
                st.rerun()
            else:
                with col:
                    st.error("Invalid Username Or Password")

    with col2:
        if st.form_submit_button("Sign up"):
            st.session_state.flag = "signup"
            st.rerun() 