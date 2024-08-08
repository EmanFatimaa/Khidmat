# standard imports 
from datetime import datetime, date, time  # Correct import
from PIL import Image
import time

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

# database information ; will change when db hosting
server = 'DESKTOP-67BT6TD\\FONTAINE' # IBAD
# server = 'DESKTOP-HT3NB74' # EMAN
# server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA

database = 'DummyPawRescue'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

st.set_page_config(page_title="Treatments", page_icon="💊", initial_sidebar_state="expanded", layout="wide")

def implement_markdown():
    # Button Styling
    st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)

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

    # Sidebar better
    st.sidebar.markdown(""" <style> [data-testid='stSidebarNav'] > ul { min-height: 54vh; } </style> """, unsafe_allow_html=True) 

# logo
logo = Image.open("assets/logo.png")
st.logo(logo)

implement_markdown()

hide_pages(["Login"])

# Creating columns for better formatting
col1, col2, col3, col4 = st.columns(4)

st.header("Treatment", divider='orange')

#Funciton to extract number from cat id
def extract_cat_number(cat_id_str):
    # Remove the prefix "PA-"
    numberStr = cat_id_str.replace("PR-", "")
    
    # Convert to integer
    numberInt = int(numberStr)
    
    return numberInt

def add_treatment_dialog():
    st.session_state.show_add_treatment_dialog = True
    st.session_state.show_update_treatment_dialog = False
    st.session_state.show_delete_treatment_dialog = False

def update_treatment_dialog():
    st.session_state.show_add_treatment_dialog = False
    st.session_state.show_update_treatment_dialog = True
    st.session_state.show_delete_treatment_dialog = False

def delete_treatment_dialog():
    st.session_state.show_add_treatment_dialog = False
    st.session_state.show_update_treatment_dialog = False
    st.session_state.show_delete_treatment_dialog = True

@st.experimental_dialog("Add Treatment")
def add_treatment(ID_to_add=None):

    with engine.begin() as conn:
        treatmentid = int(pd.read_sql_query(sa.text("SELECT TOP 1 treatmentID FROM Treatment ORDER BY treatmentID DESC"), conn).iat[0,0]) + 1
        df = pd.read_sql_query("SELECT catID FROM Cats where catID IS NOT NULL", conn)
        if ID_to_add is None:
            current_catID = 1
        else:
            current_catID = int(conn.execute(sa.text("select catId from Treatment where treatmentid = :t"), {"t":ID_to_add}).fetchall()[0][0])

    df['catID'] = df['catID'].apply(lambda x: f"PR-{str(x).zfill(5)}")
    catcode_id = df['catID'].tolist()

    col1, col2 = st.columns(2)
    with col1:
        selected_cat_id = st.selectbox("Select CatID", catcode_id, index = current_catID - 1)
        selected_cat_id = extract_cat_number(selected_cat_id)

    with col2:
        with engine.begin() as conn:
            name = conn.execute(sa.text("select catName from Cats where catID= :catID"), {"catID": selected_cat_id}).fetchall()[0][0]
        selected_cat_name = st.text_input('Cat Name', value = name)

    col1, col2 = st.columns(2)
    
    with col1:
        treatment_time = st.time_input("Time")
    
    with col2:
        treatment_date = st.date_input("Treatment Date") 

    col1, col2 = st.columns(2)
    with col1:
        temperature = st.text_input("Temperature", value=float(100))
    with col2:
        with engine.begin() as conn:
            df = pd.read_sql_query("SELECT userName FROM Users", conn)
            user = df['userName'].tolist()
        # givenby = st.selectbox("Given By", user)
        givenby = st.text_input("Given By", value = st.session_state.user_name.title(), disabled=True)
    
    treatment_details = st.text_area("Treatment Details", placeholder="IV given, dressing done", value = '')

    add_treatment_button = st.button("Add Treatment", key="add_treatment")

    if add_treatment_button:
        print("button pressed")
        # check other individual fields for errors as well.
        everything_filled = False
        valid_treatment =   False

        if all(x.isalpha() or x.isspace() or x=='.' for x in treatment_details):
            valid_treatment = True
        else:
            st.error("Please enter valid treatment details.")

        # Check if any of the fields are left unfilled
        if not (id and selected_cat_name and treatment_time and temperature and givenby and treatment_date and treatment_details):
            st.error("Please fill in all fields before submitting.")
        else: 
            date_and_time = datetime.combine(treatment_date, treatment_time)
            everything_filled = True

        if everything_filled and valid_treatment:
            with engine.begin() as conn:
                catid = conn.execute(sa.text("""SELECT catID FROM Cats WHERE catName = :catName"""), {"catName": selected_cat_name}).fetchone()[0] 
                userid = conn.execute(sa.text("""SELECT UserID FROM Users WHERE userName = :userName"""), {"userName": givenby}).fetchone()[0] 
                conn.execute(sa.text("""
                    INSERT INTO Treatment (TreatmentID, CatID, UserID, DateTime, Temperature, Treatment)
                    VALUES (:treatmentID, :CatID, :UserID, :DateTime, :Temperature, :Treatment)
                """), {
                    "treatmentID": treatmentid,
                    "CatID": catid,
                    "UserID" : userid,
                    "DateTime": date_and_time,
                    "Temperature": temperature,
                    "Treatment": treatment_details              
                })
            st.rerun()
    
    st.session_state.show_add_treatment_dialog = False
    st.caption('_:orange[Press Esc to Cancel]_')

