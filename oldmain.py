import streamlit as st
import sqlite3
from keras.models import load_model
from PIL import Image
import numpy as np

# Database setu

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


else:  # Main application view
    if not st.session_state.role:
        st.session_state.page = 'login'
        st.rerun()

    st.sidebar.title(f"Welcome, {st.session_state.role}")

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.role = None
        st.session_state.page = 'login'
        st.rerun()

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
