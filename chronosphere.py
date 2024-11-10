import streamlit as st
from streamlit_option_menu import option_menu
from st_clickable_images import clickable_images

# Function to execute code from the selected file
def run_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        file_content = file.read()
    exec(file_content, globals())

# Function to display character selection page with 4 buttons per row
def index_page():
    st.title("Welcome to the gateway where space and time converge")
    st.write("""Try introducing yourself to one of the following prominent individuals from our recent and ancient history.""")

    # Display clickable images for character selection
    clicked = clickable_images(
        [
            "https://github.com/Noobeen/hack_princeton/blob/main/images/characters/buddha.jpg?raw=true",
            "https://github.com/Noobeen/hack_princeton/blob/main/images/characters/einstein.jpg?raw=true",
            "https://github.com/Noobeen/hack_princeton/blob/main/images/characters/gandhi.jpg?raw=true",
            "https://github.com/Noobeen/hack_princeton/blob/main/images/characters/elon.jpg?raw=true",
            "https://github.com/Noobeen/hack_princeton/blob/main/images/characters/vinci.jpg?raw=true",
            "https://github.com/Noobeen/hack_princeton/blob/main/images/characters/cleo.jpg?raw=true",
            "https://github.com/Noobeen/hack_princeton/blob/main/images/characters/socrates.jpg?raw=true",
            "https://github.com/Noobeen/hack_princeton/blob/main/images/sudip.jpg?raw=true",
        ],
        titles=[f"Image #{str(i)}" for i in range(8)],
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "5px", "height": "200px"},
    )
    return clicked

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

# Initialize state to track selected character page
if "character_page" not in st.session_state:
    st.session_state.character_page = -1  # -1 indicates main selection page

# Render different sections based on the selected option
if selected == "Character Selection":
    if st.session_state.character_page == -1:
        # Show character selection page
        clicked = index_page()

        # Check which image was clicked and set character page
        if clicked == 0:
            st.session_state.character_page = "buddha.py"
        elif clicked == 1:
            st.session_state.character_page = "einstein.py"
        elif clicked == 2:
            st.session_state.character_page = "gandi.py"
        elif clicked == 3:
            st.session_state.character_page = "musk.py"
        elif clicked == 4:
            st.session_state.character_page = "davinci.py"
        elif clicked == 5:
            st.session_state.character_page = "cleo.py"
        elif clicked == 6:
            st.session_state.character_page = "socrates.py"
        elif clicked == 7:
            st.session_state.character_page = "sudi.py"
    else:
        # Display the selected character page and back button
        st.button("⬆️ Back", on_click=lambda: st.session_state.update({"character_page": -1}))
        run_file(st.session_state.character_page)
elif selected == "About Us":
    run_file("aboutUs.py")