@st.experimental_dialog("Update Treatment") # , width='large')
def update_treatment(ID_to_update):

    col1, col2 = st.columns(2)

    with engine.begin() as conn:
        df = pd.read_sql_query("SELECT CatID FROM Cats", conn)
        current_catID = int(conn.execute(sa.text("select catId from Treatment where treatmentid = :t"), {"t":ID_to_update}).fetchall()[0][0])
    cat_ids = df['CatID'].tolist()
    with col1:
        selected_cat_code_id = st.selectbox("Select Cat ID", map(lambda x: f"PR-{str(x).zfill(5)}", cat_ids), index = current_catID - 1)
        selected_cat_id = extract_cat_number(selected_cat_code_id)

    with col2:
        with engine.begin() as conn:
            name = conn.execute(sa.text("select catName from Cats where catID= :catID"), {"catID": selected_cat_id}).fetchall()[0][0]
        st.text_input('Cat Name', value = name)

    col1, col2 = st.columns(2)
        
    with col1:
        with engine.begin() as conn:
            time_value = conn.execute(sa.text("select dateTime from Treatment where treatmentID = :treatmentID"), {"treatmentID": ID_to_update}).fetchall()[0][0]
        time_only = time_value.time()
        Time = st.time_input("Time", value=time_only)
    
    with col2:
        with engine.begin() as conn:
            date_value = conn.execute(sa.text("select convert(date, dateTime) from Treatment where treatmentID = :treatmentID"), {"treatmentID": ID_to_update}).fetchall()[0][0]
        date = st.date_input("Date", value=date_value)

    col1, col2 = st.columns(2)
        
    with col1:
        with engine.begin() as conn:
            temp_value = conn.execute(sa.text("select temperature from Treatment where treatmentID = :treatmentID"), {"treatmentID": ID_to_update}).fetchall()[0][0]
        temperature = st.number_input("Temperature", value=float(temp_value))
    
    with col2:
        with engine.begin() as conn:
            user_value = conn.execute(sa.text("select userName from Users where userID = (select userID from Treatment where treatmentID = :treatmentID)"), {"treatmentID": ID_to_update}).fetchall()[0][0]
            df = pd.read_sql_query("SELECT userName FROM Users where userName is not NULL", conn)
            update_user = df['userName'].tolist()

        final_user_index = update_user.index(user_value)
        # print(final_user_index)
        user = st.selectbox("Given By", update_user, index = final_user_index)

        with engine.begin() as conn:
            Userid = conn.execute(sa.text("""SELECT UserID FROM Users WHERE userName = :userName"""), {"userName": user}).fetchall()[0][0]

    with engine.begin() as conn:
        treatment_value = conn.execute(sa.text("select treatment from Treatment where treatmentID = :treatmentID"), {"treatmentID": ID_to_update}).fetchall()[0][0]
    treatment = st.text_area("Treatment Details", value=treatment_value)

    update_treatment_button = st.button("Save Changes", key = 'update_treatment')

    if update_treatment_button:
        # check other individual fields for errors as well.
        everything_filled = False
        valid_treatment_details =   False
        
        if all(x.isalpha() or x.isspace() or x=='.' for x in treatment):
            valid_treatment_details = True
        else:
            st.error("Please enter valid treatment details for updation.")

        if not (selected_cat_id and Time and date and user and temperature and treatment):
            st.error("Please fill in all fields before submitting.")
        else:
            date_and_time = datetime.combine(date, Time)
            everything_filled = True

        if everything_filled and valid_treatment_details:
            # print(selected_cat_id, Userid, Time, temperature, treatment, ID_to_update)
            with engine.begin() as conn:
                conn.execute(sa.text(""" 
                    UPDATE Treatment
                    SET catID = :catID, userID = :userID, dateTime = :dateTime, temperature = :temperature, treatment = :treatment
                    WHERE treatmentID = :treatmentID
                    """), {"catID": selected_cat_id, "userID": Userid, "dateTime": date_and_time, "temperature": temperature, "treatment": treatment, "treatmentID": ID_to_update})
            st.rerun()

    st.session_state.show_update_treatment_dialog = False  
    st.caption('_:orange[Press Esc to Cancel]_')


