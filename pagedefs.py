import streamlit as st

def logout():
    st.session_state.role = None
    st.rerun()

login_page = st.Page("page/general/login.py", title="Log in")
signup_page = st.Page("page/general/signup.py", title="Sign up")
specialistLanding = st.Page("page/role/specialist/specialist.py", title="Home")
patientLanding = st.Page("page/role/patient/patient.py", title="Home")
physicianLanding = st.Page("page/role/physician/physician.py", title="Home")
osteoarthmodel = st.Page("page/model/osteoarthritis.py", title="Osteoarthritis Diagnostic")

generalPages = []
specialistPages = [specialistLanding]
patientPages = [patientLanding]
physicianPages = [physicianLanding]
modelPages = [osteoarthmodel]
