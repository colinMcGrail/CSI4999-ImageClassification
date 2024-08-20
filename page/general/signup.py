import streamlit as st
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

st.title('MedImage Classifier')

st.subheader('Sign Up')

con = sqlite3.connect("data.db")
cur = con.cursor()

form = st.form("signup")
username = form.text_input("Username")
role = form.selectbox("Role", [None, "Patient", "Physician", "Specialist"])
password = form.text_input("Password", type="password")


if form.form_submit_button("Sign up"):
    if username and password and role:
        try:
            cur.execute("INSERT INTO users (username,password,role) VALUES(?,?,?)", (username, password, role.lower()))
            con.commit()
            st.session_state.flag = "newuser"
            st.rerun()
        except sqlite3.IntegrityError:
            st.error("Username already exists. Please choose another.")
    else:
        st.error("Please fill in all fields.")
if form.form_submit_button("Back to login"):
    st.session_state.flag = None
    st.rerun()

