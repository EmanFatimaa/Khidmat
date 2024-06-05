import streamlit as st
import pandas as pd

st.write("## Displaying all of the Ward related forms here:")
st.write("### 1. Adding a new Ward")

#LOGO GOES HERE -- sidebar..
from PIL import Image
img= Image.open("logo.png")
st.logo(img )


#######################
##ADD
# Create a form
form = st.form("Add Ward")

# Ward name text input
ward_name = form.text_input("Ward Name", placeholder= "IC - 05") #ward = st.text_input("Ward Name", placeholder="Enter Ward Name")

# Ward type dropdown
ward_type = form.selectbox("Ward Type", [
    "General Ward",
    "ICU Ward",
    "Lounge",
    "Qurantine",
    "Viral Room",
])

# Capacity text input
capacity = form.number_input("Capacity", step= 1 , value= 5)

# Available beds text input
available_beds = form.number_input("Available Beds", step = 1, value= 10)

# Remarks text area
remarks = form.text_area("Remarks", placeholder= "Construction under process")

# Flag to track message box visibility
show_message_box = st.empty()  # Initially empty element

# Submit button

# Arrange buttons horizontally
col1, col2, col3, col4, col5, col6, col7 = form.columns(7)
with col6:
    submitted = col6.form_submit_button("Add Ward")
with col7:
    cancelled = col7.form_submit_button("Cancel")
    
if submitted:
    if not ( ward_name and ward_type and capacity and available_beds and remarks):
        show_message_box.error("Please fill in all fields before submitting.")
    else:
        # Add logic to process form data here
        st.success(f"Ward '{ward_name}' added successfully!")
        # You can potentially use the data to update a database or perform other actions
        st.write(f"Ward Name: {ward_name}")
        st.write(f"Ward Type: {ward_type}")
        st.write(f"Capacity: {capacity}")
        st.write(f"Available Beds: {available_beds}")
        st.write(f"Remarks: {remarks}")

elif cancelled:
    # Handle cancel button click (optional)
    st.warning("Form submission cancelled.")

#######################
##UPDATE

st.write("### 2. Updating the details of the Ward")
# Create a form
form = st.form("Update Ward")

# Ward name text input
ward_name = form.text_input("Ward Name", placeholder= "IC - 05") #ward = st.text_input("Ward Name", placeholder="Enter Ward Name")

# Ward type dropdown
ward_type = form.selectbox("Ward Type", [
    "General Ward",
    "ICU Ward",
    "Lounge",
    "Qurantine",
    "Viral Room",
])

# Capacity text input
capacity = form.number_input("Capacity", step= 1 , value= 5)

# Available beds text input
available_beds = form.number_input("Available Beds", step = 1, value= 10)

# Remarks text area
remarks = form.text_area("Remarks", placeholder= "Construction under process")

# Flag to track message box visibility
show_message_box = st.empty()  # Initially empty element

# Submit button

# Arrange buttons horizontally
col1, col2, col3, col4, col5, col6, col7 = form.columns(7)
with col6:
    submitted = col6.form_submit_button("Update Ward")
with col7:
    cancelled = col7.form_submit_button("Cancel")
    
if submitted:
    if not ( ward_name and ward_type and capacity and available_beds and remarks):
        show_message_box.error("Please fill in all fields before submitting.")
    else:
        # Add logic to process form data here
        st.success(f"Ward '{ward_name}' added successfully!")
        # You can potentially use the data to update a database or perform other actions
        st.write(f"Ward Name: {ward_name}")
        st.write(f"Ward Type: {ward_type}")
        st.write(f"Capacity: {capacity}")
        st.write(f"Available Beds: {available_beds}")
        st.write(f"Remarks: {remarks}")

elif cancelled:
    # Handle cancel button click (optional)
    st.warning("Form submission cancelled.")

#######################
##DELETE

st.write("### 3. Deleting a Ward")
# Create a form
form = st.form("Delete Ward")

# Ward name text input
ward_name = form.text_input("Ward Name", placeholder= "IC - 05") #ward = st.text_input("Ward Name", placeholder="Enter Ward Name")

# Ward type dropdown
ward_type = form.selectbox("Ward Type", [
    "General Ward",
    "ICU Ward",
    "Lounge",
    "Qurantine",
    "Viral Room",
])

# Capacity text input
capacity = form.number_input("Capacity", step= 1 , value= 5)

# Available beds text input
available_beds = form.number_input("Available Beds", step = 1, value= 10)

# Remarks text area
remarks = form.text_area("Remarks", placeholder= "Construction under process")

# Flag to track message box visibility
show_message_box = st.empty()  # Initially empty element

# Submit button

# Arrange buttons horizontally
col1, col2, col3, col4, col5, col6, col7 = form.columns(7)
with col6:
    submitted = col6.form_submit_button("Delete Ward")
with col7:
    cancelled = col7.form_submit_button("Cancel")
    
if submitted:
    if not ( ward_name and ward_type and capacity and available_beds and remarks):
        show_message_box.error("Please fill in all fields before submitting.")
    else:
        # Add logic to process form data here
        st.success(f"Ward '{ward_name}' added successfully!")
        # You can potentially use the data to update a database or perform other actions
        st.write(f"Ward Name: {ward_name}")
        st.write(f"Ward Type: {ward_type}")
        st.write(f"Capacity: {capacity}")
        st.write(f"Available Beds: {available_beds}")
        st.write(f"Remarks: {remarks}")

elif cancelled:
    # Handle cancel button click (optional)
    st.warning("Form submission cancelled.")
##################
