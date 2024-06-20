import streamlit as st
import pandas as pd
import datetime
import sqlalchemy as sa

from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from st_pages import Page, show_pages, add_page_title, hide_pages
from PIL import Image

st.set_page_config(page_title="Finances", page_icon="💰", layout= "wide",initial_sidebar_state="expanded")

# logo
logo = Image.open("assets/logo.png")
st.logo(logo)

# TODO: fix the dialog thingy coming again and again

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

col1, col2, col3, col4 = st.columns(4)
with col1:
    with st.container(border=True):
        st.metric(label="Total Donations", value="40,689 PKR", delta="5%")

with col2:
    with st.container(border=True):
        st.metric(label="Total Revenue", value="10,293 PKR", delta="2%")

with col3:
    with st.container(border=True):
        st.metric(label="Total Transactions", value="81,100 PKR", delta="3%")

with col4:
    with st.container(border=True):
        st.metric(label="Remaining Balance", value="5,100 PKR", delta="-5.5%")

tab1, tab2, tab3 = st.tabs(["📦 Donations", "💹 Revenue", "💰 Transactions"])

with tab1:
    st.header("Donations")
   
    if 'donations_df' not in st.session_state:
        st.session_state.donations_df = pd.DataFrame(columns=["Donor Name", "Donation ID", "Contact", "Amount", "Mode", "Date"])

    if 'show_add_donation_dialog' not in st.session_state:
        st.session_state.show_add_donation_dialog = False

    def add_donation_dialog():
            st.session_state.show_add_transaction_dialog = False
            st.session_state.show_add_donation_dialog = True
            st.session_state.show_add_revenue_dialog = False  # Close revenue dialog if open

    @st.experimental_dialog("Add New Donation")
    def add_donation():
        col1, col2 = st.columns(2)
        
        with col1:
            donor_name = st.text_input("Donor Name", placeholder="Enter Donor Name")
            contact = st.text_input("Donor Contact", placeholder="XXXX-XXXXXXX")
        
        with col2:
            donor_ID = st.text_input("Donation ID", placeholder="Enter Donation ID e.g D-0001")
            amount = st.number_input("Amount Donated", value=0, step=500, format="%d", min_value=0)
            
        col3, col4 = st.columns(2)
        
        with col3:
            date = st.date_input("Donation Date", datetime.datetime.now(), disabled=True)
            
        with col4:
            mode = st.selectbox("Donation Mode", ("Cash", "Cheque", "Online"))

        add_donation_button = st.button("Add Donation")

        if add_donation_button:
            new_row = pd.DataFrame({"Donation ID": [donor_ID], "Donor Name": [donor_name], "Contact": [contact], "Amount": [amount], "Mode": [mode], "Date": [date]})
            st.session_state.donations_df = pd.concat([st.session_state.donations_df, new_row], ignore_index=True)
            st.session_state.show_add_donation_dialog = False
            st.experimental_rerun()

        st.caption('_:orange[Press Esc to Cancel]_')

    st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)
    new_donation = st.button("⊹ Add New Donation", on_click=add_donation_dialog)

    if st.session_state.show_add_donation_dialog:
        add_donation()

    def edit_donation(index):
        st.session_state.edit_index = index

    def delete_donation(index):
        st.session_state.donations_df = st.session_state.donations_df.drop(index).reset_index(drop=True)
        if 'edit_index' in st.session_state and st.session_state.edit_index == index:
            del st.session_state['edit_index']
        st.session_state.show_add_donation_dialog = False
        # st.experimental_rerun()

    def save_changes(index):
        st.session_state.donations_df.at[index, "Donor Name"] = st.session_state.new_name
        st.session_state.donations_df.at[index, "Donation ID"] = st.session_state.new_id
        st.session_state.donations_df.at[index, "Contact"] = st.session_state.new_contact
        st.session_state.donations_df.at[index, "Amount"] = st.session_state.new_amount
        st.session_state.donations_df.at[index, "Mode"] = st.session_state.new_mode
        st.session_state.donations_df.at[index, "Date"] = st.session_state.new_date
        st.session_state.edit_index = None
        st.experimental_rerun()

    donations_df = st.session_state.donations_df

    if "show_options" not in st.session_state:
        st.session_state.show_options = {}

    for index, row in donations_df.iterrows():
        with st.container():
            with st.expander(f"***{row['Donation ID']}***"):
                col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
                with col1:
                    if st.session_state.get('edit_index') == index:
                        st.session_state.new_name = st.text_input("Donor Name", value=row['Donor Name'])
                    else:
                        st.write(f"Name: {row['Donor Name']}")
                with col2:
                    if st.session_state.get('edit_index') == index:
                        st.session_state.new_id = st.text_input("Donation ID", value=row['Donation ID'])
                    else:
                        st.write(f"ID: {row['Donation ID']}")
                with col3:
                    if st.session_state.get('edit_index') == index:
                        st.session_state.new_contact = st.text_input("Donor Contact", value=row['Contact'])
                    else:
                        st.write(f"Donor Contact: {row['Contact']}")
                with col4:
                    if st.session_state.get('edit_index') == index:
                        st.session_state.new_amount = st.text_input("Amount Donated", value=row['Amount'])
                    else:
                        st.write(f"Amount Donated: {row['Amount']}")
                with col5:
                    if st.session_state.get('edit_index') == index:
                        st.session_state.new_mode = st.selectbox("Mode", ["Cash", "Cheque", "Online"], index=["Cash", "Cheque", "Online"].index(row['Mode']))
                    else:
                        st.write(f"Mode: {row['Mode']}")
                with col6:
                    if st.session_state.get('edit_index') == index:
                        st.session_state.new_date = st.date_input("Donation Date", value=pd.to_datetime(row['Date']), key=f"date_{index}")
                    else:
                        st.write(f"Date: {row['Date']}")
                with col7:
                    if st.session_state.get('edit_index') == index:
                        if st.button("Save"):
                            save_changes(index)
                    else:
                        if st.button("Edit", key=f"edit_donation_{index}", on_click=lambda i=index: edit_donation(i)):
                            pass
                with col8:
                    if st.button("Delete", key=f"delete_donation{index}", on_click=lambda i=index: delete_donation(i)):
                        pass
                st.write("")

