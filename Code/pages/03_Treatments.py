import streamlit as st
import pandas as pd
from datetime import time 
from datetime import date
from st_pages import Page, show_pages, add_page_title, hide_pages
from PIL import Image
import sqlalchemy as sa
from millify import prettify
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

# server = 'DESKTOP-67BT6TD\\FONTAINE' # IBAD
server = 'DESKTOP-HT3NB74' # EMAN
# server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA # Note the double backslashes
database = 'PawRescue'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

st.set_page_config(page_title="Treatments", page_icon="💊", initial_sidebar_state="expanded")

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

with st.form("Add Treatment"):
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

    treatment_details = st.text_area("Treatment Details", placeholder="IV given, dressing done")

    if st.form_submit_button("Add Treatment"):
        # Check if any of the fields are left unfilled
        if not (selected_cat_id and cat_time and temperature and treatment_details):
            st.error("Please fill in all fields before submitting.")
        else:
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
            st.success(f"Treatment added successfully!")
            st.experimental_rerun()

# Table for treatments
with engine.begin() as conn:
    treatment_table = pd.read_sql_query(sa.text("""
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


st.dataframe(treatment_table, width=1500, height=600, hide_index=True, on_select="rerun", selection_mode="single-row")