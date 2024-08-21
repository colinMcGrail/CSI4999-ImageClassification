from library.elements import *
import streamlit as st
import sqlite3

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
else:
    imageUploader(st.session_state.role)