# ---------------------------------------------------------------------------------------------------------------------------

with tab2:
    st.header("Revenue")
    if 'revenue_df' not in st.session_state:
        st.session_state.revenue_df = pd.DataFrame(columns=["Name", "ID", "contact", "amount", "remarks" "mode", "date"])

    if 'show_add_revenue_dialog' not in st.session_state:
        st.session_state.show_add_revenue_dialog = False

    def add_revenue_dialog():
            st.session_state.show_add_transaction_dialog = False
            st.session_state.show_add_revenue_dialog = True
            st.session_state.show_add_donation_dialog = False  # Close donation dialog if open

    @st.experimental_dialog("Add New Revenue")
    def add_revenue():
        col1, col2 = st.columns(2)
        
        with col1:
            rev_name = st.text_input("Name", placeholder="Enter Name")
            rev_contact = st.text_input("Contact", placeholder="XXXX-XXXXXXX")
        
        with col2:
            rev_ID = st.text_input("ID", placeholder="Enter ID e.g PA-001")
            rev_amount = st.number_input("Amount", value=0, step=500, format="%d", min_value=0)
            
        col3, col4 = st.columns(2)
        
        with col3:
            rev_date = st.date_input("Revenue Date", datetime.datetime.now(), disabled=True)
            
        with col4:
            rev_mode = st.selectbox("Revenue Mode", ("Cash", "Cheque", "Online"))
            
        rev_remarks = st.text_area("Remarks", placeholder="Bought a collar")

        add_rev_button = st.button("Add Revenue")

        if add_rev_button:
            new_row = pd.DataFrame({"Name": [rev_name], "ID": [rev_ID], "contact": [rev_contact], "amount": [rev_amount], "remarks": [rev_remarks], "mode": [rev_mode], "date": [rev_date]})
            st.session_state.revenue_df = pd.concat([st.session_state.revenue_df, new_row], ignore_index=True)
            st.session_state.show_add_revenue_dialog = False
            st.experimental_rerun()

        st.caption('_:orange[Press Esc to Cancel]_')

    st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)
    new_revenue = st.button("⊹ Add New Revenue", on_click=add_revenue_dialog)

    if st.session_state.show_add_revenue_dialog:
        add_revenue()

    def edit_revenue(index1):
        st.session_state.edit_index = index1

    def delete_revenue(index1):
        st.session_state.revenue_df = st.session_state.revenue_df.drop(index1).reset_index(drop=True)
        if 'edit_index1' in st.session_state and st.session_state.edit_index == index1:
            del st.session_state['edit_index1']
        st.session_state.show_add_revenue_dialog = False
        # st.experimental_rerun()

    def save_changes(index1):
        st.session_state.revenue_df.at[index1, "Name"] = st.session_state.new_rev_name
        st.session_state.revenue_df.at[index1, "ID"] = st.session_state.new_rev_id
        st.session_state.revenue_df.at[index1, "contact"] = st.session_state.new_rev_contact
        st.session_state.revenue_df.at[index1, "amount"] = st.session_state.new_rev_amount
        st.session_state.revenue_df.at[index1, "mode"] = st.session_state.new_rev_mode
        st.session_state.revenue_df.at[index1, "remarks"] = st.session_state.new_rev_remarks
        st.session_state.revenue_df.at[index1, "date"] = st.session_state.new_rev_date
        st.session_state.edit_index = None
        st.experimental_rerun()

    revenue_df = st.session_state.revenue_df

    if "show_options" not in st.session_state:
        st.session_state.show_options = {}

    for index1, row in revenue_df.iterrows():
        with st.container():
            with st.expander(f"***{row['ID']}***"):
                col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
                with col1:
                    if st.session_state.get('edit_index') == index1:
                        st.session_state.new_rev_name = st.text_input("Name", value=row['Name'])
                    else:
                        st.write(f"Name: {row['Name']}")
                with col2:
                    if st.session_state.get('edit_index') == index1:
                        st.session_state.new_rev_id = st.text_input("ID", value=row['ID'])
                    else:
                        st.write(f"ID: {row['ID']}")
                with col3:
                    if st.session_state.get('edit_index') == index1:
                        st.session_state.new_rev_contact = st.text_input("Contact", value=row['contact'])
                    else:
                        st.write(f"Contact: {row['contact']}")
                with col4:
                    if st.session_state.get('edit_index') == index1:
                        st.session_state.new_rev_amount = st.text_input("Amount", value=row['amount'], key=f"rev_amount_{index1}")
                    else:
                        st.write(f"Revenue Amount: {row['amount']}")
                with col5:
                    if st.session_state.get('edit_index') == index1:
                        st.session_state.new_rev_mode = st.selectbox("Mode", ["Cash", "Cheque", "Online"], key=f"rev_mode_{index1}", index=["Cash", "Cheque", "Online"].index(row['mode']))
                    else:
                        st.write(f"Mode: {row['mode']}")
                with col6:
                    if st.session_state.get('edit_index') == index1:
                        st.session_state.new_rev_remarks = st.text_input("Remarks", value=row['remarks'])
                    else:
                        st.write(f"Remarks: {row['remarks']}")
                with col7:
                    if st.session_state.get('edit_index') == index1:
                        st.session_state.new_rev_date = st.date_input("Date", value=pd.to_datetime(row['date']), key=f"rev_date_{index1}")
                    else:
                        st.write(f"Date: {row['date']}")
                with col8:
                    if st.session_state.get('edit_index') == index1:
                        if st.button("Save", key=f"save_revenue_{index1}"):
                            save_changes(index1)
                    else:
                       if st.button("Edit", key=f"edit_revenue_{index1}", on_click=lambda i=index1: edit_revenue(i)):
                            pass
                with col9:
                    if st.button("Delete", key=f"delete_revenue{index1}", on_click=lambda i=index1: delete_revenue(i)):
                        pass
                st.write("")

