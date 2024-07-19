# standard imports 
from datetime import datetime, date, time  # Correct import
from PIL import Image
import io

# third party imports
import sqlalchemy as sa
import streamlit as st
import pandas as pd

# custom imports
from millify import prettify
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

# custom streamlit imports
from st_pages import Page, show_pages, add_page_title, hide_pages

# streamlit-authenticator package
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Make the file from the database each time and every time we update or add a new user!
# Right now it only works for the 7 people that should also be in the database

# Note the double backslashes
# server = 'DESKTOP-67BT6TD\\FONTAINE' # IBAD
# server = 'DESKTOP-HT3NB74' # EMAN
server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA

database = 'PawRescue'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

st.set_page_config(page_title="Teams", page_icon="👥", initial_sidebar_state="expanded")

# logo
logo = Image.open("assets/logo.png")
st.logo(logo)

#Title
st.header("Team", divider='orange')

# Button Styling
st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)

hide_pages(["Login"])

st.markdown(
        """
       <style>
       [data-testid="stSidebar"][aria-expanded="true"]{
           min-width: 250px;
           max-width: 250px;
       }
       """,
        unsafe_allow_html=True,
)

def add_team_dialog():
    st.session_state.show_add_team_dialog = True
    st.session_state.show_edit_team_dialog = False

def edit_team_dialog():
    st.session_state.show_add_team_dialog = False
    st.session_state.show_edit_team_dialog = True

col1, col2 = st.columns([1, 3])
with col1:
    add_button = st.button("✙ Add New Member", on_click=add_team_dialog)
with col2:
    update_button = st.button("Update Member Details", on_click = edit_team_dialog)

query = "SELECT userName, email, roleDesc, picture FROM Users inner join InternalRole on InternalRole.internalRoleID = Users.internalRoleID"  # Adjust the query to your database structure
with engine.begin() as conn:
    team_member_df = pd.read_sql_query(query, conn)


cols = st.columns(4)
for i, member in team_member_df.iterrows():
    with cols[i % 4]:
        with st.container(border=True, height = 290):
            if member['picture']:
                image = Image.open(io.BytesIO(member['picture']))
                st.image(image, use_column_width='auto')
            st.write(f"**<center>{member['userName']}</center>**", unsafe_allow_html=True)
            st.caption(f"<center>{member['roleDesc']}</center>", unsafe_allow_html=True)
            st.caption(f"<center>{member['email']}</center>", unsafe_allow_html=True)


