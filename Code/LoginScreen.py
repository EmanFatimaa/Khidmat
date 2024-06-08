import streamlit as st
from st_pages import Page, show_pages, add_page_title, hide_pages
from PIL import Image
import time

@st.experimental_dialog("Reset Your Password")
def reset_pass_dialog():
    st.write("Contact the administrator to reset your password.")

st.set_page_config(page_title="Login", page_icon="🔐", layout="wide", initial_sidebar_state="collapsed")

logo = Image.open("assets/logo.png")
st.logo(logo)

show_pages(
    [
        Page("LoginScreen.py", "Login", "🔐"),
        Page("pages/01_Dashboard.py", "Dashboard", ":books:"),
    ]
)

hide_pages(["Dashboard"])

st.markdown("""
    <style>
        .css-18e3th9 {padding: 0;}
        .css-1d391kg {padding: 0; margin: 0; width: 100%;}
        .main {padding: 0; margin: 0;}
        .block-container {padding: 0;}
        .stTextInput > div > div > input {
            width: 200px; /* Adjust the width as needed */
            margin: 0 auto; /* Center the input fields */
        }
        .stButton button {
            background-color: orange; /* Change the login button color to orange */
            color: black; /* Set the text color of the button to white */
            width: 200px; /* Match the width of the input fields */
            margin: 0 auto; /* Center the button */
        }
        a {
            color: orange !important; /* Change the forgot password link color to orange */
            text-align: center; /* Center the link */
            display: block; /* Display the link as a block element */
            margin-top: 10px; /* Add margin to the top */
        }
        .header {
            text-align: center;
            
        }
    </style>
""", unsafe_allow_html=True)

# Create two columns
picture, login = st.columns(2)  # Adjust the ratio as needed

with picture:
    st.image("assets/cat.jpg", use_column_width=True)

with login:
    
    # st.markdown("""
    #     <h2 class="header">
    #         <span style='color: orange;'>PAW</span> 
    #         <span style='color: white;'>RESCUE</span>
    #     </h2>
    # """, unsafe_allow_html=True)
    st.write("# ")
    st.image("assets/logo.png", width= 350)
    st.markdown("## Login")

    buff, col3, buff2 = st.columns([1,3,1])
    buff, col5, buff2 = st.columns([3.2,5,1]) # hardcoded centering, check this when aesthetics are important

    email = col3.text_input("Username", key="email")
    password = col3.text_input("Password", type="password", key="password")
    
    if email and password:
        if col5.button("Login"):

            with st.spinner('Logging in...'):
                time.sleep(2)
                # st.success('Logged in successfully')
                st.switch_page("pages/01_Dashboard.py")
    else:
        col5.button("Login", disabled=True)

    forget_button = col5.button("Forgot Password?")

    if forget_button:
        reset_pass_dialog()