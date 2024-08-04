import streamlit as st
from keras.models import load_model
from PIL import Image
import numpy as np

# Dummy user data
users = {
    "user1": {"password": "password1", "role": "User"},
    "user2": {"password": "password2", "role": "Physician"},
    "user3": {"password": "password3", "role": "Specialist"},
}

def authenticate(username, password):
    if username in users and users[username]["password"] == password:
        return users[username]["role"]
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

# Set page config
st.set_page_config(page_title="MedImage Classifier", page_icon=":hospital:", layout="wide")


# # CSS for enhanced styling
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

# Display app name before login
if not st.session_state.role:
    st.title('MedImage Classifier')
    st.subheader('AI-Powered Osteoarthritis Diagnosis')
    st.image("./doctor.png", caption="")

if st.session_state.role:
    st.sidebar.title(f"Welcome, {st.session_state.role}")


    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.role = None
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

    elif role == "Specialist":
        st.title("Specialist Dashboard")
        st.write("Welcome to the Specialist Dashboard. You can verify diagnoses and compare with the model's output.")
        annotation = st.text_area("Annotation", "Enter your notes here...")
        if st.button("Analyze Image"):
            # Simulating an API call
            response = {"predictions": "Simulated Prediction"}
            predictions = response["predictions"]
            st.write("Predictions:", predictions)
            diagnosis = st.selectbox("Verify Diagnosis", ["Correct", "Incorrect"])
            st.write(f"Diagnosis Verified as: {diagnosis}")

else:
    st.sidebar.title('Login')

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        role = authenticate(username, password)
        if role:
            st.session_state.role = role
            st.sidebar.success(f"Logged in as {username} with role {role}")
            st.experimental_rerun()
        else:
            st.sidebar.error("Invalid Username Or Password")
    else:
        st.sidebar.warning("Enter Valid Username and Password")
