import streamlit as st
from st_pages import Page, show_pages, add_page_title, hide_pages
from PIL import Image
import time

import sqlalchemy as sa
import pandas as pd

# custom imports
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

# streamlit-authenticator package
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# database information ; will change when db hosting

# Note the double backslashes
# server = 'DESKTOP-67BT6TD\\FONTAINE' # IBAD
# server = 'DESKTOP-HT3NB74' # EMAN
server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA

database = 'DummyPawRescue'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

st.set_page_config(page_title="Login", page_icon="🔐", layout="wide", initial_sidebar_state="collapsed")

# Button Styling
st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)

with open('../config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

st.markdown(hide_img_fs, unsafe_allow_html=True)

fixed_sidebar_width = '''
       <style>
       [data-testid="stSidebar"][aria-expanded="true"]{
           min-width: 250px;
           max-width: 250px;
       }
       '''

st.markdown(fixed_sidebar_width, unsafe_allow_html=True)

@st.experimental_dialog("Reset Your Password")
def reset_pass_dialog():
    st.warning('Contact the administrator to reset your password', icon="ℹ️")
    
    col1, col2, col3, col4, col5, col6 = st.columns([1,0.3,1,1,1,1])
    okay = col3.button("Okay")
    cancel = col4.button("Cancel")

    if okay:
        st.rerun()
    
    elif cancel:
        st.rerun()

logo = Image.open("assets/logo.png")
st.logo(logo)

show_pages(
    [
        Page("LoginScreen.py", "Login", "🔐"),
        Page("pages/01_Dashboard.py", "Dashboard", ":books:"),
    ]
)

hide_pages(["Dashboard"])

# Create two columns
picture, login = st.columns([1,1])  # Adjust the ratio as needed

with picture:
    st.image("assets/cat.jpg", use_column_width=True)

with login:
    st.image("assets/logo.png", width= 350)

    name, logged_in, user_name = authenticator.login(max_concurrent_users = 1, fields={'Form name':'Login', 'Username':'Username', 'Password':'Password', 'Login':'Login'})

    if logged_in:
        st.session_state['user_name'] = user_name
        st.session_state['logged_in'] = True

        with st.spinner('Logging in...'): # is this really necessary? lmao
            time.sleep(2)

        container = st.empty()
        container.success(f'Welcome, {user_name.title()}!') # Create a success alert
        time.sleep(3)  # Wait 3  seconds
        container.empty()  # Clear the success alert

        st.switch_page("pages/01_Dashboard.py")
    
    elif not logged_in: # change condition...smth like wronguser name or wrong password ka check ho then aye ye msg.. u can copy opar container wala method for time delay
        st.info('Please enter your correct username and password')     
        
        # container = st.empty()
        # container.info('Please enter your correct username and password')
        # time.sleep(3)  # Wait 3  seconds
        # container.empty()  # Clear the success alert

    # col1, col2, col3, col4= st.columns(4)
    forget_button = st.button("Forgot Password?")
    
    if forget_button: # ask Maida if we actually need to add reset password functionality.
        reset_pass_dialog()

    # Do something about the forgotten password thingy
    # Do something about the login attempts. if not zero then show Login Failed or something.