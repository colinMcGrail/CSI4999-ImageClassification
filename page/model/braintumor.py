import streamlit as st
import sqlite3

from library.stylesheet import custom_css
from library.elements import *

st.markdown(custom_css, unsafe_allow_html=True)

st.title("Brain Tumor Recognition")
st.text("This model is capable of recognizing meningiomas, gliomas, and pituitary tumors.")


if st.session_state.data == "spec":
    st.session_state.data = None
    specialistPageGuard()
elif st.session_state.data == "write":
    st.session_state.data = None
    submitfuncGuard("Brain Tumor")
elif st.session_state.data == "AI":
    st.session_state.data = None
    AIfuncGuard("Brain Tumor")
elif st.session_state.data == "imagePage":
    st.session_state.data = None
    imagePage()
else:
    imageUploader(st.session_state.role)