# -----------------------------------------------------------------------------------------------------------------------------

with tab3:
    st.header("Transactions")

    if 'transaction_df' not in st.session_state:
        st.session_state.transaction_df = pd.DataFrame(columns=["t_name", "t_ID", "t_amount", "t_remarks" "t_mode", "t_date"])

    if 'show_add_transaction_dialog' not in st.session_state:
        st.session_state.show_add_transaction_dialog = False

    def add_transaction_dialog():
            st.session_state.show_add_transaction_dialog = True #only transaction will be open
            st.session_state.show_add_revenue_dialog = False #close revenue dialgog if open
            st.session_state.show_add_donation_dialog = False  # Close donation dialog if open

    @st.experimental_dialog("Add Revenue")
    def add_transaction():
        col1, col2 = st.columns(2)
        
        with col1:
            tran_ID = st.text_input("Transaction ID", placeholder="Enter ID e.g T-001")
            tran_amount = st.number_input("Amount", value=0, step=500, format="%d", min_value=0)
        
        with col2:
            tran_name = st.text_input("Name", placeholder="Enter Name")
            tran_mode = st.selectbox("Transaction Mode", ("Cash", "Cheque", "Online"))
            
        tran_date = st.date_input("Transaction Date", datetime.datetime.now(), disabled=True)
        tran_remarks = st.text_area("Remarks", placeholder="-")

        add_tran_button = st.button("Add New Transaction")

        if add_tran_button:
            new_row = pd.DataFrame({"t_name": [tran_name], "t_ID": [tran_ID], "t_amount": [tran_amount], "t_remarks": [tran_remarks], "t_mode": [tran_mode], "t_date": [tran_date]})
            st.session_state.transaction_df = pd.concat([st.session_state.transaction_df, new_row], ignore_index=True)
            st.session_state.show_add_transaction_dialog = False
            st.experimental_rerun()

        st.caption('_:orange[Press Esc to Cancel]_')
    
    st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)
    new_transaction = st.button("⊹ Add New Transaction", on_click=add_transaction_dialog)

    if st.session_state.show_add_transaction_dialog:
        add_transaction()

    def edit_transaction(index2):
        st.session_state.edit_index = index2

    def delete_transaction(index2):
        st.session_state.transaction_df = st.session_state.transaction_df.drop(index2).reset_index(drop=True)
        if 'edit_index2' in st.session_state and st.session_state.edit_index == index2:
            del st.session_state['edit_index2']
        st.session_state.show_add_transaction_dialog = False
        # st.experimental_rerun()

    def save_changes(index2):
        st.session_state.transaction_df.at[index2, "t_name"] = st.session_state.new_tran_name
        st.session_state.transaction_df.at[index2, "t_ID"] = st.session_state.new_tran_id
        st.session_state.transaction_df.at[index2, "t_amount"] = st.session_state.new_tran_amount
        st.session_state.transaction_df.at[index2, "t_mode"] = st.session_state.new_tran_mode
        st.session_state.transaction_df.at[index2, "t_remarks"] = st.session_state.new_tran_remarks
        st.session_state.transaction_df.at[index2, "t_date"] = st.session_state.new_tran_date
        st.session_state.edit_index = None
        st.experimental_rerun()

    transaction_df = st.session_state.transaction_df

    if "show_options" not in st.session_state:
        st.session_state.show_options = {}

    for index2, row in transaction_df.iterrows():
        with st.container():
            with st.expander(f"***{row['t_ID']}***"):
                col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
                with col1:
                    if st.session_state.get('edit_index') == index2:
                        st.session_state.new_tran_name = st.text_input("Name", value=row['t_name'])
                    else:
                        st.write(f"Transaction Name: {row['t_name']}")
                with col2:
                    if st.session_state.get('edit_index') == index2:
                        st.session_state.new_tran_id = st.text_input("ID", value=row['t_ID'])
                    else:
                        st.write(f"Transaction ID: {row['t_ID']}")
                with col3:
                    if st.session_state.get('edit_index') == index2:
                        st.session_state.new_tran_amount = st.text_input("Amount", value=row['t_amount'], key=f"tran_amount_{index2}")
                    else:
                        st.write(f"Transaction Amount: {row['t_amount']}")
                with col4:
                    if st.session_state.get('edit_index') == index2:
                        st.session_state.new_tran_mode = st.selectbox("Mode", ["Cash", "Cheque", "Online"], key=f"tran_mode_{index2}", index=["Cash", "Cheque", "Online"].index(row['t_mode']))
                    else:
                        st.write(f"Transaction Mode: {row['t_mode']}")
                with col5:
                    if st.session_state.get('edit_index') == index2:
                        st.session_state.new_tran_remarks = st.text_input("Remarks", value=row['t_remarks'])
                    else:
                        st.write(f"Remarks for Transaction: {row['t_remarks']}")
                with col6:
                    if st.session_state.get('edit_index') == index2:
                        st.session_state.new_tran_date = st.date_input("Date", value=pd.to_datetime(row['t_date']), key=f"tran_date_{index2}")
                    else:
                        st.write(f"Transaction Date: {row['t_date']}")
                with col7:
                    if st.session_state.get('edit_index') == index2:
                        if st.button("Save", key=f"save_transaction_{index2}"):
                            save_changes(index2)
                    else:
                       if st.button("Edit", key=f"edit_transaction_{index2}", on_click=lambda i=index2: edit_transaction(i)):
                            pass
                with col8:
                    if st.button("Delete", key=f"delete_transaction{index2}", on_click=lambda i=index2: delete_transaction(i)):
                        pass
                st.write("")