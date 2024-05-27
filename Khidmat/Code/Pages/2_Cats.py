import streamlit as st
import pandas as pd

st.write("## Displaying all of the Cat related forms here:")
###################
##ADD 
st.write("### 1. Adding a new Pet")
# Create a form
form = st.form("Add Pet")

# Name field
name = form.text_input("Name", placeholder= "Teen Patti")

# Status dropdown with new options
status = form.selectbox("Status", [
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
]) ###HOW TO PREVENT THE USER FROM EDITING THE OPTIONS -- not needed ig..

# Cage number text input
cage_num = form.text_input("Cage Number", placeholder= "ICU-C5")

# Remarks text area
remarks = form.text_area("Remarks", placeholder= "Moved to healthy area on 3rd April 2024")

# Owner name text input
owner_name = form.text_input("Owner Name", placeholder= "Sara Qalandari")

# Owner contact text input 
owner_contact = form.text_input("Owner Contact", placeholder="03124578321") #format="%d-%d%d%d%d%d%d%d%d%d"

# Arrange buttons horizontally & to shift to the right side -- hardcoded I guess, need to figure out some way to make sure hardcoding is not needed. This was one of the ways to do this
col1, col2, col3, col4, col5, col6, col7 = form.columns(7)
with col6:
    submitted = col6.form_submit_button("Add Pet")
with col7:
    cancelled = col7.form_submit_button("Cancel")

# Flag to track message box visibility
show_message_box = st.empty()  # Initially empty element

if submitted:
    # Check if any of the fields are left unfilled
    if not (name and status and cage_num and owner_name and owner_contact):
        show_message_box.error("Please fill in all fields before submitting.")
    else:
        # Add logic to process form data here 
        st.success(f"Pet {name} added successfully!")
        # You can potentially use the data to update a database or perform other actions
        st.write(f"Name: {name}")
        st.write(f"Status: {status}")
        st.write(f"Cage Number: {cage_num}")
        st.write(f"Remarks: {remarks}")
        st.write(f"Owner Name: {owner_name}")
        st.write(f"Owner Contact: {owner_contact}")

elif cancelled:
    # Handle cancel button click (optional)
    st.warning("Form submission cancelled.")

##################
## UPDATEE

st.write("### 2. Updating the details of a Pet")
###################
# Create a form
form = st.form("Update Pet")

# Name field
name = form.text_input("Name", placeholder= "Teen Patti")

# Status dropdown with new options
status = form.selectbox("Status", [
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
]) ###HOW TO PREVENT THE USER FROM EDITING THE OPTIONS -- not needed ig..

# Cage number text input
cage_num = form.text_input("Cage Number", placeholder= "ICU-C5")

# Remarks text area
remarks = form.text_area("Remarks", placeholder= "Moved to healthy area on 3rd April 2024")

# Owner name text input
owner_name = form.text_input("Owner Name", placeholder= "Sara Qalandari")

# Owner contact text input 
owner_contact = form.text_input("Owner Contact", placeholder="03124578321") #format="%d-%d%d%d%d%d%d%d%d%d"

# Arrange buttons horizontally & to shift to the right side -- hardcoded I guess, need to figure out some way to make sure hardcoding is not needed. This was one of the ways to do this
col1, col2, col3, col4, col5, col6, col7 = form.columns(7)
with col6:
    submitted = col6.form_submit_button("Update Pet")
with col7:
    cancelled = col7.form_submit_button("Cancel")

# Flag to track message box visibility
show_message_box = st.empty()  # Initially empty element

if submitted:
    # Check if any of the fields are left unfilled
    if not (name and status and cage_num and owner_name and owner_contact):
        show_message_box.error("Please fill in all fields before submitting.")
    else:
        # Add logic to process form data here 
        st.success(f"Pet {name} added successfully!")
        # You can potentially use the data to update a database or perform other actions
        st.write(f"Name: {name}")
        st.write(f"Status: {status}")
        st.write(f"Cage Number: {cage_num}")
        st.write(f"Remarks: {remarks}")
        st.write(f"Owner Name: {owner_name}")
        st.write(f"Owner Contact: {owner_contact}")

elif cancelled:
    # Handle cancel button click (optional)
    st.warning("Form submission cancelled.")

######################
##DELETE / REMOVE


st.write("### 3. Deleting a Pet")
###################
# Create a form
form = st.form("Delete Pet")

# Name field
name = form.text_input("Name", placeholder= "Teen Patti")

# Status dropdown with new options
status = form.selectbox("Status", [
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
]) ###HOW TO PREVENT THE USER FROM EDITING THE OPTIONS -- not needed ig..

# Cage number text input
cage_num = form.text_input("Cage Number", placeholder= "ICU-C5")

# Remarks text area
remarks = form.text_area("Remarks", placeholder= "Moved to healthy area on 3rd April 2024")

# Owner name text input
owner_name = form.text_input("Owner Name", placeholder= "Sara Qalandari")

# Owner contact text input 
owner_contact = form.text_input("Owner Contact", placeholder="03124578321") #format="%d-%d%d%d%d%d%d%d%d%d"

# Arrange buttons horizontally & to shift to the right side -- hardcoded I guess, need to figure out some way to make sure hardcoding is not needed. This was one of the ways to do this
col1, col2, col3, col4, col5, col6, col7 = form.columns(7)
with col6:
    submitted = col6.form_submit_button("Delete Pet")
with col7:
    cancelled = col7.form_submit_button("Cancel")

# Flag to track message box visibility
show_message_box = st.empty()  # Initially empty element

if submitted:
    # Check if any of the fields are left unfilled
    if not (name and status and cage_num and owner_name and owner_contact):
        show_message_box.error("Please fill in all fields before submitting.")
    else:
        # Add logic to process form data here 
        st.success(f"Pet {name} added successfully!")
        # You can potentially use the data to update a database or perform other actions
        st.write(f"Name: {name}")
        st.write(f"Status: {status}")
        st.write(f"Cage Number: {cage_num}")
        st.write(f"Remarks: {remarks}")
        st.write(f"Owner Name: {owner_name}")
        st.write(f"Owner Contact: {owner_contact}")

elif cancelled:
    # Handle cancel button click (optional)
    st.warning("Form submission cancelled.")

########################################################

