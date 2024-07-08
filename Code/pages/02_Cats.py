# standard imports
import datetime
from PIL import Image

# third party imports
import pandas as pd
import streamlit as st
import sqlalchemy as sa

#cusotm imports
from millify import prettify
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

#custome streamlit imports
from st_pages import Page, show_pages, add_page_title, hide_pages

# database information ; will change when db hosting

# server = 'DESKTOP-67BT6TD\\FONTAINE' # IBAD

# server = 'DESKTOP-HT3NB74' # EMAN
server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA # Note the double backslashes

# server = 'DESKTOP-HT3NB74' # EMAN
# server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA # Note the double backslashes

database = 'PawRescue' # EMAN 'Khidmat'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

st.set_page_config(page_title="Cats", page_icon="🐈", layout="wide", initial_sidebar_state="expanded")

# Logo
logo = Image.open("assets/logo.png")
st.logo(logo)

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

if st.sidebar.button("🔓 Logout"):
    st.switch_page("LoginScreen.py")

hide_pages(["Login"])

#Creating columns for better formatting
col1, col2, col3, col4 = st.columns(4)

#Title
with col1:
    st.header("Cats")

def add_cat_dialog():
    st.session_state.show_add_cat_dialog = True
    # st.session_state.edit_cat_dialog = False

# ADD DIALOGE EMAN:)
@st.experimental_dialog("Add a New Cat")
def add_cat():
    #cats info (in the form)
    st.write("Cat related details")
        # Creating columns for better formatting 
    col1, col2 = st.columns(2)

    with col1:
        # Cat ID Field
        with engine.begin() as conn:
            result = pd.read_sql_query(sa.text("SELECT TOP 1 catID FROM Cats ORDER BY catID DESC"), conn)
        if not result.empty:
            currentCatID = int(result.iat[0, 0]) + 1
        else:
            currentCatID = 1  # or some other default value
        catID = st.text_input("Cat ID", value=str(currentCatID), disabled=True)

        # Age field
        age = st.number_input("Age (in years)", step=0.1, value=0.0)

        # Type field
        with engine.begin() as conn:
            typeSelection = pd.read_sql_query(sa.text("SELECT type FROM Type"), conn)
        type = st.selectbox("Type", typeSelection["type"].tolist())

    with col2:
        # Name field
        name = st.text_input("Cat Name", placeholder="Enter Cat's Name")

        # Gender field
        with engine.begin() as conn:
            genderSelection = pd.read_sql_query(sa.text("SELECT gender FROM Gender"), conn)
        gender = st.selectbox("Gender", genderSelection["gender"].tolist())

        # Cage no field
        with engine.begin() as conn:
            cageID = pd.read_sql_query(sa.text("SELECT cageID FROM Cage WHERE cageID NOT IN (SELECT cageID FROM Cats)"), conn)  # OR: select cageID from Cage where cageStatus = 'Free'
        cageNum = st.selectbox("Cage Number", cageID["cageID"].tolist())  # This should also show which Ward it is in and that Cage is free or not ofc.

    with engine.begin() as conn:
        statusSelection = pd.read_sql_query(sa.text("SELECT statusType FROM CatStatus"), conn)
    status = st.selectbox("Status", statusSelection["statusType"].tolist())

    # Owner related info (in the form)
    st.write("Owner related details")

    col1, col2 = st.columns(2)  # redefining to enter owner related details after cat details

    with col1:
        # Owner name text input
        ownerName = st.text_input("Owner's Name", placeholder="Enter Owner's Name")

    with col2:
        contactFromDB = ''
        if ownerName:
            with engine.begin() as conn:
                fetchall = conn.execute(sa.text("SELECT contactNum FROM Externals WHERE name = :name"), {"name": ownerName}).fetchall()
                if fetchall:
                    contactFromDB = fetchall[0][0]

        # Owner contact text input
        ownerContact = st.text_input("Owner's Contact", value=contactFromDB, placeholder="0300-7413639")

    # Date
    date = st.date_input('Date', value=datetime.date.today(), disabled=True)

    # Address text area
    address = st.text_area("Address", placeholder="Enter Address")

    # Submit and Cancel buttons
    st.caption(':orange[Press Esc to Cancel]')

    # Logic for inserting the data
    if st.button("Add cat"):
        # Checks
        everythingFilled = False

        # Check if any of the fields are left unfilled
        if not (age and type and name and gender and cageNum and status and ownerName and ownerContact and address):
            st.error("Please fill in all fields before submitting.")
            print("Please fill in all fields.")
        else:
            everythingFilled = True

        if everythingFilled:
            with engine.begin() as conn:
                conn.execute(sa.text(""" 
                IF NOT EXISTS (SELECT externalID FROM Externals WHERE name = :name)
                BEGIN
                    INSERT INTO Externals
                    VALUES
                    ((SELECT COALESCE(MAX(externalID), 0) + 1 FROM Externals), :name, :contactNum, :address)
                END

                INSERT INTO Cats (catID, catName, age, genderID, typeID, cageID, externalID, statusID, admittedOn)
                VALUES
                (:catID, :catName, :age, 
                (SELECT genderID FROM Gender WHERE gender = :gender),
                (SELECT typeID FROM Type WHERE type = :type), 
                :cageID, 
                (SELECT externalID FROM Externals WHERE name = :name), 
                (SELECT statusID FROM CatStatus WHERE statusType = :status), 
                :admittedOn)"""),
                {
                    "catID": currentCatID, "catName": name, "age": age, "gender": gender, 
                    "type": type, "cageID": cageNum, "name": ownerName, 
                    "contactNum": ownerContact, "address": address, 
                    "status": status, "admittedOn": date
                })

            st.rerun()
        st.session_state.show_add_cat_dialog = False


# Check if the session state exists or not
if 'show_add_cat_dialog' not in st.session_state:
    st.session_state.show_add_cat_dialog = False

col1, col2, col3, col4, col5, col6 = st.columns(6)

#Add a new cat button
st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)
new_treatment = col6.button("⊹ Add New Cat", on_click = add_cat_dialog)

if st.session_state.show_add_cat_dialog:
    add_cat()

#Add a new ward button
with col4:    
    addWard = st.button("Go To Wards")#, on_click= add_cat_dialog -- doesnt work dky..
    
if addWard:
    st.switch_page("pages/04_Wards.py") # -- dk if this is the right way to do this

#With form or only form = , st. inputs or form. inputs?

# ------------------------------------------------------------
#Table for Cats:
with engine.begin() as conn:
    cat_table_df = pd.read_sql_query(sa.text(""" 
                        select catID as 'Cat ID', catName as 'Cat Name', Externals.name as 'Owner/Reporter', admittedOn as 'Admitted On',
                                Type.type as 'Type', Cage.cageID as 'Cage', CatStatus.statusType as 'Status'

                        from Cats, Externals, Type, Cage, CatStatus 
                        where Cats.externalID = Externals.externalID and 
                        Type.typeID = Cats.typeID and 
                        Cage.cageID = Cats.cageID and
                        Cats.statusID = CatStatus.StatusID"""), conn)
    
cat_table = st.dataframe(cat_table_df, width = 1500, height = 600, hide_index= True , on_select = "rerun", selection_mode= "single-row")

#-------------------------------------------------------------------

