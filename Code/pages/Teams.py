import streamlit as st
from PIL import Image
from st_pages import Page, show_pages, add_page_title, hide_pages

st.set_page_config(page_title="Teams", page_icon="👥", initial_sidebar_state="expanded")

# logo
logo = Image.open("assets/logo.png")
st.logo(logo)

#Title
st.write("## Team")

# Button Styling
st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)

hide_pages(["Login", "Teams"])

st.sidebar.markdown("""
    <style>
        .sidebar-content > div:nth-child(1) > div > div {color: white}
        .sidebar-content > div:nth-child(1) > div > div > span {color: #FFA500}
    </style>
""", unsafe_allow_html=True)

# if st.sidebar.button("👥 Team"):
#     st.switch_page("pages/Teams.py")
            
if st.sidebar.button("🔓 Logout"):
    st.switch_page("LoginScreen.py")

#Creating columns
col0, col01, col02, col03 = st.columns(4)

with col03:
    
    add = st.button('**⊹ Add New Team Member**')

###################
col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border= True, height= 145):
        # st.image(Image.open("silhouette.png"))
        st.write("**<center>Ahmed Bilal</center>**", unsafe_allow_html=True)
        # st.write("**Ahmed Bilal**")
        st.caption("<center>Admin<center>", unsafe_allow_html=True)
        st.caption("<center>Username<center>", unsafe_allow_html=True)

with col2:
    with st.container(border= True, height= 145):
        # st.image(Image.open("silhouette.png"))
        st.markdown("**<center>Maida Butt</center>**", unsafe_allow_html=True)
        st.caption("<center>Admin<center>", unsafe_allow_html=True)
        st.caption("<center>Username<center>", unsafe_allow_html=True)


with col3:
    with st.container(border= True, height= 145):
            # st.image(Image.open("silhouette.png"))
            st.markdown("**<center>Anum Rafiq</center>**", unsafe_allow_html=True)
            st.caption("<center>Admin<center>", unsafe_allow_html=True)
            st.caption("<center>Username<center>", unsafe_allow_html=True)


with col4:
    with st.container(border= True, height= 145):
        # st.image(Image.open("silhouette.png"))
        st.markdown("**<center>Hunain Theba</center>**", unsafe_allow_html=True)
        st.caption("<center>Admin<center>", unsafe_allow_html=True)
        st.caption("<center>Username<center>", unsafe_allow_html=True)
    
col5, col6 = st.columns(2)

with col5:
    with st.container(border= True, height= 145):
        st.markdown("**<center>Dr Sajdeen</center>**", unsafe_allow_html=True)
        st.caption("<center>Moderator<center>", unsafe_allow_html=True)
        st.caption("<center>Username<center>", unsafe_allow_html=True)

with col6:
    with st.container(border= True, height= 145):
        st.markdown("**<center>Syeda Maryum<center>**", unsafe_allow_html=True)
        st.caption("<center>Moderator<center>", unsafe_allow_html=True)
        st.caption("<center>Username<center>", unsafe_allow_html=True)
    
##############
##ADDING A NEW TEAM MEMBER

@st.experimental_dialog("Add a New Team Member")
def addScreen():
    
    #creating columns for better formatting:
    col1, col2 =st.columns(2)

    with col1:
        # Name field
        name = st.text_input("Enter the name here", placeholder= "Sara Qalandari")

    with col2:
        # User Type dropdown with new options
        UserType = st.selectbox("User Type", [
            "Admin", 
            "Moderator"
            
        ])

    with col1:
        # User name field
        userName = st.text_input("Enter email/user name here", placeholder= "Sara123/ sq123@gmail.com")
    with col2:
        # Passwords text input
        password = st.text_input("Password", type="password", placeholder= "••••••••••")

    submitted = st.button("Sign Up")
    st.caption(':orange[*Press Esc to Cancel*]') #st.write("Note: Upon clicking Cancel, the form will be closed")

    # Flag to track message box visibility
    show_message_box = st.empty()  # Initially empty element

    if submitted:
        # Check if any of the fields are left unfilled
        if not (name and userName and UserType and password):
            show_message_box.error("Please fill in all fields before submitting.")
        else:
            # Add logic to process form data here 
            st.success(f"User Name {userName} signed up successfully!")

if add:
    addScreen()

##TO DO: Check if we are doing something with the picture?