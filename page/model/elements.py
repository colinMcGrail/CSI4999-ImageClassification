import streamlit as st
from PIL import Image
from streamlit_extras.image_selector import image_selector

@st.dialog("Crop image")
def imageCropper(image):
    st.write("For best results, please crop out any irrelevant parts of the image, trying to keep the result as square as possible.")
    width, height = image.size
    select = image_selector(image=image, width=width, height=height)

    if st.button("Submit"):
        st.success(str(select))
    



def imageUploader(role):
    with st.form("Upload image here"):
        file = st.file_uploader("Select image")
        if file: 
            image = Image.open(file).convert('RGB')
            image = imageCropper(image)
            st.success(str(image))
        st.form_submit_button("Submit")

