import streamlit as st
import base64

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Get base64 images
nabin_img = get_img_as_base64("images/nabin.jpg")
prameya_img = get_img_as_base64("images/prameya.jpg")
kishor_img = get_img_as_base64("images/kishor.png")
sudip_img = get_img_as_base64("images/sudip.jpg")

st.markdown(
    """
    <style>
    /* Expand the content width without changing the nav bar or sidebar */
    .block-container {
        padding-left: 0rem;
        padding-right: 0rem;
        width: 100%;
    }
    .about-section {
        padding: 50px;
        text-align: center;
        color: white;
        background-color: rgba(0,0,0,0);
        width: 100%;
    }
    .team-member {
        text-align: center;
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 8px;
        color: white;
        height: 580px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        width: 100%;
    }
    .team-member img {
        width: 100%;
        border-radius: 8px;
        height: 200px;
        object-fit: cover;
        margin-bottom: 15px; 
    }
    .team-member h3, .team-member p, .team-member .button {
        margin: 0;
    }
    .team-member h3 {
        font-size: 18px;
        height: 40px;
        margin-bottom: 20px;  
        align: center;
    }
    .team-member .title {
        font-size: 14px;
        height: 30px;
        margin-bottom: 50px; 
    }
    .team-member p.university {
        font-size: 14px;
        height: 30px;
        margin-bottom: 20px;  
    }
    .team-member p.email {
        font-size: 14px;
        height: 20px;
        margin-bottom: 35px; 
    }
    .button {
        border: none;
        padding: 8px;
        color: black;
        background-color: white;
        text-align: center;
        cursor: pointer;
        width: 100%;
        text-decoration: none;
    }
    .button:hover {
        background-color: #555;
    }
    [data-testid="stHorizontalBlock"] {
        width: 100% !important;
        margin: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# About Section
st.markdown(
    """
    <div class="about-section">
        <h1 style="text-align: center; color: #fff; text-transform: uppercase; font-size: 50px;">About <span style="color: #00fecb;">Us</span></h1>
        <p style="border-color: tomato;font-family: monospace;">"Solo commitment, embedded movement"</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Welcome message
st.markdown(
   """
    <div style="background-color: rgba(0,0,0,0); padding: 10px;">
        <p style="color:#fff;">Welcome! We’re excited to introduce you to “Chronosphere.” The place, where people from different timelines and perspectives come together at a common ground and learn.
        An interesting way to communicate with your favorite characters from curriculum as well as non-curriculum books.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Team Section Title
st.markdown(
    """
    <h2 style="text-align:center;color:white;font-size: 30px;">Our Team</h2>
    <hr>
    """,
    unsafe_allow_html=True
)

# Team members information
team_members = [
    {
        "name": "Nabin Oli",
        "degree": "B.S. in Computer Science and Mathematics (Class of 2028)",
        "university": "Caldwell University, NJ",
        "email": "oli.nabin1729@gmail.com",
        "linkedin": "https://www.linkedin.com/in/nabin-oli-4b7132276/",
        "image": nabin_img,
    },
    {
        "name": "Prameya Dhaubadhel",
        "degree": "B.S. in Computer Science (Class of 2028)",
        "university": "Caldwell University, NJ",
        "email": "dhaubhadelprameya@gmail.com",
        "linkedin": "https://www.linkedin.com/in/prameya-dhaubhadel/",
        "image": prameya_img
    },
    {
        "name": "Kishor Baniya",
        "degree": "B.S. in Computer Science and Mathematics (Class of 2028)",
        "university": "Caldwell University, NJ",
        "email": "kishorbaniya15@gmail.com",
        "linkedin": "https://www.linkedin.com/in/kishor-baniya-7164bb213/",
        "image": kishor_img
    },
    {
        "name": "Sudip Kumar Thakur",
        "degree": "B.S. in Computer Science (Class of 2028)",
        "university": "Caldwell University, NJ",
        "email": "sthakur3@caldwell.edu",
        "linkedin": "https://www.linkedin.com/in/sudip-kumar-thakur-460599331/",
        "image": sudip_img
    }
]

# Display team members in rows and columns
cols = st.columns(len(team_members))  # Create dynamic columns for each member

for i, member in enumerate(team_members):
    with cols[i]:  # Access each column for each member
        st.markdown(
            f"""
            <div class="team-member">
                <img src="data:image/png;base64,{member['image']}" alt="{member['name']}">
                <h3>{member['name']}</h3>
                <p class="title">{member['degree']}</p>
                <p class="university">{member['university']}</p>
                <p class="email">{member['email']}</p>
                <a class="button" target="_blank" href="{member['linkedin']}">Contact</a>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<hr style='width: 100%;'>", unsafe_allow_html=True)
