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

# Database Information

# Windows
# server = 'DESKTOP-67BT6TD\\FONTAINE' # IBAD
# server = 'DESKTOP-HT3NB74' # EMAN
# server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA

# database = 'DummyPawRescue'
# database = 'SchemaPawRescue'

# connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# Linux
server = '127.0.0.1'
database = 'DummyPawRescue'
connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID=sa;PWD=PawRescue!1;TrustServerCertificate=yes;'

connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

st.set_page_config(page_title="Login", page_icon="🔐", layout="wide", initial_sidebar_state="collapsed")

def implement_markdown():
    # Button Styling
    orange_button = '''
    <style>
    div.stButton > button:first-child {
        background-color: #FFA500; 
        color: black}
    </style>
    '''
    st.markdown(orange_button, unsafe_allow_html=True)

    # Hide the fullscreen button
    hide_img_fs = '''
    <style>
    button[title="View fullscreen"]{
        visibility: hidden;}
    </style>
    '''
    st.markdown(hide_img_fs, unsafe_allow_html=True)

    # Fix the sidebar width
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

# ---------------------------------------------------------- #

implement_markdown()

with open('../config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

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
    st.image("assets/cat.jpg", width=580)
    pass

with login:
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.image("assets/logo.png", width= 250)

    name, logged_in, user_name = authenticator.login(max_concurrent_users = 1, fields={'Form name':'Login', 'Username':'Username', 'Password':'Password', 'Login':'Login'})

    if logged_in:
        
        with engine.connect() as conn:
            role = conn.execute(sa.text("select roleDesc from InternalRole, Users where Users.internalRoleID = InternalRole.internalRoleID and Users.userName = :name"), {"name":name}).fetchone()[0]    

        st.session_state['role'] = role
        st.session_state['user_name'] = user_name
        st.session_state['logged_in'] = True

        # container = st.empty()
        st.success(f'Welcome, {user_name.title()}!') # Create a success alert
        # time.sleep(3)  # Wait 3  seconds
        # container.empty()  # Clear the success alert

        st.switch_page("pages/01_Dashboard.py")
    
    # elif not logged_in: # change condition...smth like wronguser name or wrong password ka check ho then aye ye msg.. u can copy opar container wala method for time delay
    #     st.info('Please enter your correct username and password')     
        
    # forget_button = st.button("Forgot Password?")
    
    # if forget_button:
    #     reset_pass_dialog()

# TODO:
# Do something about the forgotten password thingy ; maybe..
# Do something about the login attempts. if not zero then show Login Failed or something.