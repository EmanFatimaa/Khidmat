import streamlit as st
import pandas as pd

st.write("## Displaying all of the Donation related forms here:")
###################
##ADD 
st.write("### 1. Adding the record of the donation received")
# Create a form
form = st.form("Donation Received")

# Donor Name field
donorName = form.text_input("Donor Name", placeholder= "Shamsur Rehman")

# Amount input
amount = form.number_input("Amount", step= 100, value= 500)

# Mode of payment
modeOfPayment = form.text_area("Mode Of Payment", placeholder= "Online Payment")

# Date input
date = form.date_input("Select a date")

# Arrange buttons horizontally & to shift to the right side -- hardcoded I guess, need to figure out some way to make sure hardcoding is not needed. This was one of the ways to do this
col1, col2, col3, col4, col5, col6, col7 = form.columns(7)
with col6:
    submitted = col6.form_submit_button("Add Donation")
with col7:
    cancelled = col7.form_submit_button("Cancel")

# cols = form.columns(7)
# with cols[-2]:
#     submitted = cols[-2].form_submit_button("Add Donation")
# with cols[-1]:
#     cancelled = cols[-1].form_submit_button("Cancel")

# Flag to track message box visibility
show_message_box = st.empty()  # Initially empty element

if submitted:
    # Check if any of the fields are left unfilled
    if not (donorName and amount and date and modeOfPayment):
        show_message_box.error("Please fill in all fields before submitting.")
    else:
        # Add logic to process form data here 
        st.success(f"Donation of amount {amount} added successfully!")

elif cancelled:
    # Handle cancel button click (optional)
    st.warning("Form submission cancelled.")

##################