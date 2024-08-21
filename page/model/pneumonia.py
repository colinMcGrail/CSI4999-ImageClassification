from library.elements import *
import streamlit as st
import sqlite3

st.title("Pneumonia model")
st.text("This model is capable of recognizing viral and bacterial pneumonia")


if st.session_state.data == "spec":
    st.session_state.data = None
    specialistPageGuard()
elif st.session_state.data == "write":
    st.session_state.data = None
    submitfuncGuard("Pneumonia")
elif st.session_state.data == "AI":
    st.session_state.data = None
    AIfuncGuard("Pneumonia")
else:
    imageUploader(st.session_state.role)
