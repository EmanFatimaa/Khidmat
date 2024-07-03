# standard imports 
import datetime
from PIL import Image

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
from streamlit_dynamic_filters import DynamicFilters

server = 'DESKTOP-67BT6TD\\FONTAINE' # IBAD
# server = 'DESKTOP-HT3NB74' # EMAN
# server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA # Note the double backslashes
database = 'PawRescue'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

st.set_page_config(page_title="Treatments", page_icon="💊", initial_sidebar_state="expanded", layout="wide")

# logo
logo = Image.open("assets/logo.png")
st.image(logo, width=150)

# Button Styling
st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)

st.sidebar.markdown("""
    <style>
        .sidebar-content > div:nth-child(1) > div > div {color: white}
        .sidebar-content > div:nth-child(1) > div > div > span {color: #FFA500}
    </style>
""", unsafe_allow_html=True)

if st.sidebar.button("👥 Team"):
    st.experimental_rerun("pages/Teams.py")
            
if st.sidebar.button("🔓 Logout"):
    st.experimental_rerun("LoginScreen.py")

hide_pages(["Login", "Teams"])

# Creating columns for better formatting
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.header("Treatment")

st.write("Filter By:")

col1, col2 = st.columns([2, 17])
with col1:
    st.button("Cat ID")
with col2:
    st.button("Current Date")

def add_treatment_dialog():
    st.session_state.show_add_treatment_dialog = True

@st.experimental_dialog("Add Treatment")
def add_treatment():

    with engine.begin() as conn:
        treatmentid = int(pd.read_sql_query(sa.text("SELECT TOP 1 treatmentID FROM Treatment ORDER BY treatmentID DESC"), conn).iloc[0][0]) + 1
        df = pd.read_sql_query("SELECT CatID FROM Cats", conn)
        cat_ids = df['CatID'].tolist()
    selected_cat_id = st.selectbox("Select Cat ID", cat_ids)

    col1, col2 = st.columns(2)
    
    with col1:
        # Gender field
        cat_time = st.time_input("Time")
    
    with col2:
        temperature = st.number_input("Temperature", min_value=99, max_value=105, step=1, value=100)

    treatment_details = st.text_area("Treatment Details", placeholder="IV given, dressing done", value = '')

    add_treatment_button = st.button("Add Treatment", key="add_treatment")

    if add_treatment_button:

        # TODO: check other individual fields for errors as well.

        # Check if any of the fields are left unfilled
        if not (selected_cat_id and cat_time and temperature and treatment_details):
            st.error("Please fill in all fields before submitting.")
        
        with engine.begin() as conn:
            userid = conn.execute(sa.text("""SELECT UserID FROM Treatment WHERE CatID = :cat_id"""), {"cat_id": selected_cat_id}).fetchone()[0] 
            conn.execute(sa.text("""
                INSERT INTO Treatment (TreatmentID, CatID, UserID, DateTime, Temperature, Treatment)
                VALUES (:treatmentID, :CatID, :UserID, :DateTime, :Temperature, :Treatment)
            """), {
                "treatmentID": treatmentid,
                "CatID": selected_cat_id,
                "UserID" : userid,
                "DateTime": cat_time,
                "Temperature": temperature,
                "Treatment": treatment_details              
            })
        st.rerun()
    
    st.session_state.show_add_treatment_dialog = False
    st.caption('_:orange[Press Esc to Cancel]_')

# Check if the session state variable exists
if "show_add_treatment_dialog" not in st.session_state:
    st.session_state.show_add_treatment_dialog = False

# Table for treatments
with engine.begin() as conn:
    treatment_table_df = pd.read_sql_query(sa.text("""
    SELECT 
        Cats.CatID, 
        Cats.CatName AS Name, 
        Cats.CageID AS CageNo, 
        Treatment.Temperature AS Temperature, 
        Treatment.Treatment AS Treatment, 
        CONVERT(VARCHAR, Treatment.DateTime, 108) AS Time, 
        Users.UserName AS GivenBy
    FROM 
        Cats
    INNER JOIN 
        Treatment ON Treatment.CatID = Cats.CatID
    INNER JOIN 
        Users ON Treatment.UserID = Users.UserID
    """), conn)

    
# Filtering and Final Table
# st.write("Filters")
# dynamic_filters = DynamicFilters(treatment_table_df, filters=['CatID'])
# dynamic_filters.display_filters(location = 'columns', num_columns=1, gap='large')
# treatment_table_df_final = dynamic_filters.filter_df()

col1, col2, col3, col4, col5, col6 = st.columns(6)
    
# Add a New Donation Button
st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)
new_treatment = col6.button("Add Treatment", on_click = add_treatment_dialog)

if st.session_state.show_add_treatment_dialog:
    add_treatment()

# Display the Table
donation_table = st.dataframe(treatment_table_df, width=1500, height=600, hide_index = True, on_select = "rerun", selection_mode = "single-row") 

# Update and Delete Buttons Remaining. (check Finance.py for reference)