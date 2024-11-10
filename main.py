# main.py
import streamlit as st
from registration import show_registration
from login import show_login
from firebase_config import db

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_id'] = None
    st.session_state['purpose_set'] = False

def select_purpose(user_id):
    st.subheader("Select Your Purpose")
    purpose = st.selectbox("Purpose", ["", "Learn", "Collaborate", "Consult"])
    if st.button("Submit"):
        if purpose:
            db.collection("users").document(user_id).update({"purpose": purpose})
            st.success("Purpose updated successfully!")
            st.session_state['purpose_set'] = True
        else:
            st.error("Please select a purpose.")

# Main Application Logic
st.sidebar.title("Navigation")
if st.session_state['logged_in']:
    st.sidebar.write("You are logged in.")
    
    # Purpose selection if not set
    if not st.session_state['purpose_set']:
        select_purpose(st.session_state['user_id'])
    else:
        st.write("Thank you for selecting your purpose.")
        
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['user_id'] = None
        st.session_state['purpose_set'] = False
        st.experimental_rerun()
else:
    # Toggle between Login and Register pages
    choice = st.sidebar.radio("Choose an option", ["Login", "Register"])
    if choice == "Register":
        show_registration()
    elif choice == "Login":
        show_login()
