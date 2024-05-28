import streamlit as st

st.write("## Displaying all of the Transaction related forms here:")
###################
##ADD 

st.write("### 1. Adding the record of the Transaction made (Bills Paid)")
# Create a form
form = st.form("Transaction Made")

# Date of buying items input
dateOfPurchase = form.date_input("Date of purchasing items")

# Amount input
amount = form.number_input("Amount", step= 100, value= 500)

#Remarks
remarks = form.text_area("Remarks", placeholder= "Bill for buying 2Kg Chicken")

# Payment Status
status = form._selectbox("Payment Status", [
    "Paid",
    "Pending",
    "Unpaid"
])

# Donor Name field
remitterName = form.text_input("Remitter Name", placeholder= "Shamsur Rehman")


# Mode of Payment
modeOfPayment = form.selectbox("Mode of Payment", [
        "Donation Box", 
        "Online Payment",
        "Petty Cash in hand"
    ])

# Date of payment input
dateOfProcessing = form.date_input("Date of processing payment")

# Arrange buttons horizontally & to shift to the right side -- hardcoded I guess, need to figure out some way to make sure hardcoding is not needed. This was one of the ways to do this
col1, col2, col3, col4, col5, col6, col7 = form.columns([1,1,1,2,5,3,2])
with col6:
    submitted = col6.form_submit_button("Add Transaction")
with col7:
    cancelled = col7.form_submit_button("Cancel")

# Flag to track message box visibility
show_message_box = st.empty()  # Initially empty element

if submitted:
    # Check if any of the fields are left unfilled
    if not (dateOfPurchase and amount and dateOfProcessing and modeOfPayment and remitterName and status):
        show_message_box.error("Please fill in all fields before submitting.")
    else:
        # Add logic to process form data here 
        st.success(f"Donation of amount {amount} added successfully!")

elif cancelled:
    # Handle cancel button click (optional)
    st.warning("Form submission cancelled.")

##################