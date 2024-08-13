import streamlit as st
import sqlite3
from keras.models import load_model
from PIL import Image
import numpy as np

# Database setup
def create_users_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, role TEXT, password TEXT)''')
    conn.commit()
    conn.close()

def add_user_to_db(username, role, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, role, password) VALUES (?, ?, ?)", (username, role, password))
    conn.commit()
    conn.close()

def authenticate(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return user[0]
    else:
        return None

# Function to classify image
def classify(image, model, class_names):
    img = image.resize((224, 224))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    predictions = model.predict(img_array)
    class_index = np.argmax(predictions)
    class_name = class_names[class_index]
    confidence_score = predictions[0][class_index]
    return class_name, confidence_score

# Initialize session state
if 'role' not in st.session_state:
    st.session_state.role = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Clear fields when changing page
def reset_fields():
    st.session_state.username = ""
    st.session_state.password = ""
    st.session_state.role_selection = "User"

# Set page config
st.set_page_config(page_title="MedImage Classifier", page_icon=":hospital:", layout="wide")

# CSS for enhanced styling
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #0e76a8;
            color: white;
        }
        .stButton>button {
            background-color: #0e76a8;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Ensure the database is set up
create_users_table()

# Login and Sign Up Page
if st.session_state.page == 'login':
    st.sidebar.title('Login')

    # Reset fields if navigating from another page
    reset_fields()

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        role = authenticate(username, password)
        if role:
            st.session_state.role = role
            st.session_state.page = 'main'
            st.experimental_rerun()
        else:
            st.sidebar.error("Invalid Username Or Password")

    if st.sidebar.button("Sign Up"):
        st.session_state.page = 'signup'
        st.experimental_rerun()

elif st.session_state.page == 'signup':
    st.sidebar.title('Sign Up')

    # Reset fields if navigating from another page
    reset_fields()

    username = st.text_input("Username")
    role = st.selectbox("Role", ["User", "Physician", "Professional Doctor"])
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if username and password:
            try:
                add_user_to_db(username, role, password)
                st.success("Account created successfully! You can now [log in](#).")
                st.session_state.page = 'login'
                st.experimental_rerun()
            except sqlite3.IntegrityError:
                st.error("Username already exists. Please choose another.")
        else:
            st.error("Please fill in all fields.")

else:  # Main application view
    if not st.session_state.role:
        st.session_state.page = 'login'
        st.experimental_rerun()

    st.sidebar.title(f"Welcome, {st.session_state.role}")

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.role = None
        st.session_state.page = 'login'
        st.experimental_rerun()

    st.title('Osteoarthritis Classification')
    st.header('Upload your file here')

    file = st.file_uploader('', type=['jpeg', 'jpg', 'png'])
    model = load_model('./model/osteoarthritis.h5')
    with open('./model/labels.txt') as f:
        class_names = [a[:-1].split(' ')[1] for a in f.readlines()]
        f.close()

    if file is not None:
        image = Image.open(file).convert('RGB')
        st.image(image, use_column_width=True)

        class_name, conf_score = classify(image, model, class_names)

        st.write("## {}".format(class_name))
        st.write("### score: {}%".format(int(conf_score * 1000) / 10))

    role = st.session_state.role
    if role == "User":
        st.title("Normal User Dashboard")
        st.write("Welcome to the Normal User Dashboard. You can upload and view your medical images here.")

    elif role == "Physician":
        st.title("Physician Dashboard")
        st.write("Welcome to the Physician Dashboard. You can upload, annotate, and analyze medical images here.")
        annotation = st.text_area("Annotation", "Enter your notes here...")
        if st.button("Analyze Image"):
            # Simulating an API call
            response = {"predictions": "Simulated Prediction"}
            predictions = response["predictions"]
            st.write("Predictions:", predictions)

    elif role == "Professional Doctor":
        st.title("Professional Doctor Dashboard")
        st.write("Welcome to the Professional Doctor Dashboard. You can verify diagnoses and compare with the model's output.")
        annotation = st.text_area("Annotation", "Enter your notes here...")
        if st.button("Analyze Image"):
            # Simulating an API call
            response = {"predictions": "Simulated Prediction"}
            predictions = response["predictions"]
            st.write("Predictions:", predictions)
            diagnosis = st.selectbox("Verify Diagnosis", ["Correct", "Incorrect"])
            st.write(f"Diagnosis Verified as: {diagnosis}")