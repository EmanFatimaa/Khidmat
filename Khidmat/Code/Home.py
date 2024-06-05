import streamlit as st
import pandas as pd
#for image..
from PIL import Image


st.set_page_config(
    page_title="Paw Rescue Database Management System", 
    page_icon="👋 ", # to be replace with their logo
)


#Adding a new member button
st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)


#LOGO GOES HERE -- sidebar..
img= Image.open("logo.png")
st.logo(img ) #, caption= "Paw Rescue Poster"
####################
st.image(img) #, caption= "Paw Rescue
####################
# # Custom CSS for centering text
# st.markdown(
#     """
#     <style>
#     .center-text {
#         text-align: center;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# Using HTML within st.markdown to center-align text
# st.markdown("<h2 class='center-text'>Paws Rescue DataBase Management System!</h2>", unsafe_allow_html=True)
###################
# USER CHOICE:

# Add a radio button to let the user choose between Login and Sign Up
choice = st.radio("Are you already a user?", ["Login", "Sign Up"])

# Display the Login form if the user chooses Login
if choice == "Login":
    st.write("## Login")
    # Your login form code goes here...


    ###################
    ##Login

    # Create a form
    form = st.form("Login")

    # Name field
    userName = form.text_input("Email address or User name", placeholder= "abc@gmail.com")

    # User Type dropdown with new options
    UserType = form.selectbox("User Type", [
        "Admin", 
        "Finance Manager",
        "Social Media Manager",
        "Vet"
    ])

    # Cage number text input
    password = form.text_input("Password",type="password" ,placeholder= "••••••••••")

    # Arrange buttons horizontally & to shift to the right side -- hardcoded I guess, need to figure out some way to make sure hardcoding is not needed. This was one of the ways to do this
    col1, col2, col3, col4, col5, col6, col7 = form.columns(7)
    with col6:
        submitted = col6.form_submit_button("Login")
    with col7:
        cancelled = col7.form_submit_button("Cancel")

    # Flag to track message box visibility
    show_message_box = st.empty()  # Initially empty element

    if submitted:
        # Check if any of the fields are left unfilled
        if not (userName and UserType and password):
            show_message_box.error("Please fill in all fields before submitting.")
        else:
            # Add logic to process form data here 
            st.success(f"User Name {userName} logged in successfully!")

    elif cancelled:
        # Handle cancel button click (optional)
        st.warning("Form submission cancelled.")


########################
##SIGN UP

# Display the Sign Up form if the user chooses Sign Up
elif choice == "Sign Up":
    st.write("## Sign Up")
    # Your sign-up form code goes here...

    # Create a form
    form = st.form("Sign Up")

    # Name field
    userName = form.text_input("Email address or User name", placeholder= "abc@gmail.com")

    # User Type dropdown with new options
    UserType = form.selectbox("User Type", [
        "Admin", 
        "Finance Manager",
        "Social Media Manager",
        "Vet"
    ])

    # Cage number text input
    password = form.text_input("Password", type="password", placeholder= "••••••••••")
    confirmPassword = form.text_input("Confirm Password", type="password", placeholder= "••••••••••")

    # Arrange buttons horizontally & to shift to the right side -- hardcoded I guess, need to figure out some way to make sure hardcoding is not needed. This was one of the ways to do this
    col1, col2, col3, col4, col5, col6, col7 = form.columns(7)
    with col6:
        submitted = col6.form_submit_button("Sign Up")
    with col7:
        cancelled = col7.form_submit_button("Cancel")

    # Flag to track message box visibility
    show_message_box = st.empty()  # Initially empty element

    if submitted:
        # Check if any of the fields are left unfilled
        if not (userName and UserType and password and confirmPassword):
            show_message_box.error("Please fill in all fields before submitting.")
        else:
            # Add logic to process form data here 
            st.success(f"User Name {userName} signed up successfully!")

    elif cancelled:
        # Handle cancel button click (optional)
        st.warning("Form submission cancelled.")

# def jumpToPage():
#     st.switch_page("Pages\7_👥_Team.py")
# with st.sidebar():
# if st.sidebar.button('**👥Team Member**'):
#     jumpToPage()
        
# st.sidebar.button('**🔒Log out**')

# # if team:
# #     jumpToPage()

# # else:
# #     st.write("Watever")

# with st.sidebar:
if st.sidebar.button('**👥Team Member**'):
    st.switch_page("Pages\7_👥_Team.py")
    # elif st.button('**🔒Log out**'):