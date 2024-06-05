import streamlit as st
import pandas as pd
import sqlalchemy as sa

from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from st_pages import Page, show_pages, add_page_title, hide_pages
from PIL import Image

st.set_page_config(page_title="Table From Database", page_icon=":books:", layout="wide", initial_sidebar_state="expanded")

logo = Image.open("assets/logo.png")
st.logo(logo)

hide_pages(["Login", "Teams"])

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

server = 'DESKTOP-B3MBPDD\\FONTAINE'  # Note the double backslashes
database = 'Northwind'

connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

engine = create_engine(connection_url)

# everything indented is communicating with the database ; closes automatically
with engine.begin() as conn:
    employee_table = pd.read_sql_query(sa.text("select * from Employees"), conn)

selected_info = st.dataframe(employee_table, on_select = "rerun", selection_mode = "single-row", hide_index = True)

# If a row is selected
if len(selected_info["selection"]["rows"]) == 1:

    selected_row = selected_info["selection"]["rows"][0] + 1 # start surrogate key from 1 please
    st.write(f"Selected row: {selected_row}")

    if selected_row != 2:

        with engine.begin() as conn:
            row_information = pd.read_sql_query(sa.text(f"select * from Employees where EmployeeID = {selected_row}"), conn)

        first_name = row_information["FirstName"][0]
        last_name = row_information["LastName"][0]
        reports_to = row_information["ReportsTo"][0]

        with engine.begin() as conn:
            reports_to_name = pd.read_sql_query(sa.text(f"select FirstName, LastName from Employees where EmployeeID = {int(reports_to)}"), conn)
        
        reports_to_first_name = reports_to_name["FirstName"][0]
        reports_to_last_name = reports_to_name["LastName"][0]

        st.text_input("First Name", value = first_name, key = "first_name")
        st.text_input("Last Name", value = last_name, key = "last_name")
        st.text_input("Reports To", value = reports_to_first_name + " " + reports_to_last_name, key = "reports_to")

        # Using object notation
        add_selectbox = st.sidebar.selectbox(
            "How would you like to be contacted?",
            ("Email", "Home phone", "Mobile phone")
        )