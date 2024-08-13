import streamlit_authenticator as stauth
hashed_passwords = stauth.Hasher(['specialist', 'doctor', 'patient']).generate()

print(hashed_passwords)
