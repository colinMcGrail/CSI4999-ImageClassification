import streamlit as st
import sqlite3

from library.stylesheet import custom_css
from library.elements import *

st.markdown(custom_css, unsafe_allow_html=True)

st.title("Osteoarthritis")
st.text("Returned values are a decimal approximation of the Kellgren-Lawrence scale")


if st.session_state.data == "spec":
    st.session_state.data = None
    specialistPageGuard()
elif st.session_state.data == "write":
    st.session_state.data = None
    submitfuncGuard("Osteoarthritis")
elif st.session_state.data == "AI":
    st.session_state.data = None
    AIfuncGuard("Osteoarthritis")
elif st.session_state.data == "imagePage":
    st.session_state.data = None
    imagePage()
else:
    imageUploader(st.session_state.role)
