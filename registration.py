# registration.py
import streamlit as st
from firebase_admin import auth
from firebase_config import db

def register_user(email, password, name, phone):
    try:
        # Create a user with Firebase Authentication
        user = auth.create_user(email=email, password=password)
        
        # Store additional user information in Firestore
        user_ref = db.collection("users").document(user.uid)
        user_ref.set({
            "name": name,
            "email": email,
            "phone": phone,
            "purpose": ""
        })
        
        st.success("Registration successful! You can now log in.")
    except auth.EmailAlreadyExistsError:
        st.error("Email already exists.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def show_registration():
    st.title("Register")

    # Registration form fields
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    password = st.text_input("Password", type="password")
    
    if st.button("Register"):
        register_user(email, password, name, phone)
