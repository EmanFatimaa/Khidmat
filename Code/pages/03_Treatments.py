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

server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA: 'DESKTOP-HPUUN98\SPARTA'   EMAN: 'DESKTOP-HT3NB74' IBAD: 'DESKTOP-B3MBPDD\\FONTAINE'# Note the double backslashes
database = 'PawRescue' # EMAN :'Khidmat'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

st.set_page_config(page_title="Treatments", page_icon="💊",initial_sidebar_state="expanded")

# logo
logo = Image.open("assets/logo.png")
st.logo(logo)

# Button Styling
st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)

st.sidebar.markdown("""
    <style>
        .sidebar-content > div:nth-child(1) > div > div {color: white}
        .sidebar-content > div:nth-child(1) > div > div > span {color: #FFA500}
    </style>
""", unsafe_allow_html=True)

if st.sidebar.button("👥 Team"):
    st.switch_page("pages/Teams.py")
            
if st.sidebar.button("🔓 Logout"):
    st.switch_page("LoginScreen.py")

hide_pages(["Login", "Teams"])

#Creating columns for better formatting
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.header("Treatment")

# current_date = date.today().strftime("%Y-%m-%d")

st.write("Filter By:")
col1, col2= st.columns([2, 17])
with col1:
    st.button("Cat ID")
with col2:
    st.button("Current Date")

@st.experimental_dialog("Add New Treatment")
def open_dialog():
    ID = st.text_input("Cat ID", placeholder= "Enter Cat's ID")

    col1, col2= st.columns(2)
    with col1:
        # Gender field
        cat_time = st.time_input("Time")
    with col2:
        temperature = st.number_input("Temperature", min_value=99, max_value=105, step=1, placeholder="100 F")

    treatment_details = st.text_area("Treatment Details", placeholder="IV given, dressing done")

    # Submit and Cancel buttons
    submitted = st.button("Add Pet")
    
    # cancelled = st.form_submit_button("Cancel")
    st.caption(':orange[*Press Esc to Cancel*]') #st.write("Note: Upon clicking Cancel, the form will be closed")

    if submitted:
        # Check if any of the fields are left unfilled
        if not (ID and cat_time and temperature and treatment_details):
            st.error("Please fill in all fields before submitting.")
        else:
            with engine.begin() as conn:
                catname = pd.read_sql_query(sa.text("""select CatName from Cats where CatID = :ID"""), {"CatID": ID})
                cageid = pd.read_sql_query(sa.text("""select CageID from Cats where CatID = :ID"""), {"CatID": ID})
                conn.execute(sa.text("""
                    insert into Treatment (CatID, CatName, CageID, temperature, treatment, DateTime)
                    values (:CatID, (select CatName from Cats where CatID = :catID) , (select cageID from Cats where CatID = :CatID), :temperature, :treatment, :dateTime)
                    """), {
                    "CatID": ID, 
                    "catName": catname,  # Assuming catName is not provided in the form
                    "cageID": cageid,  # Assuming cageID is not provided in the form
                    "temperature": temperature, 
                    "treatment": treatment_details, 
                    "dateTime": cat_time
                                    })
            st.rerun()
        st.success(f"Treatment added successfully!")
                
with col4:    
    addCat = st.button("⊹ Add Treatment", on_click=open_dialog)#, on_click= open_dialog -- doesnt work dky..

  # Table for treatments
with engine.begin() as conn:
    treatment_table = pd.read_sql_query(sa.text("""
    select Cats.catID, catName as Name, cageID as CageNo, temperature as Temperature, treatment as Treatment, CONVERT(varchar, dateTime, 108) AS Time, userName as GivenBy
    from Cats
    inner join Treatment on Treatment.catID = Cats.catID
    inner join Users on treatment.userID = Users.userID"""), conn)
        
st.dataframe(treatment_table, width=1500, height=600, hide_index = True, on_select = "rerun", selection_mode = "single-row")