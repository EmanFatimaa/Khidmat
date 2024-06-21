import streamlit as st
import pandas as pd
import datetime
import sqlalchemy as sa
from millify import prettify

from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from st_pages import Page, show_pages, add_page_title, hide_pages
from PIL import Image

# database information ; will change when db hosting
server = 'DESKTOP-B3MBPDD\\FONTAINE' # 'DESKTOP-HT3NB74' # Note the double backslashes
database = 'PawRescue' # 'Khidmat'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

st.set_page_config(page_title="Finances", page_icon="💰", layout= "wide",initial_sidebar_state="expanded")

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

st.header("Finances")

col1, col2, col3, col4 = st.columns(4)
with col1:
    with st.container(border=True):
        # everything indented is communicating with the database ; closes automatically
        with engine.begin() as conn:
            total_donations = pd.read_sql_query(sa.text("select sum(amount) from Donations"), conn)
        st.metric(label="Total Donations", value = prettify(int(total_donations.iloc[0][0])) + " PKR")

with col2:
    with st.container(border=True):
        with engine.begin() as conn:
            total_revenue = pd.read_sql_query(sa.text("select sum(amount) from Revenue"), conn)
        st.metric(label="Total Revenue", value = prettify(int(total_revenue.iloc[0][0])) + " PKR")

with col3:
    with st.container(border=True):
        with engine.begin() as conn:
            total_trans = pd.read_sql_query(sa.text("select sum(amount) from Transactions"), conn)
        st.metric(label="Total Transactions", value = prettify(int(total_trans.iloc[0][0])) + " PKR")

with col4:
    with st.container(border=True):
        st.metric(label="Remaining Balance", value= prettify(int(total_donations.iloc[0][0]) + int(total_revenue.iloc[0][0]) - int(total_trans.iloc[0][0])) + " PKR")

tab1, tab2, tab3 = st.tabs(["📦 Donations", "💹 Revenue", "💰 Transactions"])

with tab1:
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

            with engine.begin() as conn:
                current_donationid = int(pd.read_sql_query(sa.text("select top 1 donationID from Donations order by donationID desc"), conn).iloc[0][0]) + 1
            donor_ID = st.text_input("Donation ID", value = current_donationid, disabled = True)
        
            with engine.begin() as conn:
                donation_mode = pd.read_sql_query(sa.text("select mode from Mode"), conn)
            mode = st.selectbox("Donation Mode", donation_mode["mode"].tolist())

        with col2:
            with engine.begin() as conn: # if user already in the database then automatically fill the contact number.
                fetchall = conn.execute(sa.text("select contactNum from Externals where name = :name"), {"name": donor_name}).fetchall()
                contact_from_db = ''
                for row in fetchall:
                    contact_from_db = row[0]
            contact = st.text_input("Donor Contact", value = contact_from_db, placeholder="0324-2059215")

            date = st.date_input("Donation Date", datetime.datetime.now(), disabled=True)

            amount = st.text_input("Amount Donated", value=0)

        # TODO: add a check if all the fields are filled or not and are the correct type or not.
        # TODO: need to have a check as well that the user really needs to add the donation or not.
        # TODO: Filtering

        add_donation_button = st.button("Add Donation")

        if add_donation_button:
            with engine.begin() as conn:
                conn.execute(sa.text(""" 
                if not exists(select externalID from Externals where name = :name)
                    begin 
                        insert into Externals values
                            ((select top 1 externalID from Externals order by externalID desc) + 1, 
                            :name, :contact, Null,(select externalRoleID from ExternalRole where roleDesc = 'Donor'))
                    end

                insert into Donations
                values (:donor_ID, (select externalID from Externals where name = :name), (select modeID from Mode where mode = :mode), :amount, :date)
                """), {"name": donor_name, "name": donor_name, "contact": contact, "donor_ID": donor_ID, "name": donor_name, "mode": mode, "amount": amount, "date": date})
            st.rerun()

        st.session_state.show_add_donation_dialog = False
        st.caption('_:orange[Press Esc to Cancel]_')

    col1, col2 = st.columns([6,1])
    col1.write("Filtering Remains.")
    # Add a New Donation Button
    st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)
    new_donation = col2.button("⊹ Add New Donation", on_click=add_donation_dialog)

    if st.session_state.show_add_donation_dialog:
        add_donation()

    # Table for Donations
    with engine.begin() as conn:
        donation_table = pd.read_sql_query(
        sa.text("""select donationID as 'Donation ID', 
	                      name as 'Donor Name', 
	                      contactNum as 'Contact Number', 
	                      amount as 'Amount', 
	                      (select mode from Mode where Mode.modeID = Donations.modeID) as 'Mode', 
	                      date as 'Date' 
                    from Donations, Externals where Donations.donorID = Externals.externalID"""), conn)
        
    st.dataframe(donation_table, width=1500, height=600, hide_index = True, on_select = "rerun", selection_mode = "single-row") 

    # TODO: we can have update and delete any donations but only for admin

# ---------------------------------------------------------------------------------------------------------------------------

