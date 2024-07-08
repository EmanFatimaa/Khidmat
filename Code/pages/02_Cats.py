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

server = 'DESKTOP-HT3NB74' # EMAN
# server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA # Note the double backslashes

# server = 'DESKTOP-HT3NB74' # EMAN
server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA # Note the double backslashes

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
    #To ensure only one dialog opens at a time
    st.session_state.show_add_cat_dialog = True
    # st.session_state.edit_cat_dialog = False

# ADD DIALOGE EMAN:)
@st.experimental_dialog("Add a New Cat")

def add_cat():

    #cats info (in the form)
    st.write("Cat related details")

    # Creating columns for better formatting 
    col1, col2= st.columns(2)

    with col1:
        
        #Cat ID Field
        with engine.begin()as conn:
            currentCatID = int(pd.read_sql_query(sa.text("select top 1 catID from Cats order by catID desc"), conn).iat[0,0]) + 1
            #TODO:
            CatCodestr = "PA-0000" + str(currentCatID) #need to fix this logic , explore prettify
        catID = st.text_input("Cat ID", value = CatCodestr, disabled= True)
        
        # Age field
        age = st.number_input("Age (in years)", step=0.1, value=0.0)

        # Type field
        with engine.begin() as conn:
            typeSelection = pd.read_sql_query(sa.text("Select type from Type"), conn)
        type = st.selectbox("Type", typeSelection["type"].tolist())

       
    with col2:

        # Name field
        name = st.text_input("Cat Name", placeholder= "Enter Cat's Name")

        # Gender field
        with engine.begin() as conn:
            genderSelection = pd.read_sql_query(sa.text("Select gender from Gender"), conn)
        gender = st.selectbox("Gender", genderSelection["gender"].tolist())

        # Cage no field
        with engine.begin() as conn:
            cageID = pd.read_sql_query(sa.text("SELECT cageID FROM cage WHERE cageID NOT IN (SELECT cageID FROM cats)"), conn) # OR: select cageID from cage where cageStatus = 'Free'
        cageNum = st.selectbox("Cage Number", cageID["cageID"].tolist()) # This should also show whcih Ward it is in and that Cage is free or not ofc.

    with engine.begin() as conn:
        statusSelection = pd.read_sql_query(sa.text("Select statusType from CatStatus"), conn)
    status = st.selectbox("Status", statusSelection["statusType"].tolist())	
    
    #owner related infro (int the form)
    st.write("Owner related details")
  
    col1, col2= st.columns(2) #redefining to enter owner related details after cats details
    
    with col1:
        # Owner name text input
        ownerName = st.text_input("Owner's Name", placeholder="Enter Owner's Name")

    with col2:
        with engine.begin() as conn:
            fetchall = conn.execute(sa.text("Select contactNum from Externals where name = :name"), {"name": ownerName}).fetchall()
            contactFromDB = ''
            for row in fetchall:
                contactFromDB = row[0]
        # Owner contact text input
        ownerContact = st.text_input("Owner's Contact", value = contactFromDB, placeholder="0300-7413639")

    #date
    date = st.date_input('Date', value=datetime.date.today(), disabled= True)

    # address text area
    address = st.text_area("Address", placeholder="Enter Address")
    
    # Submit and Cancel buttons
    submitted = st.button("Add Pet")
    st.caption(':orange[*Press Esc to Cancel*]') #st.write("Note: Upon clicking Cancel, the form will be closed")

    #Logic for inserting the data
    if submitted:

        # Checks
        everythingFilled = False
        #valid name, contact number, address?

        # Check if any of the fields are left unfilled
        if not (age and type and name and gender and cageNum and status and ownerName and  ownerContact and address ):
            st.error("Please fill in all fields before submitting.")
            print("Sab fields barho bete")
        else:
            everythingFilled = True

        if everythingFilled:
            with engine.begin() as conn:
                conn.execute(sa.text(""" 
                if not exists(select externalID from Externals where name = :name)
                    begin
                        insert into Externals
                        values
                        ((select top 1 externalID from Externals  order by externalID desc) + 1,
                        :name, :contactNum, :address)
                    end

                    insert into Cats
                    values 
                    (:catID, :catName, :age , 
                    (select genderID from gender where gender = :gender),
                    (select typeID from type where type = :type), :cageID , 
                    (select externalID from Externals where name = :name) , 
                    (select statusID from CatStatus where statusType = :status), 
                    :admittedOn)
                    """),

                    {"name": ownerName, "name": ownerName, "contactNum": ownerContact, "address": address, "catID": catID, "catName": name,
                    "age": age, "gender": gender, "type" : type, "cageID":cageID, "name": ownerName, "status": status, "admittedOn" : date })
                
            print("wohoo")
            st.rerun()
    st.session_state.show_add_cat_dialog = False

# Check if the session state exists or not
if 'show_add_cat_dialog' not in st.session_state:
    st.session_state.show_add_cat_dialog = False


#Add a new cat button
with col3:    
    addCat = st.button("⊹ Add a New Cat")#, on_click= add_cat_dialog -- doesnt work dky..

if addCat:
    add_cat_dialog()

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

# @st.experimental_dialog("Edit Cat Details")
# def edit_cat():

#     # Creating columns for better formatting -- dk if better way of doing 
#     col1, col2= st.columns(2)
    
#     with col1:
#         # Name field
#         name = st.text_input("Cat Name", placeholder= "Enter Cat's Name")

#     with col2:
#         # Age field
#         age = st.number_input("Age (in years)", step=0.5, value=1.0)

#     with col1:
#         # Gender field
#         gender = st.selectbox("Gender", ["Female", "Male"])

#     with col2:
#         # Type field
#         type = st.selectbox("Type", ["Pet", "Rescued"])

#     with col1:
#         # Cage no field
#         cageNum = st.text_input("Cage Number", placeholder="Please select a cage number")

#     with col2:
#         # Status dropdown with new options
#         status = st.selectbox("Status", [
#             "Adopted",
#             "Discharged",
#             "Expired",
#             "Fostered",
#             "Healthy In Lower Portion",
#             "Missing",
#             "Moved To Healthy Area",
#             "Ready To Be Moved To Healthy Area",
#             "Ready To Discharge",
#             "Under Observation",
#             "Under Treatment"
#         ])

#     with col1:
#         # Owner name text input
#         ownerName = st.text_input("Owner's Name", placeholder="Enter Owner's Name")

#     with col2:
#         # Owner contact text input
#         ownerContact = st.text_input("Owner's Contact", placeholder="xxxx-xxxxxxx")

#     # with col1:
#     # Date input
#     date = st.date_input('Date', value=datetime.date.today())

#     # with col2:
#     # address text area
#     address = st.text_area("Address", placeholder="Enter Address")

# # Submit and Cancel buttons
#     submitted = st.button("Save Changes")
#     st.caption(':orange[*Press Esc to Cancel*]')

#     if submitted:
#         # Check if any of the fields are left unfilled
#         if not (name and age and gender and type and cageNum and status and ownerName and ownerContact and address and date):
#             st.error("Please fill in all fields before submitting.")
#         else:
#             # Add logic to process form data here
#             st.success(f"Pet {name} details edited successfully!")

# Edit and Delete Remains
# Filtering Remains
# Lastly, Aesthestics ofc
# Checks remain for each field as well (Refer to Treatments.py or Finances.py)
# Error of when inserting a new queryy
# Wards and Cage should update by their own
# Code for upfating cage id for managing when cages get free/occupied