@st.experimental_dialog("Add a New Member")
def addScreen():
    with engine.begin() as conn:
        id = int(pd.read_sql_query(sa.text("SELECT TOP 1 userID FROM Users ORDER BY userID DESC"), conn).iat[0,0]) + 1
    user_id = st.text_input("User ID", value = id, disabled=True)
            
    image = st.file_uploader("Upload Photo", type='png')

    col1, col2 =st.columns(2)

    with col1:
        # Name field
        name = st.text_input("Name", placeholder= "Sara Qalandari")

    with col2:
        with engine.begin() as conn:
            df = pd.read_sql_query("SELECT roleDesc FROM InternalRole", conn)
            user = df['roleDesc'].tolist()
        UserType = st.selectbox("Role", user)

    with col1:
        # User name field
        email = st.text_input("Email Address", placeholder= "sq123@gmail.com")
    with col2:
        # Passwords text input
        password = st.text_input("Password", type="password", placeholder= "••••••••••")

    submitted = st.button("Add Member")

    # Flag to track message box visibility
    show_message_box = st.empty()  # Initially empty element

    if submitted:

        everything_filled = False
        valid_name = False
        valid_email = False
        valid_password = False
        # Check if any of the fields are left unfilled


        if not (user_id and name and email and UserType and password):
            show_message_box.error("Please fill in all fields before submitting.")
        else:
            everything_filled = True
        
        if all(x.isalpha() or x.isspace() for x in name):
            valid_name = True
        else:
            st.error("Please enter a valid name.")

        if (len(password)>=0 and len(password)<8):
            st.error("Password should be atleast 8 characters long.")
        else:
            valid_password = True

        if ('@' in email):
            valid_email = True
        else:
            st.error("Please enter valid Email")

        if everything_filled and valid_name and valid_email and valid_password:
            with engine.begin() as conn:
                image_bytes = image.read() if image else None
                conn.execute(sa.text("""
                INSERT INTO Users (userID, userName, email, password, picture, internalRoleID)
                VALUES (:userID, :userName, :email, :password, :picture, 
                (SELECT internalRoleID FROM InternalRole WHERE roleDesc = :roleDesc))
            """), {
                "userID": user_id,
                "userName": name,
                "email": email,
                "password": password,
                "picture": image_bytes,
                "roleDesc": UserType
                })
            
            # Add a new user in the config file
            config['credentials']['usernames'][name.lower()] = {
                'email': email,
                'failed_login_attempts': 0,
                'logged_in': False,
                'name': name,
                'password': password
            }
            
            with open('../config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
    
            st.rerun()
        # st.success(f"{name} added to team successfully!")
    
    st.session_state.show_add_team_dialog = False
    st.caption('_:orange[Press Esc to Cancel]_')

@st.experimental_dialog("Edit Team Member")
def edit_team():
    with engine.begin() as conn:
            df = pd.read_sql_query("SELECT userName FROM Users", conn)
            user_value = df['userName'].tolist()
    user_name = str(st.selectbox("Member Name", user_value))

    with engine.begin() as conn:
        picture_value = conn.execute(sa.text("select picture from Users where userName = :userName"), {"userName": user_name}).fetchall()[0][0]
    if picture_value:
        current_image = Image.open(io.BytesIO(picture_value))
        st.image(current_image, caption= "Current Photo", width=150)
    new_image = st.file_uploader("Upload New Photo", type='png')

    # with col1:
    #     with engine.begin() as conn:
    #         name_value = conn.execute(sa.text("select userName from Users where userID = :userID"), {"userID": user_id}).fetchall()[0][0]
    #     current_name = st.text_input("Name", value = name_value)

    with engine.begin() as conn:
        role = conn.execute(sa.text("select roleDesc from InternalRole where internalRoleID = (Select internalRoleID from Users where userName = :userName)"), {"userName": user_name}).fetchall()[0][0]
        df = pd.read_sql_query("SELECT roleDesc FROM InternalRole", conn)
        update_role = df['roleDesc'].tolist()
    final_role_index = update_role.index(role)

    current_role = st.selectbox("Role", update_role, index = final_role_index)

    col1, col2 =st.columns(2)

    with col1:
        with engine.begin() as conn:
            email_value = conn.execute(sa.text("select email from Users where userName = :userName"), {"userName": user_name}).fetchall()[0][0]
        current_email = st.text_input("Email", value = email_value)

    with col2:
        with engine.begin() as conn:
            password_value = conn.execute(sa.text("select password from Users where userName = :userName"), {"userName": user_name}).fetchall()[0][0]
        current_password = st.text_input("Password", value = password_value)

    if st.button("Save Changes"):
        everything_filled = False
        valid_email = False
        valid_password = False
        # Check if any of the fields are left unfilled


        if not (current_email and current_password):
            st.error("Please fill in all fields before submitting.")
        else:
            everything_filled = True

        if (len(current_password)>=0 and len(current_password)<8):
            st.error("Password should be atleast 8 characters long.")
        else:
            valid_password = True

        if ('@' not in current_email):
            st.error("Please enter valid Email")
        else:
            valid_email = True


        if (valid_email and valid_password and everything_filled):
            with engine.begin() as conn:
                internal_role_id = conn.execute(sa.text("SELECT internalRoleID FROM InternalRole WHERE roleDesc = :roleDesc"), {"roleDesc": current_role}).fetchall()[0][0]
                if new_image:
                    image_bytes = new_image.read()
                    conn.execute(sa.text(""" 
                        UPDATE Users
                        SET userName = :userName, email = :email, password = :password, internalRoleID = :internalRoleID, picture = :picture
                        WHERE userName= :userName
                        """), {
                        "userName": user_name,
                        "email": current_email,
                        "password": current_password,
                        "internalRoleID": internal_role_id,
                        "picture": image_bytes,
                    })
                else:
                    conn.execute(sa.text(""" 
                        UPDATE Users
                        SET userName = :userName, email = :email, password = :password, internalRoleID = :internalRoleID
                        WHERE userName = :userName
                        """), {
                        "userName": user_name,
                        "email": current_email,
                        "password": current_password,
                        "internalRoleID": internal_role_id,
                    })
            
            # Update the user in the config file
            config['credentials']['usernames'][user_name.lower()] = {
                'email': current_email,
                'failed_login_attempts': 0,
                'logged_in': False,
                'name': user_name,
                'password': current_password
            }
            
            with open('../config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            
            st.rerun()

    st.session_state.show_edit_team_dialog = False
    st.caption('_:orange[Press Esc to Cancel]_')

if 'show_add_team_dialog' not in st.session_state:
    st.session_state.show_add_team_dialog = False
if 'show_edit_team_dialog' not in st.session_state:
    st.session_state.show_edit_team_dialog = False

if st.session_state.show_add_team_dialog:
    addScreen()

if st.session_state.show_edit_team_dialog:
    edit_team()

with open('../config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

name, logged_in, user_name = authenticator.login()

st.sidebar.write(f"Logged in as: _:orange[{name}]_")

with engine.connect() as conn:
    role = conn.execute(sa.text("select roleDesc from InternalRole, Users where Users.internalRoleID = InternalRole.internalRoleID and Users.userName = :name"), {"name":name}).fetchone()[0]

st.sidebar.write(f"Role: _:orange[{role}]_")

if st.sidebar.button("🔓 Logout"):
    authenticator.logout(location = "unrendered")
    st.switch_page("LoginScreen.py")