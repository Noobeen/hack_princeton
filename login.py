# login.py
import streamlit as st
from firebase_config import auth, db
from firebase_admin import auth as firebase_auth

def login_user(email, password):
    try:
        # Retrieve user by email
        user = firebase_auth.get_user_by_email(email)
        
        # Check if user exists in Firestore
        user_ref = db.collection("users").document(user.uid).get()
        if user_ref.exists:
            st.session_state['logged_in'] = True
            st.session_state['user_id'] = user.uid
            st.success("Login successful!")
            return True
        else:
            st.error("User data not found in database.")
    except firebase_auth.UserNotFoundError:
        st.error("User not found.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    return False

def show_login():
    st.title("Login")

    # Login form fields
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        login_success = login_user(email, password)
        if login_success:
            st.experimental_rerun()
