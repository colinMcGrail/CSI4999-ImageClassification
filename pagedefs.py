import streamlit as st

def logout():
    st.session_state.role = None
    st.rerun()

login_page = st.Page("login.py", title="Log in")
signup_page = st.Page("signup.py", title="Sign up")
specialistLanding = st.Page("roles/specialist/specialist.py")
patientLanding = st.Page("roles/patient/patient.py")
physicianLanding = st.Page("roles/physician/physician.py")
osteoarthmodel = st.Page("model/osteoarthritis.py")

generalPages = [logout]
specialistPages = [specialistLanding]
patientPages = [patientLanding]
physicianPages = [physicianLanding]
modelPages = [osteoarthmodel]