@st.experimental_dialog("Delete Treatment")
def delete_treatment(Id_to_delete):
    
    with engine.begin() as conn:
        current_catID = int(conn.execute(sa.text("select catId from Treatment where treatmentid = :t"), {"t":Id_to_delete}).fetchall()[0][0])

    st.write('Are you sure you want to delete this treatment of ID:', f"PR-{str(current_catID).zfill(5)}", '?')

    blank, col1, col2 = st.columns([3,1,1])
    if col1.button("Yes", use_container_width=True):
        with engine.begin() as conn:
            conn.execute(sa.text("update Treatment set catID = NULL, userID = NULL, dateTime = NULL, temperature = NULL, treatment = NULL where treatmentID = :treatmentID"), {"treatmentID": Id_to_delete})
        st.rerun()

    if col2.button("No", key = 'no', use_container_width=True):
        st.rerun()

    st.session_state.show_delete_treatment_dialog = False
    st.caption('_:orange[Press Esc to Cancel]_') 

col1, col2, col3, col4, col5, col6 = st.columns(6)

if 'show_add_treatment_dialog' not in st.session_state:
    st.session_state.show_add_treatment_dialog = False
if 'show_update_treatment_dialog' not in st.session_state:
    st.session_state.show_update_treatment_dialog = False
if 'show_delete_treatment_dialog' not in st.session_state:
    st.session_state.show_delete_treatment_dialog = False

# Table for treatments
with engine.begin() as conn:
    treatment_table_df = pd.read_sql_query(sa.text("""
    SELECT 
        treatmentID as ID,  
        Cats.CatID,
        Cats.CatName AS Name, 
        Cats.CageID AS CageNo, 
        ward.code AS 'Ward Code', 
        Treatment.Temperature AS Temperature, 
        Treatment.Treatment AS Treatment, 
        CONVERT(VARCHAR, Treatment.DateTime, 108) AS Time, 
        convert(date, dateTime) as Date,
        Users.UserName AS GivenBy
    FROM 
        Cats, Treatment, Users, Cage, Ward
        where Treatment.CatID = Cats.CatID and Treatment.UserID = Users.UserID and
        Cage.cageID = Cats.cageID and Cage. wardID = ward.wardID 
    """), conn)

# ----------------------------------------------------------- #

# Generate catCodestr for each catID
treatment_table_df['CatID'] = treatment_table_df['CatID'].apply(lambda x: f"PR-{str(x).zfill(5)}")

treatment_table_df['Date'] = pd.to_datetime(treatment_table_df['Date']).dt.date

