import streamlit as st
import pandas as pd
import datetime

#LOGO GOES HERE -- sidebar..
from PIL import Image
img= Image.open("logo.png")
st.logo(img )

# Button Styling
st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)
###################
# ##DATA FRAME 

# # Define the relevant columns
# relevantColumns = ['Cat ID', 'Cat Name', 'Owner', "Owner's Contact", 'Date', 'Type', 'Cage Number', 'Status']

# # Initialize an empty DataFrame with the relevant columns
# df = pd.DataFrame(columns=relevantColumns)

# # Define type and status options
# type = ['Pet', 'Rescued']
# status = ["Adopted", 
#     "Discharged",
#     "Expired",
#     "Fostered",
#     "Healthy In Lower Portion",
#     "Missing",
#     "Moved To Healthy Area",
#     "Ready To Be Moved To Healthy Area",
#     "Ready To Discharge",
#     "Under Observation",
#     "Under Treatment"
# ]

# # gender = ['Male', 'Female']
# currDate = datetime.datetime.today()
# config = {
#     'Cat ID' : st.column_config.TextColumn('Cat ID', required=True),
#     'Cat Name' : st.column_config.TextColumn('Cat Name', required=True),
#     'Owner Name' : st.column_config.TextColumn('Owner Name', width='large', required=True),
#     "Owner's Contact" : st.column_config.TextColumn("Owner's Contact", required=True),
#     'Date': st.column_config.DateColumn('Date', required=True), 
#     'Type' : st.column_config.SelectboxColumn('Type', options = type, required= True),
#     'Cage Number' : st.column_config.TextColumn('Cage Number', required= True),
#     'Status' : st.column_config.SelectboxColumn('Status', options =  status, required= True),
#     #'Date': st.date_input('Date', value = currDate, key='date')  # Date input with default value as current date
# }

# result = st.data_editor(df, column_config = config, num_rows='dynamic')

# if st.button('Get results'):
#     st.write(result)

###############

# ##ADD form
# st.write("### 1. Add  a New Cat")
# # Create a form
# form = st.form("Add Pet")

# # Name field
# name = form.text_input("Cat Name", placeholder= "Enter Cat's Name")

# # Age field
# age = form.number_input("Age (in years)" , step = 0.5 , value= 1.0)

# # Gender field
# gender = form.selectbox("Gender",[
#     "Female",
#     "Male"])

# # Type field
# type = form.selectbox("Type", [
#     "Pet",
#     "Rescued"])

# # Cage no field
# cageNum = form.text_input("Cage Number", placeholder= "Please select an cage number")

# # Status dropdown with new options
# status = form.selectbox("Status", [
#     "Adopted", 
#     "Discharged",
#     "Expired",
#     "Fostered",
#     "Healthy In Lower Portion",
#     "Missing",
#     "Moved To Healthy Area",
#     "Ready To Be Moved To Healthy Area",
#     "Ready To Discharge",
#     "Under Observation",
#     "Under Treatment"
# ]) ###HOW TO PREVENT THE USER FROM EDITING THE OPTIONS -- not needed ig..

# # Owner name text input
# ownerName = form.text_input("Owner's Name", placeholder= "Enter Owner's Name")

# # Owner contact text input 
# ownerContact = form.text_input("Owner's Contact", placeholder="xxxx-xxxxxxx") #format="%d-%d%d%d%d%d%d%d%d%d"

# # Date input
# date = form.date_input('Date', value=datetime.date.today()) #form.date_input("Select a date")

# # Remarks text area
# address = form.text_area("Address", placeholder= "Enter Address")

# # Arrange buttons horizontally & to shift to the right side -- hardcoded I guess, need to figure out some way to make sure hardcoding is not needed. This was one of the ways to do this
# col1, col2, col3, col4, col5, col6, col7 = form.columns(7)
# with col6:
#     submitted = col6.form_submit_button("Add Pet")
# with col7:
#     cancelled = col7.form_submit_button("Cancel")

# # Flag to track message box visibility
# show_message_box = st.empty()  # Initially empty element

# if submitted:
#     # Check if any of the fields are left unfilled
#     if not ( name and age and gender and type and cageNum and status and ownerName and ownerContact and address and date):
#         show_message_box.error("Please fill in all fields before submitting.")
#     # else:
#     #     # Add logic to process form data here 
#     #     st.success(f"Pet {name} added successfully!")
#     #     # You can potentially use the data to update a database or perform other actions
#     #     st.write(f"Name: {name}")
#     #     st.write(f"Status: {status}")
#     #     st.write(f"Cage Number: {cage_num}")
#     #     st.write(f"Remarks: {remarks}")
#     #     st.write(f"Owner Name: {owner_name}")
#     #     st.write(f"Owner Contact: {owner_contact}")

# elif cancelled:
#     # Handle cancel button click (optional)
#     st.warning("Form submission cancelled.")


#########################
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

    # Create a form -- is it needed
    # with st.form("Add Pet"): #, clear_on_submit= True

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

    # if cancelled:
    #     # Close the form
    #     st.rerun()

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
    addWard = st.button("⊹ Add a New Ward")#, on_click= open_dialog -- doesnt work dky..
    
if addWard:
    open_dialog()
#With form or only form = , st. inputs or form. inputs?

###############################
##UPDATE:

@st.experimental_dialog("Edit Cat Details")
def open_dialogEdit():

    # Create a form
    # with st.form("Edit Pet"): #, clear_on_submit= True

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

        
####################
#DATAFRAME

# Specify the path to your CSV file
csv_file_path = 'Cats.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Display the DataFrame with adjustable width and height
st.dataframe(df, width= 1500, height= 150, hide_index= True, on_select= open_dialogEdit)

