import streamlit as st
import pandas as pd
import datetime
from PIL import Image
from st_pages import Page, show_pages, add_page_title, hide_pages

st.set_page_config(page_title="Cats", page_icon="🐈", layout="centered", initial_sidebar_state="expanded")

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

logo = Image.open("assets/logo.png")
st.logo(logo)

#Creating columns for better formatting
col1, col2, col3, col4 = st.columns(4)

#Title
with col1:
    st.write("## Cats")

# ADD DIALOGE EMAN:)
@st.experimental_dialog("Add a New Cat")
def open_dialog():

    # Creating columns for better formatting -- dk if better way of doing 
    col1, col2= st.columns(2)

    with col1:
        # Name field
        name = st.text_input("Cat Name", placeholder= "Enter Cat's Name")

    with col2:
        # Age field
        age = st.number_input("Age (in years)", step=0.5, value=1.0)

    with col1:
        # Gender field
        gender = st.selectbox("Gender", ["Female", "Male"])

    with col2:
        # Type field
        type = st.selectbox("Type", ["Pet", "Rescued"])

    with col1:
        # Cage no field
        cageNum = st.text_input("Cage Number", placeholder="Please select a cage number")

    with col2:
        # Status dropdown with new options
        status = st.selectbox("Status", [
            "Adopted",
            "Discharged",
            "Expired",
            "Fostered",
            "Healthy In Lower Portion",
            "Missing",
            "Moved To Healthy Area",
            "Ready To Be Moved To Healthy Area",
            "Ready To Discharge",
            "Under Observation",
            "Under Treatment"
        ])

    with col1:
        # Owner name text input
        ownerName = st.text_input("Owner's Name", placeholder="Enter Owner's Name")

    with col2:
        # Owner contact text input
        ownerContact = st.text_input("Owner's Contact", placeholder="xxxx-xxxxxxx")

    # with col1:
    # Date input
    date = st.date_input('Date', value=datetime.date.today())

    # with col2:
    # address text area
    address = st.text_area("Address", placeholder="Enter Address")

    # Submit and Cancel buttons
    submitted = st.button("Add Pet")
    
    # cancelled = st.form_submit_button("Cancel")
    st.caption(':orange[*Press Esc to Cancel*]') #st.write("Note: Upon clicking Cancel, the form will be closed")

    if submitted:
        # Check if any of the fields are left unfilled
        if not (name and age and gender and type and cageNum and status and ownerName and ownerContact and address and date):
            st.error("Please fill in all fields before submitting.")
        else:
            # Add logic to process form data here
            st.success(f"Pet {name} added successfully!")
            st.balloons()
                
#Add a new cat button
with col3:    
    addCat = st.button("⊹ Add a New Cat")#, on_click= open_dialog -- doesnt work dky..

if addCat:
    open_dialog()

#Add a new ward button
with col4:    
    addWard = st.button("Go To Wards")#, on_click= open_dialog -- doesnt work dky..
    
if addWard:
    st.switch_page("pages/04_Wards.py") # -- dk if this is the right way to do this

#With form or only form = , st. inputs or form. inputs?

@st.experimental_dialog("Edit Cat Details")
def open_dialogEdit():

    # Creating columns for better formatting -- dk if better way of doing 
    col1, col2= st.columns(2)
    
    with col1:
        # Name field
        name = st.text_input("Cat Name", placeholder= "Enter Cat's Name")

    with col2:
        # Age field
        age = st.number_input("Age (in years)", step=0.5, value=1.0)

    with col1:
        # Gender field
        gender = st.selectbox("Gender", ["Female", "Male"])

    with col2:
        # Type field
        type = st.selectbox("Type", ["Pet", "Rescued"])

    with col1:
        # Cage no field
        cageNum = st.text_input("Cage Number", placeholder="Please select a cage number")

    with col2:
        # Status dropdown with new options
        status = st.selectbox("Status", [
            "Adopted",
            "Discharged",
            "Expired",
            "Fostered",
            "Healthy In Lower Portion",
            "Missing",
            "Moved To Healthy Area",
            "Ready To Be Moved To Healthy Area",
            "Ready To Discharge",
            "Under Observation",
            "Under Treatment"
        ])

    with col1:
        # Owner name text input
        ownerName = st.text_input("Owner's Name", placeholder="Enter Owner's Name")

    with col2:
        # Owner contact text input
        ownerContact = st.text_input("Owner's Contact", placeholder="xxxx-xxxxxxx")

    # with col1:
    # Date input
    date = st.date_input('Date', value=datetime.date.today())

    # with col2:
    # address text area
    address = st.text_area("Address", placeholder="Enter Address")

# Submit and Cancel buttons
    submitted = st.button("Save Changes")
    st.caption(':orange[*Press Esc to Cancel*]')

    if submitted:
        # Check if any of the fields are left unfilled
        if not (name and age and gender and type and cageNum and status and ownerName and ownerContact and address and date):
            st.error("Please fill in all fields before submitting.")
        else:
            # Add logic to process form data here
            st.success(f"Pet {name} details edited successfully!")

# Specify the path to your CSV file
csv_file_path = 'assets/Cats.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Display the DataFrame with adjustable width and height
st.dataframe(df, width= 1500, height= 150, hide_index= True, on_select= open_dialogEdit)