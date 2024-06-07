import streamlit as st
import pandas as pd
import datetime
from st_pages import Page, show_pages, add_page_title, hide_pages
from PIL import Image

# logo
logo = Image.open("assets/logo.png")
st.logo(logo)

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

st.write("Need to do a lot of things!")

# Code below used to be in tab4

st.header("Wards")
# Initialize session state for ward data if not already present
if 'wards_df' not in st.session_state:
    st.session_state.wards_df = pd.DataFrame(columns=["Name", "code", "total_cages", "free_cages"])

# Create a row with search icon and search bar in the first column, and the "+ Add New Ward" button in the second column
with st.container():
    selected = st.text_input("", placeholder="🔍 Search...")

    # Define the dialog for adding a new ward
    if 'show_add_ward_dialog' not in st.session_state:
        st.session_state.show_add_ward_dialog = False

    def add_ward_dialog():
        st.session_state.show_add_ward_dialog = True


@st.experimental_dialog("Ward Details")
def Details():
    st.write("_Filter By_:")
    col1, col2 = st.columns([1, 5.5])  # Adjust the ratio as needed
    with col1:
        st.button("Date")
    with col2:
        st.button("Status")

    data = pd.read_csv("assets/wards.csv")
    
    selected_info = st.dataframe(data, on_select="rerun", selection_mode="single-row", hide_index=True)
    selected_row = selected_info["selection"]["rows"]

    # Doctor_ID = selected_row[0] + 1

    st.write("")
    edited_data = st.data_editor(data, key="data_editor", height=400, use_container_width=True, hide_index=True)
    st.caption('_:orange[Press Esc to Close]_')

@st.experimental_dialog("Add New Ward")
def add_ward():
    new_name = st.text_input("Ward Name", placeholder="Enter Ward Name")
    new_code = st.text_input("Ward Cage Code", placeholder="Enter Code for Cage e.g GW")
    new_cage = st.number_input("Total Cages", value=0, step=1, format="%d", min_value=0)
    new_free_cage = st.number_input("Free Cages", value=0, step=1, format="%d", min_value=0, max_value=0)

    add_ward_button = st.button("Add Ward")
    # cancel_ward_button = st.button("Cancel")

    if add_ward_button:
        new_row = pd.DataFrame({"code": [new_code], "total_cages": [new_cage], "free_cages": [new_free_cage]}, index=[new_name])
        st.session_state.wards_df = pd.concat([st.session_state.wards_df, new_row])
        st.session_state.show_add_ward_dialog = False
        st.experimental_rerun()

    st.caption('_:orange[Press Esc to Cancel]_')

# "Add Ward" button
st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)
new_ward = st.button("⊹ Add New Ward", on_click=add_ward_dialog)

if st.session_state.show_add_ward_dialog:
    add_ward()

def edit_ward(index):
    st.session_state.edit_index = index

def delete_ward(index):
        st.write("You need to delete the cages of this ward from the Cats data first in order to delete this ward.")
        st.warning('This is a warning', icon="⚠️")
        if st.button("Okay", key=f"confirm_delete_{index}"):
            st.session_state.wards_df = st.session_state.wards_df.drop(index).reset_index(drop=True)
            # Optionally clear any session state related to the deleted ward
            if 'edit_index' in st.session_state and st.session_state.edit_index == index:
                del st.session_state['edit_index']
            st.session_state.show_add_ward_dialog = False  # Close any open dialogs
            st.experimental_rerun()  # Refresh the app to reflect changes

def save_changes(index):
    st.session_state.wards_df.at[index, "total_cages"] = st.session_state.new_total_cages
    st.session_state.wards_df.at[index, "free_cages"] = st.session_state.new_free_cages
    st.session_state.wards_df.at[index, "code"] = st.session_state.new_code
    st.session_state.edit_index = None
    st.experimental_rerun()

# Display the ward information
wards_df = st.session_state.wards_df

if "show_options" not in st.session_state:
    st.session_state.show_options = {}

for index, row in wards_df.iterrows():
    with st.container():
        with st.expander(f"***{index}***"):
            # Assign unique key to the button
            col1, col2, col3, col4, col5, col6 = st.columns([0.1, 0.5, 0.7, 0.7, 0.5, 1])  # Adjusted column widths
            with col1:
                st.write("")  # Placeholder for the button
            with col2:
                if st.session_state.get('edit_index') == index:
                    st.session_state.new_code = st.text_input("Cage Code", value=row['code'])
                else:
                    st.write(f"Code: {row['code']}")
            with col3:
                if st.session_state.get('edit_index') == index:
                    original_total_cages = row['total_cages'] 
                    st.session_state.new_total_cages = st.number_input("Total Cages", value=row['total_cages'], min_value=original_total_cages, step=1, format="%d")
                    st.write("⚠ To reduce the number of cages, you need to first delete them from Cats' Data ")
                else:
                    st.write(f"Total Cages: {row['total_cages']}")
            with col4:
                if st.session_state.get('edit_index') == index:
                    st.session_state.new_free_cages = st.number_input("Free Cages", value=row['free_cages'], step=1, format="%d")
                else:
                    st.write(f"Free Cages: {row['free_cages']}")
            with col5:
                if st.session_state.get('edit_index') == index:
                    if st.button("Save"):
                        save_changes(index)
                else:
                    if st.button("⋮", key={index}):
                        st.session_state.show_options[index] = not st.session_state.get('show_options', {}).get(index, False)
            with col6:
                if st.session_state.get('show_options', {}).get(index, False):
                    if st.session_state.get('edit_index') != index:
                        if st.button(f"{index} Details"):
                            Details()
                        if st.button(f"Edit {index}", key=f"Edit {index}", on_click=lambda i=index: edit_ward(i)):
                            pass
                        if st.button(f"Delete {index}", key=f"Delete {index}", on_click=lambda i=index: delete_ward(i)):
                         pass
            st.write("")