with tab2:
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

            with engine.begin() as conn:
                current_revenueid = int(pd.read_sql_query(sa.text("select top 1 revenueID from Revenue order by revenueID desc"), conn).iloc[0][0]) + 1
            rev_ID = st.text_input("Revenue ID", value = current_revenueid, disabled = True)
        
            with engine.begin() as conn:
                revenue_mode = pd.read_sql_query(sa.text("select mode from Mode"), conn)
            mode = st.selectbox("Revenue Mode", revenue_mode["mode"].tolist())
            
        with col2:
            
            with engine.begin() as conn: # if user already in the database then automatically fill the contact number.
                fetchall = conn.execute(sa.text("select contactNum from Externals where name = :name"), {"name": rev_name}).fetchall()
                contact_from_db = ''
                for row in fetchall:
                    contact_from_db = row[0]
            contact = st.text_input("Contact", value = contact_from_db, placeholder="0324-2059215")

            date = st.date_input("Revenue Date", datetime.datetime.now(), disabled=True)

            amount = st.text_input("Amount", value=0)

        col5, col6 = st.columns([1,0.000000000000001])

        with col5:
            remarks = st.text_area("Remarks", placeholder="Bought a collar")

        # TODO: add a check if all the fields are filled or not and are the correct type or not.
        # TODO: need to have a check as well that the user really needs to add the donation or not.
        # TODO: Filtering

        add_rev_button = st.button("Add Revenue")

        if add_rev_button:
            with engine.begin() as conn:
                conn.execute(sa.text(""" 
                    if not exists(select externalID from Externals where name = :name)
                        begin 
                            insert into Externals values
                                ((select top 1 externalID from Externals order by externalID desc) + 1, 
                                :name, :contact, Null,(select externalRoleID from ExternalRole where roleDesc = 'Buyer'))
                        end

                    insert into Revenue
                    values (:rev_ID, (select externalID from Externals where name = :name), (select modeID from Mode where mode = :mode), :date, :amount, :remarks)
                    """), {"name": rev_name, "name": rev_name, "contact": contact, "rev_ID": rev_ID, "name": rev_name, "mode": mode, "date": date, "amount": amount, "remarks": remarks})
            st.rerun()

        st.session_state.show_add_revenue_dialog = False
        st.caption('_:orange[Press Esc to Cancel]_')

    col1, col2 = st.columns([6,1])
    col1.write("Filtering Remains.")
    # Add a New Revenue Button
    st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)
    new_revenue = col2.button("⊹ Add New Revenue", on_click=add_revenue_dialog)

    if st.session_state.show_add_revenue_dialog:
        add_revenue()
    
    # Table for Revenue
    with engine.begin() as conn:
        revenue_table = pd.read_sql_query(sa.text("""
        select revenueID as 'Revenue ID', 
        name as 'Name', 
        contactNum as 'Contact Number', 
        amount as 'Amount', 
        (select mode from Mode where Mode.modeID = Revenue.modeID) as 'Mode', 
        remarks as 'Remark',
        date as 'Date' 
        from Revenue, Externals where Revenue.buyerID = Externals.externalID"""), conn)
        
    st.dataframe(revenue_table, width=1500, height=600, hide_index = True, on_select = "rerun", selection_mode = "single-row")

    # TODO: we can have update and delete any revenue but only for admin
    
# -----------------------------------------------------------------------------------------------------------------------------

with tab3:
    if 'show_add_transaction_dialog' not in st.session_state:
        st.session_state.show_add_transaction_dialog = False

    def add_transaction_dialog():
            st.session_state.show_add_transaction_dialog = True #only transaction will be open
            st.session_state.show_add_revenue_dialog = False #close revenue dialgog if open
            st.session_state.show_add_donation_dialog = False  # Close donation dialog if open

    @st.experimental_dialog("Add New Transaction")
    def add_transaction():

        col1, col2 = st.columns([1,0.000000000000001])

        with col1:
            billFor = st.text_area("Bill For", placeholder="Enter bill for")

        col3, col4 = st.columns(2)
        
        with col3:
            with engine.begin() as conn:
                trans_mode = pd.read_sql_query(sa.text("select mode from Mode"), conn)
                current_transid = int(pd.read_sql_query(sa.text("select top 1 transactionID from Transactions order by transactionID desc"), conn).iloc[0][0]) + 1
            mode = st.selectbox("Transaction Mode", trans_mode["mode"].tolist())
            trans_ID = st.text_input("Transaction ID", value = current_transid, disabled = True)
        
        with col4:
            amount = st.text_input("Amount", value=0)
            date = st.date_input("Transaction Date", datetime.datetime.now(), disabled=True)
        
        col5, col6 = st.columns([1,0.000000000000001])
        with col5:
            remarks = st.text_area("Remarks", placeholder="")

        # TODO: add a check if all the fields are filled or not and are the correct type or not.
        # TODO: need to have a check as well that the user really needs to add the donation or not.
        # TODO: Filtering

        add_tran_button = st.button("Add New Transaction")

        if add_tran_button:
            with engine.begin() as conn:
                conn.execute(sa.text(""" 
insert into Transactions
values (:trans_ID, (select modeID from Mode where mode = :mode), :amount, :billFor, :date, :remarks)
                                     """), {"trans_ID":trans_ID, "mode": mode, "amount": amount, "billFor": billFor, "date": date, "remarks": remarks})
            st.rerun()
        
        st.session_state.show_add_transaction_dialog = False
        st.caption('_:orange[Press Esc to Cancel]_')
    
    col1, col2 = st.columns([6,1])
    col1.write("Filtering Remains.")
    # Add a New Transaction Button
    st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)
    new_transaction = col2.button("⊹ Add Transaction", on_click=add_transaction_dialog)

    if st.session_state.show_add_transaction_dialog:
        add_transaction()

    # Table for Transactions
    with engine.begin() as conn:
        transaction_table = pd.read_sql_query(sa.text("""
select transactionID as 'Transaction ID', billFor as 'Bill For', amount as 'Amount', 
(select mode from Mode where Mode.modeID = Transactions.modeID) as 'Mode', remarks as 'Remarks', date as 'Date' from Transactions"""), conn)
    
    st.dataframe(transaction_table, width=1500, height=600, hide_index = True, on_select = "rerun", selection_mode = "single-row") 

    # TODO: we can have update and delete any donations but only for admin