st.write('##### :orange[Filters:]')

dates = treatment_table_df['Date'].unique()
cat_id = treatment_table_df['CatID'].unique()

min_date = min(dates)
max_date = max(dates)
    
col1, col2, col3 = st.columns(3)
with col1:
    start_date_value = st.date_input("Select From Date", min_value=min_date, max_value=max_date, value=min_date, key = 'start_date_filter')
with col2:
    end_date_value = st.date_input("Select To Date", min_value=min_date, max_value=max_date, value=max_date, key = 'end_date_filter')
with col3:
    selected_cat_id = st.selectbox("Select CatID", options=["No Filters"] + list(cat_id), index=0, placeholder='Choose an option', key = 'cat_id_filter')

# Reset Filters Button (Do it exactly like this in every page :)
def reset_filters_function():
    st.session_state.start_date_filter = min_date
    st.session_state.end_date_filter = max_date
    st.session_state.cat_id_filter = 'No Filters'

blank, blank, blank, blank, blank, reset = st.columns([3,1,1,1,1,1])

reset_filter_button = reset.button("Reset Filters", on_click=reset_filters_function, use_container_width=True)

# Filter DataFrame based on the selected dates and CatID
if start_date_value and end_date_value:
    filtered_df = treatment_table_df[(treatment_table_df['Date'] >= start_date_value) & (treatment_table_df['Date'] <= end_date_value)]
else:
    filtered_df = treatment_table_df

if selected_cat_id != 'No Filters':
    filtered_df = filtered_df[filtered_df['CatID'] == selected_cat_id]

st.divider()

col1, col2, col3, col4, col5, col6 = st.columns([2,2,2,1,1,1.4])

# Add a New Transaction Button
st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)
new_transaction = col6.button("✙ New Treatment", on_click=add_treatment_dialog, use_container_width=True)

# Convert 'Admitted On' to datetime and format as "date month year"
filtered_df['Date'] = pd.to_datetime(filtered_df['Date']).dt.strftime('%d %b %Y')

# Display the filtered table
try:
    if st.session_state.role == 'Administrator':
        treatment_table = st.dataframe(filtered_df, width=1500, height=600, hide_index=True, column_order = ("CatID", "Name", "CageNo", "Temperature", "Treatment", "Time", "Date", "GivenBy"), on_select='rerun', selection_mode='single-row', use_container_width=True)

        if treatment_table["selection"]["rows"]: # if a row is selected
            
            row_selected = int(filtered_df.iat[treatment_table['selection']['rows'][0], 0])
            # print(treatment_table_df)

            update_button = col4.button("Update", on_click = update_treatment_dialog, use_container_width=True)
            delete_button = col5.button("Delete", on_click = delete_treatment_dialog, use_container_width=True)

            if st.session_state.show_add_treatment_dialog:
                add_treatment(row_selected)

            if st.session_state.show_update_treatment_dialog:
                update_treatment(row_selected)

            if st.session_state.show_delete_treatment_dialog:
                delete_treatment(row_selected)
    else:
        treatment_table = st.dataframe(filtered_df, width=1500, height=600, hide_index=True, column_order = ("CatID", "Name", "CageNo", "Temperature", "Treatment", "Time", "Date", "GivenBy"), use_container_width=True)
except:
    pass

if st.session_state.show_add_treatment_dialog:
    add_treatment()

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

if name is not None:
    with engine.connect() as conn:
        role = conn.execute(sa.text("select roleDesc from InternalRole, Users where Users.internalRoleID = InternalRole.internalRoleID and Users.userName = :name"), {"name":name}).fetchone()[0]        
    st.sidebar.write(f"Role: _:orange[{role}]_")
else:
    st.switch_page("LoginScreen.py")

# empty
st.sidebar.write(" ")
st.sidebar.write(" ")
st.sidebar.write(" ")

if st.sidebar.button("🔓 Logout"):
    with st.sidebar:
        with st.spinner('Logging out...'):
            time.sleep(2)

    authenticator.logout(location = "unrendered")
    st.switch_page("LoginScreen.py")