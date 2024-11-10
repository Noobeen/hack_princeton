import streamlit as st
from streamlit_option_menu import option_menu
import streamlit as st
from st_clickable_images import clickable_images


def run_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        file_content = file.read()
    exec(file_content, globals())



# Function to display character selection page with 4 buttons per row
def index_page():
    st.title("Welcome to the gateway where space and time converge")
    st.write("""Try introducing yourself to one of the following prominent individuals from our recent and ancient history.
            """)
    
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
    titles=[f"Image #{str(i)}" for i in range(5)],
    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
    img_style={"margin": "5px", "height": "200px"},
)

    if clicked==1:
        run_file("buddha.py")

    st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")


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



