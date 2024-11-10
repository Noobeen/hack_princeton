import streamlit as st
from streamlit_option_menu import option_menu
import base64

# Function to read image as base64
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to display character selection page with 4 buttons per row
def index_page():
    st.title("Welcome to the gateway where space and time converge")
    st.write("""Try introducing yourself to one of the following prominent individuals from our recent and ancient history.
            """)
    
    # List of characters and their image filenames
    characters = [
        {"name": "Buddha", "image": "images/characters/buddha.jpg"},
        {"name": "Cleo", "image": "images/characters/cleo.jpg"},
        {"name": "Einstein", "image": "images/characters/einstein.jpg"},
        {"name": "Elon", "image": "images/characters/elon.jpg"},
        {"name": "Gandhi", "image": "images/characters/gandhi.jpg"},
        {"name": "Socrates", "image": "images/characters/socrates.jpg"},
        {"name": "Vinci", "image": "images/characters/vinci.jpg"},
        {"name": "Sudi", "image": "images/sudip.jpg"}
    ]

    for row in range(2):  # 2 rows (since there are 6 characters, 3 per row)
        cols = st.columns(4)
        for i in range(4):
            char_index = row * 4 + i
            if char_index >= len(characters):  # Avoid index out of range if there are fewer characters than expected
                break
            char_name = characters[char_index]["name"]
            img_path = characters[char_index]["image"]
            img_base64 = get_img_as_base64(img_path)
            
            with cols[i]:
                # Display button with an image inside
                button_html = f"""
                <button style="background-image: url(data:image/jpg;base64,{img_base64}); 
                                background-size: cover; 
                                width: 100%; height: 160px; 
                                border: none; cursor: pointer;">
                </button>
                """
                if st.markdown(button_html, unsafe_allow_html=True):
                    pass

def run_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        file_content = file.read()
    exec(file_content, globals())

# Navigation Bar
selected = option_menu(
    menu_title=None,
    options=["Character Selection", "About Us"],
    icons=["person-fill", "info-circle"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {},
        "icon": {"color": "white"},
        "nav-link": {
            "margin": "0px",
            "--hover-color": "#eee",
        },
        "nav-link-selected": {"background-color": "#00004d"},
    },
)

# Render different sections based on the selected option
if selected == "Character Selection":
    index_page()
elif selected == "About Us":
    run_file("aboutUs.py")
