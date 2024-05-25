import streamlit as st

st.write("## Displaying all of the Revenue related forms here:")
###################
##ADD 

st.write("### 1. Adding the record of the Revenue generated")
# Create a form
form = st.form("Revenue generated")

# Cat Name field
catName = form.text_input("Cat Name", placeholder= "Teen Patti")

# Owner Name field
ownerName = form.text_input("Owner Name", placeholder= "Sara Qalandari")

# Owner contact text input 
ownerContact = form.text_input("Owner Contact", placeholder="03124578321")

# Date of buying items input
date = form.date_input("Date ")

# Amount input
amount = form.number_input("Amount", step= 100, value= 500)

# Payment Status
channel = form._selectbox("Channel", [
    "Selling Goods",
    "Surgery"
])

#Remarks
remarks = form.text_area("Remarks", placeholder= "Pyometra surgery performed and Ecollar sold")


# Arrange buttons horizontally & to shift to the right side -- hardcoded I guess, need to figure out some way to make sure hardcoding is not needed. This was one of the ways to do this
col1, col2, col3, col4, col5, col6, col7 = form.columns(7)
with col6:
    submitted = col6.form_submit_button("Add Revenue")
with col7:
    cancelled = col7.form_submit_button("Cancel")

# Flag to track message box visibility
show_message_box = st.empty()  # Initially empty element

if submitted:
    # Check if any of the fields are left unfilled
    if not (catName and amount and date and ownerName and ownerContact and channel and remarks):
        show_message_box.error("Please fill in all fields before submitting.")
    else:
        # Add logic to process form data here 
        st.success(f"Donation of amount {amount} added successfully!")

elif cancelled:
    # Handle cancel button click (optional)
    st.warning("Form submission cancelled.")

##################