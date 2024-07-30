# standard imports
import datetime
from PIL import Image
import time

# third party imports
import pandas as pd
import sqlalchemy as sa
import streamlit as st

# custom imports
from millify import prettify
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

# custom streamlit imports
from st_pages import Page, show_pages, add_page_title, hide_pages

# streamlit-authenticator package
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# database information ; will change when db hosting

# Note the double backslashes
# server = 'DESKTOP-67BT6TD\\FONTAINE' # IBAD
server = 'DESKTOP-HT3NB74' # EMAN
# server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA

database = 'DummyPawRescue'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

st.set_page_config(page_title="Finances", page_icon="💰", layout= "wide",initial_sidebar_state="expanded")

# logo
logo = Image.open("assets/logo.png")
st.logo(logo)

# Button Styling
st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)

st.markdown(
        """
       <style>
       [data-testid="stSidebar"][aria-expanded="true"]{
           min-width: 250px;
           max-width: 250px;
       }
       """,
        unsafe_allow_html=True,
)

hide_pages(["Login"])

st.header("Finances", divider='orange')

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        # everything indented is communicating with the database ; closes automatically
        with engine.begin() as conn:
            total_donations = pd.read_sql_query(sa.text("select sum(amount) from Donations"), conn)
        st.metric(label="Total Donations", value = prettify(int(total_donations.iat[0,0])) + " PKR")

with col2:
    with st.container(border=True):
        with engine.begin() as conn:
            total_revenue = pd.read_sql_query(sa.text("select sum(amount) from Revenue"), conn)
        st.metric(label="Total Revenue", value = prettify(int(total_revenue.iat[0,0])) + " PKR")

with col3:
    with st.container(border=True):
        with engine.begin() as conn:
            total_trans = pd.read_sql_query(sa.text("select sum(amount) from Transactions"), conn)
        st.metric(label="Total Transactions", value = prettify(int(total_trans.iat[0,0])) + " PKR")

with col4:
    with st.container(border=True):
        st.metric(label="Remaining Balance", value= prettify(int(total_donations.iat[0,0]) + int(total_revenue.iat[0,0]) - int(total_trans.iat[0,0])) + " PKR")

Donations, Revenue, Transactions = st.tabs(["📦 Donations", "💹 Revenue", "💰 Transactions"])

with Donations:

    def add_donation_dialog():
            st.session_state.show_add_transaction_dialog = False
            st.session_state.show_add_donation_dialog = True
            st.session_state.show_add_revenue_dialog = False  # Close revenue dialog if open
            st.session_state.show_update_donation_dialog = False
            st.session_state.show_delete_donation_dialog = False
    
    def update_donation_dialog():
            st.session_state.show_add_transaction_dialog = False
            st.session_state.show_add_donation_dialog = False
            st.session_state.show_add_revenue_dialog = False
            st.session_state.show_update_donation_dialog = True
            st.session_state.show_delete_donation_dialog = False
    
    def delete_donation_dialog():
            st.session_state.show_add_transaction_dialog = False
            st.session_state.show_add_donation_dialog = False
            st.session_state.show_add_revenue_dialog = False
            st.session_state.show_update_donation_dialog = False
            st.session_state.show_delete_donation_dialog = True


    def display_unique_filters(dynamic_filters, filters_name, num_columns=2):
        unique_keys = {filter_name: f"{filters_name}_{filter_name}" for filter_name in dynamic_filters.filters}
        
        col1, col2 = st.columns(num_columns)
        with col1:
            for filter_name in dynamic_filters.filters:
                options = sorted(dynamic_filters.df[filter_name].dropna().unique())
                selected = st.multiselect(
                    f"Select {filter_name}", 
                    options, 
                    key=unique_keys[filter_name]
                )
                dynamic_filters.df = dynamic_filters.df[dynamic_filters.df[filter_name].isin(selected) | (dynamic_filters.df[filter_name].isna())]
        return dynamic_filters.df

    @st.experimental_dialog("Add New Donation")
    def add_donation():
        col1, col2 = st.columns(2)
        
        with col1:
            donor_name = st.text_input("Donor Name", placeholder="Enter Donor Name")

            with engine.begin() as conn:
                current_donationid = int(pd.read_sql_query(sa.text("select top 1 donationID from Donations order by donationID desc"), conn).iat[0,0]) + 1
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

            date = st.date_input("Donation Date", datetime.datetime.now(), disabled = False)

            amount = st.text_input("Amount Donated")

        add_donation_button = st.button("Add Donation")

        if add_donation_button:

            # Checks
            everything_filled = False
            valid_name = False
            valid_contact = False
            valid_amount = False

            # Check if any of the fields are left unfilled
            if not (donor_name and contact and donor_ID and mode and amount and date):
                st.error("Please fill in all fields before submitting.")
            else:
                everything_filled = True

            # Check if the name is valid
            if all(x.isalpha() or x.isspace() for x in donor_name):
                valid_name = True
            else:
                st.error("Please enter a valid name.")

            # Check if the contact number is valid
            try:
                if len(contact) != 12 and contact[4] != '-' and all(x.isnumeric() or x == '-' for x in contact):
                    st.error("Please enter a valid contact number. (include - after 4th digit)")
                else:
                    valid_contact = True
            except:
                st.error("Please enter a valid contact number. (include - after 4th digit)")
            
            # Check if the donation ID is valid
            if amount.isnumeric() == False:
                st.error("Please enter a valid amount.")
            else:
                valid_amount = True
            
            # There shouldn't be error with date, mode and donor_ID as they are selected from the dropdowns or automatically filled.

            if everything_filled and valid_name and valid_contact and valid_amount:
                with engine.begin() as conn:
                    conn.execute(sa.text(""" 
                    if not exists(select externalID from Externals where name = :name)
                        begin 
                            insert into Externals values
                                ((select top 1 externalID from Externals order by externalID desc) + 1, 
                                :name, :contact, Null)
                        end

                    insert into Donations
                    values (:donor_ID, (select externalID from Externals where name = :name), (select modeID from Mode where mode = :mode), :amount, :date)
                    """), {"name": donor_name, "name": donor_name, "contact": contact, "donor_ID": donor_ID, "name": donor_name, "mode": mode, "amount": amount, "date": date})
                st.rerun()

        st.session_state.show_add_donation_dialog = False
        st.caption('_:orange[Press Esc to Cancel]_')
    
    @st.experimental_dialog("Update Donation")
    def update_donation(id_to_update):
        col1, col2 = st.columns(2)
        
        with col1:
            with engine.begin() as conn:
                name_value = conn.execute(sa.text("select name from Externals where externalID = (select donorID from Donations where donationID = :donationID)"), {"donationID": id_to_update}).fetchall()[0][0]
            donor_name = st.text_input("Donor Name", placeholder="Enter Donor Name", value = name_value)

            donor_ID = st.text_input("Donation ID", value = id_to_update, disabled = True)

            with engine.begin() as conn:
                donation_mode = pd.read_sql_query(sa.text("select mode from Mode"), conn)
                mode_value = conn.execute(sa.text("select mode from Mode where modeID = (select modeID from Donations where donationID = :donationID)"), {"donationID": id_to_update}).fetchall()[0][0]
                final_mode_value = 1 if mode_value == 'Cash' else 0
            mode = st.selectbox("Donation Mode", donation_mode["mode"].tolist(), index = final_mode_value)

        with col2:
            with engine.begin() as conn:
                contact_value = conn.execute(sa.text("select contactNum from Externals where name = :name"), {"name": name_value}).fetchall()[0][0]
            contact = st.text_input("Donor Contact", value = contact_value, placeholder="0324-2059215")

            with engine.begin() as conn:
                date_value = conn.execute(sa.text("select date from Donations where donationID = :donationID"), {"donationID": id_to_update}).fetchall()[0][0]
            date = st.date_input("Donation Date", date_value, disabled=False)

            with engine.begin() as conn:
                amount_value = conn.execute(sa.text("select amount from Donations where donationID = :donationID"), {"donationID": id_to_update}).fetchall()[0][0]
            amount = st.text_input("Amount Donated", value = amount_value)

        update_donation_button = st.button("Update Donation", key = 'update_donation')

        if update_donation_button:

            # Checks
            everything_filled = False
            valid_name = False
            valid_contact = False
            valid_amount = False

            # Check if any of the fields are left unfilled
            if not (donor_name and contact and donor_ID and mode and amount and date):
                st.error("Please fill in all fields before submitting.")
            else:
                everything_filled = True

            # Check if the name is valid
            if all(x.isalpha() or x.isspace() for x in donor_name):
                valid_name = True
            else:
                st.error("Please enter a valid name.")

            # Check if the contact number is valid
            try:
                if len(contact) != 12 and contact[4] != '-' and all(x.isnumeric() or x == '-' for x in contact):
                    st.error("Please enter a valid contact number. (include - after 4th digit)")
                else:
                    valid_contact = True
            except:
                st.error("Please enter a valid contact number. (include - after 4th digit)")
            
            # Check if the donation ID is valid
            if amount.isnumeric() == False:
                st.error("Please enter a valid amount.")
            else:
                valid_amount = True
            
            # There shouldn't be error with date, mode and donor_ID as they are selected from the dropdowns or automatically filled.

            if everything_filled and valid_name and valid_contact and valid_amount:
                with engine.begin() as conn:
                    conn.execute(sa.text(""" 
                    update Externals
                    set name = :name, contactNum = :contact
                    where externalID = (select donorID from Donations where donationID = :donationID)

                    update Donations
                    set modeID = (select modeID from Mode where mode = :mode), amount = :amount, date = :date
                    where donationID = :donationID
                    """), {"name": donor_name, "contact": contact, "donationID": id_to_update, "mode": mode, "amount": amount, "date": date, "donationID": id_to_update})
                st.rerun()
        
        st.session_state.show_update_donation_dialog = False       
        st.caption('_:orange[Press Esc to Cancel]_') 

    @st.experimental_dialog("Delete Donation")
    def delete_donation(id_to_delete):
        st.write('Are you sure you want to delete donation of ID:', id_to_delete, '?')

        col1, col2 = st.columns(2)

        if col1.button("Yes"):
            with engine.begin() as conn:
                # we cannot actually delete any donations but rather just set it to Null and amount to 0.
                # when showing the donations we will filter out the ones with donorID = Null
                conn.execute(sa.text("update Donations set donorID = NULL, modeID = NULL, amount = 0, date = NULL where donationID = :donationID"), {"donationID": id_to_delete})
            st.rerun()
        
        if col2.button("No", key = 'no'):
            st.rerun()
        
        st.session_state.show_delete_donation_dialog = False
        st.caption('_:orange[Press Esc to Cancel]_') 
    
    # Check if the session state exists or not
    if 'show_add_donation_dialog' not in st.session_state:
        st.session_state.show_add_donation_dialog = False
    if 'show_update_donation_dialog' not in st.session_state:
        st.session_state.show_update_donation_dialog = False
    if 'show_delete_donation_dialog' not in st.session_state:
        st.session_state.show_delete_donation_dialog = False

    # Table for Donations
    with engine.begin() as conn:
        donation_table_df = pd.read_sql_query(
        sa.text("""select donationID as 'Donation ID', 
	                      name as 'Donor Name', 
	                      contactNum as 'Contact Number', 
	                      amount as 'Amount', 
	                      (select mode from Mode where Mode.modeID = Donations.modeID) as 'Mode', 
	                      date as 'Date' 
                    from Donations, Externals where Donations.donorID = Externals.externalID"""), conn)
    

    donation_table_df['Date'] = pd.to_datetime(donation_table_df['Date']).dt.strftime('%d %b %Y')

    st.write('##### :orange[Filters:]')
    dates = donation_table_df['Date'].unique()
    modes = donation_table_df['Mode'].unique()

    col1, col2 = st.columns(2)
    with col1:
        selected_date = st.selectbox("Select Date", options=["No Filters"] + list(dates), index=0, placeholder='Choose an option', key='donation_date_filter')
    with col2:
        selected_mode = st.selectbox("Select Mode", options=["No Filters"] + list(modes), index=0, placeholder='Choose an option', key='donation_mode_filter')

    # Apply filters
    if selected_date == 'No Filters':
        filtered_df = donation_table_df
    else:
        filtered_df = donation_table_df[donation_table_df['Date'] == selected_date]

    if selected_mode != "No Filters":
        filtered_df = filtered_df[filtered_df['Mode'] == selected_mode]

    st.divider()

    col1, col2, col3, col4, col5, col6 = st.columns([4.4,1,0.6,0.6,0.6,1.1])
    
    # Add a New Donation Button
    st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)
    new_donation = col6.button("✙ New Donation", on_click = add_donation_dialog)

    if st.session_state.show_add_donation_dialog:
        add_donation()

    # Display the Table
    donation_table = st.dataframe(filtered_df, width=1500, height=600, hide_index = True, on_select = "rerun", selection_mode = "single-row") 

    # Update and Delete Buttons (Only for Admin though)
    if donation_table["selection"]["rows"]: # if a row is selected
        
        row_selected = int(filtered_df.iat[donation_table['selection']['rows'][0], 0])
        # print([donation_table['selection']['rows'][0], 0])

        update_button = col4.button("Update", on_click = update_donation_dialog)
        delete_button = col5.button("Delete", on_click = delete_donation_dialog)

        if st.session_state.show_update_donation_dialog:
            update_donation(row_selected)

        if st.session_state.show_delete_donation_dialog:
            delete_donation(row_selected)

    else:
        print("No row selected")

# --------------------------------------------------------------------------------------------------------------------------- #

with Revenue:

    def add_revenue_dialog():
            st.session_state.show_add_transaction_dialog = False
            st.session_state.show_add_revenue_dialog = True
            st.session_state.show_add_donation_dialog = False  # Close donation dialog if open
            st.session_state.show_update_revenue_dialog = False
            st.session_state.show_delete_revenue_dialog = False
    
    def update_revenue_dialog():
            st.session_state.show_add_transaction_dialog = False
            st.session_state.show_add_revenue_dialog = False
            st.session_state.show_add_donation_dialog = False
            st.session_state.show_update_revenue_dialog = True
            st.session_state.show_delete_revenue_dialog = False
    
    def delete_revenue_dialog():
            st.session_state.show_add_transaction_dialog = False
            st.session_state.show_add_revenue_dialog = False
            st.session_state.show_add_donation_dialog = False
            st.session_state.show_update_revenue_dialog = False
            st.session_state.show_delete_revenue_dialog = True

    @st.experimental_dialog("Add New Revenue")
    def add_revenue():
        col1, col2 = st.columns(2)
        
        with col1:
            rev_name = st.text_input("Name", placeholder="Enter Name")

            with engine.begin() as conn:
                current_revenueid = int(pd.read_sql_query(sa.text("select top 1 revenueID from Revenue order by revenueID desc"), conn).iat[0,0]) + 1
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

            date = st.date_input("Revenue Date", datetime.datetime.now(), disabled=False)

            amount = st.text_input("Amount", value=0)

        col5, col6 = st.columns([1,0.000000000000001])

        with col5:
            remarks = st.text_area("Remarks", placeholder="Bought a collar")

        add_rev_button = st.button("✙ Add Revenue")

        if add_rev_button:

            # Checks
            everything_filled = False
            valid_name = False
            valid_contact = False
            valid_amount = False
            valid_remarks = False

            # Check if any of the fields are left unfilled
            if not (rev_name and contact and rev_ID and mode and amount and date and remarks):
                st.error("Please fill in all fields before submitting.")
            else:
                everything_filled = True

            # Check if the name is valid
            if all(x.isalpha() or x.isspace() for x in rev_name):
                valid_name = True
            else:
                st.error("Please enter a valid name.")

            # Check if the contact number is valid
            try:
                if len(contact) != 12 and contact[4] != '-' and all(x.isnumeric() or x == '-' for x in contact):
                    st.error("Please enter a valid contact number. (include - after 4th digit)")
                else:
                    valid_contact = True
            except:
                st.error("Please enter a valid contact number. (include - after 4th digit)")
            
            # Check if the revenue ID is valid
            if amount.isnumeric() == False:
                st.error("Please enter a valid amount.")
            else:
                valid_amount = True
            
            # Check if the remarks are valid
            if all(x.isalpha() or x.isspace() or x.isnumeric() for x in remarks):
                valid_remarks = True
            else:
                st.error("Please enter a valid remark.")
            
            # There shouldn't be error with date, mode and donor_ID as they are selected from the dropdowns or automatically filled.

            if everything_filled and valid_name and valid_contact and valid_amount and valid_remarks:
                with engine.begin() as conn:
                    conn.execute(sa.text(""" 
                        if not exists(select externalID from Externals where name = :name)
                            begin 
                                insert into Externals values
                                    ((select top 1 externalID from Externals order by externalID desc) + 1, 
                                    :name, :contact, Null)
                            end

                        insert into Revenue
                        values (:rev_ID, (select externalID from Externals where name = :name), (select modeID from Mode where mode = :mode), :date, :amount, :remarks)
                        """), {"name": rev_name, "name": rev_name, "contact": contact, "rev_ID": rev_ID, "name": rev_name, "mode": mode, "date": date, "amount": amount, "remarks": remarks})
                st.rerun()

        st.session_state.show_add_revenue_dialog = False
        st.caption('_:orange[Press Esc to Cancel]_')
        
    @st.experimental_dialog("Update Revenue")
    def update_revenue(id_to_update):
        col1, col2 = st.columns(2)
        
        with col1:
            with engine.begin() as conn:
                name_value = conn.execute(sa.text("select name from Externals where externalID = (select buyerID from Revenue where revenueID = :revenueID)"), {"revenueID": id_to_update}).fetchall()[0][0]
            rev_name = st.text_input("Name", placeholder="Enter Name", value = name_value)

            rev_ID = st.text_input("Revenue ID", value = id_to_update, disabled = True)

            with engine.begin() as conn:
                revenue_mode = pd.read_sql_query(sa.text("select mode from Mode"), conn)
                mode_value = conn.execute(sa.text("select mode from Mode where modeID = (select modeID from Revenue where revenueID = :revenueID)"), {"revenueID": id_to_update}).fetchall()[0][0]
                final_mode_value = 1 if mode_value == 'Cash' else 0
            mode = st.selectbox("Revenue Mode", revenue_mode["mode"].tolist(), index = final_mode_value)

        with col2:
            with engine.begin() as conn:
                contact_value = conn.execute(sa.text("select contactNum from Externals where name = :name"), {"name": name_value}).fetchall()[0][0]
            contact = st.text_input("Contact", value = contact_value, placeholder="0324-2059215")

            with engine.begin() as conn:
                date_value = conn.execute(sa.text("select date from Revenue where revenueID = :revenueID"), {"revenueID": id_to_update}).fetchall()[0][0]
            date = st.date_input("Revenue Date", date_value, disabled=False)

            with engine.begin() as conn:
                amount_value = conn.execute(sa.text("select amount from Revenue where revenueID = :revenueID"), {"revenueID": id_to_update}).fetchall()[0][0]
            amount = st.text_input("Amount", value = amount_value)

        col5, col6 = st.columns([1,0.000000000000001])

        with col5:
            with engine.begin() as conn:
                remarks_value = conn.execute(sa.text("select remarks from Revenue where revenueID = :revenueID"), {"revenueID": id_to_update}).fetchall()[0][0]
            remarks = st.text_area("Remarks", placeholder="", value = remarks_value)
        
        update_rev_button = st.button("Update Revenue", key = 'update_revenue')

        if update_rev_button:

            # Checks
            everything_filled = False
            valid_name = False
            valid_contact = False
            valid_amount = False
            valid_remarks = False

            # Check if any of the fields are left unfilled
            if not (rev_name and contact and rev_ID and mode and amount and date and remarks):
                st.error("Please fill in all fields before submitting.")
            else:
                everything_filled = True

            # Check if the name is valid
            if all(x.isalpha() or x.isspace() for x in rev_name):
                valid_name = True
            else:
                st.error("Please enter a valid name.")

            # Check if the contact number is valid
            try:
                if len(contact) != 12 and contact[4] != '-' and all(x.isnumeric() or x == '-' for x in contact):
                    st.error("Please enter a valid contact number. (include - after 4th digit)")
                else:
                    valid_contact = True
            except:
                st.error("Please enter a valid contact number. (include - after 4th digit)")
            
            # Check if the revenue ID is valid
            if amount.isnumeric() == False:
                st.error("Please enter a valid amount.")
            else:
                valid_amount = True
            
            # Check if the remarks are valid
            if all(x.isalpha() or x.isspace() or x.isnumeric() for x in remarks):
                valid_remarks = True
            else:
                st.error("Please enter a valid remark.")
            
            # There shouldn't be error with date, mode and donor_ID as they are selected from the dropdowns or automatically filled.

            if everything_filled and valid_name and valid_contact and valid_amount and valid_remarks:
                with engine.begin() as conn:
                    conn.execute(sa.text(""" 
                        update Externals
                        set name = :name, contactNum = :contact
                        where externalID = (select buyerID from Revenue where revenueID = :revenueID)

                        update Revenue
                        set modeID = (select modeID from Mode where mode = :mode), date = :date, amount = :amount, remarks = :remarks
                        where revenueID = :revenueID
                        """), {"name": rev_name, "contact": contact, "revenueID": id_to_update, "mode": mode, "date": date, "amount": amount, "remarks": remarks, "revenueID": id_to_update})
                st.rerun()
        
        st.session_state.show_update_revenue_dialog = False
        st.caption('_:orange[Press Esc to Cancel]_')
    
    @st.experimental_dialog("Delete Revenue")
    def delete_revenue(id_to_delete):
        st.write('Are you sure you want to delete revenue of ID:', id_to_delete, '?')

        col1, col2 = st.columns(2)

        if col1.button("Yes", key = 'yes_revenue_delete'):
            with engine.begin() as conn:
                # we cannot actually delete any revenue but rather just set it to Null and amount to 0.
                # when showing the revenue we will filter out the ones with buyerID = Null
                conn.execute(sa.text("update Revenue set buyerID = NULL, modeID = NULL, amount = 0, date = NULL, remarks = NULL where revenueID = :revenueID"), {"revenueID": id_to_delete})
            st.rerun()
        
        if col2.button("No", key = 'no_revenue_delete'):
            st.rerun()
        
        st.session_state.show_delete_revenue_dialog = False
        st.caption('_:orange[Press Esc to Cancel]_') 

    # Check if the session state exists or not
    if 'show_add_revenue_dialog' not in st.session_state:
        st.session_state.show_add_revenue_dialog = False
    if 'show_update_revenue_dialog' not in st.session_state:
        st.session_state.show_update_revenue_dialog = False
    if 'show_delete_revenue_dialog' not in st.session_state:
        st.session_state.show_delete_revenue_dialog = False

    # Table for Revenue
    with engine.begin() as conn:
        revenue_table_df = pd.read_sql_query(sa.text("""
        select revenueID as 'Revenue ID', 
        name as 'Name', 
        contactNum as 'Contact Number', 
        amount as 'Amount', 
        (select mode from Mode where Mode.modeID = Revenue.modeID) as 'Mode', 
        remarks as 'Remark',
        date as 'Date' 
        from Revenue, Externals where Revenue.buyerID = Externals.externalID"""), conn)
    
    revenue_table_df['Date'] = pd.to_datetime(revenue_table_df['Date']).dt.strftime('%d %b %Y')

    # Filtering and Final Table
    st.write('##### :orange[Filters:]')
    dates = revenue_table_df['Date'].unique()
    modes = revenue_table_df['Mode'].unique()

    col1, col2 = st.columns(2)

    with col1:
        selected_date = st.selectbox("Select Date", options=["No Filters"] + list(dates), index=0, placeholder='Choose a Date')

    with col2:
        selected_mode = st.selectbox("Select Mode", options=["No Filters"] + list(modes), index=0, placeholder='Choose a Mode')

    # Apply filters
    if selected_date == 'No Filters':
        filtered_df = revenue_table_df
    else:
        filtered_df = revenue_table_df[revenue_table_df['Date'] == selected_date]

    if selected_mode!='No Filters':
        filtered_df = filtered_df[filtered_df['Mode'] == selected_mode]

    st.divider()

    col1, col2, col3, col4, col5, col6 = st.columns([4.4,1,0.6,0.6,0.6,1.1])
    
    # Add a New Revenue Button
    st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)
    new_revenue = col6.button("✙ New Revenue", on_click=add_revenue_dialog, key = "add_revenue")

    if st.session_state.show_add_revenue_dialog:
        add_revenue()
    
    # Display the Table
    revenue_table = st.dataframe(filtered_df, width=1500, height=600, hide_index=True, on_select="rerun", selection_mode="single-row")

    # Update and Delete Buttons (Only for Admin though)
    if revenue_table["selection"]["rows"]: # if a row is selected

        row_selected = int(filtered_df.iat[revenue_table['selection']['rows'][0], 0])

        update_button = col4.button("Update", on_click = update_revenue_dialog, key = 'update_revenue')
        delete_button = col5.button("Delete", on_click = delete_revenue_dialog, key = 'delete_revenue')

        if st.session_state.show_update_revenue_dialog:
            update_revenue(row_selected)
        
        if st.session_state.show_delete_revenue_dialog:
            delete_revenue(row_selected)

    else:
        print("No row selected")

# ----------------------------------------------------------------------------------------------------------------------------- #

with Transactions:

    def add_transaction_dialog():
        st.session_state.show_add_transaction_dialog = True #only transaction will be open
        st.session_state.show_add_revenue_dialog = False #close revenue dialgog if open
        st.session_state.show_add_donation_dialog = False  # Close donation dialog if open
        st.session_state.show_update_transaction_dialog = False
        st.session_state.show_delete_transaction_dialog = False
    
    def update_transaction_dialog():
        st.session_state.show_add_transaction_dialog = False
        st.session_state.show_add_revenue_dialog = False
        st.session_state.show_add_donation_dialog = False
        st.session_state.show_update_transaction_dialog = True
        st.session_state.show_delete_transaction_dialog = False

    def delete_transaction_dialog():
        st.session_state.show_add_transaction_dialog = False
        st.session_state.show_add_revenue_dialog = False
        st.session_state.show_add_donation_dialog = False
        st.session_state.show_update_transaction_dialog = False
        st.session_state.show_delete_transaction_dialog = True

    @st.experimental_dialog("Add New Transaction")
    def add_transaction():

        col1, col2 = st.columns([1,0.000000000000001])

        with col1:
            billFor = st.text_area("Bill For", placeholder="Enter bill for")

        col3, col4 = st.columns(2)
        
        with col3:
            with engine.begin() as conn:
                trans_mode = pd.read_sql_query(sa.text("select mode from Mode"), conn)
                current_transid = int(pd.read_sql_query(sa.text("select top 1 transactionID from Transactions order by transactionID desc"), conn).iat[0,0]) + 1
            mode = st.selectbox("Transaction Mode", trans_mode["mode"].tolist())
            trans_ID = st.text_input("Transaction ID", value = current_transid, disabled = True)
        
        with col4:
            amount = st.text_input("Amount", value=0)
            date = st.date_input("Transaction Date", datetime.datetime.now(), disabled=True)
        
        col5, col6 = st.columns([1,0.000000000000001])
        with col5:
            remarks = st.text_area("Remarks", placeholder="")

        add_tran_button = st.button("Add New Transaction")

        if add_tran_button:

            # Checks
            everything_filled = False
            valid_billFor = False
            valid_amount = False
            valid_remarks = False

            # Check if any of the fields are left unfilled
            if not (billFor and trans_ID and mode and amount and date and remarks):
                st.error("Please fill in all fields before submitting.")
            else:
                everything_filled = True
            
            # Check if the billFor is valid
            if all(x.isalpha() or x.isspace() or x.isnumeric() for x in billFor):
                valid_billFor = True
            else:
                st.error("Please enter a valid bill for.")
            
            # Check if the amount is valid
            if amount.isnumeric() == False:
                st.error("Please enter a valid amount.")
            else:
                valid_amount = True
            
            # Check if the remarks are valid
            if all(x.isalpha() or x.isspace() or x.isnumeric() for x in remarks):
                valid_remarks = True
            else:
                st.error("Please enter a valid remark.")
            
            # There shouldn't be error with date, mode and trans_ID as they are selected from the dropdowns or automatically filled.

            if everything_filled and valid_billFor and valid_amount and valid_remarks:
                with engine.begin() as conn:
                    conn.execute(sa.text(""" 
                                        insert into Transactions
                                        values (:trans_ID, (select modeID from Mode where mode = :mode), :amount, :billFor, :date, :remarks)
                                        """), {"trans_ID":trans_ID, "mode": mode, "amount": amount, "billFor": billFor, "date": date, "remarks": remarks})
                st.rerun()
        
        st.session_state.show_add_transaction_dialog = False
        st.caption('_:orange[Press Esc to Cancel]_')
    
    @st.experimental_dialog("Update Transaction")
    def update_transaction(id_to_update):

        col1, col2 = st.columns([1,0.000000000000001])
        
        with col1:
            with engine.begin() as conn:
                billFor_value = conn.execute(sa.text("select billFor from Transactions where transactionID = :transactionID"), {"transactionID": id_to_update}).fetchall()[0][0]
            billFor = st.text_area("Bill For", placeholder="Enter bill for", value = billFor_value)

        col3, col4 = st.columns(2)

        with col3:
            with engine.begin() as conn:
                trans_mode = pd.read_sql_query(sa.text("select mode from Mode"), conn)
                mode_value = conn.execute(sa.text("select mode from Mode where modeID = (select modeID from Transactions where transactionID = :transactionID)"), {"transactionID": id_to_update}).fetchall()[0][0]
            final_mode_value = 1 if mode_value == 'Cash' else 0
            mode = st.selectbox("Transaction Mode", trans_mode["mode"].tolist(), index = final_mode_value)
            trans_ID = st.text_input("Transaction ID", value = id_to_update, disabled = True)
        
        with col4:
            with engine.begin() as conn:
                amount_value = conn.execute(sa.text("select amount from Transactions where transactionID = :transactionID"), {"transactionID": id_to_update}).fetchall()[0][0]
                date_value = conn.execute(sa.text("select date from Transactions where transactionID = :transactionID"), {"transactionID": id_to_update}).fetchall()[0][0]
            amount = st.text_input("Amount", value = amount_value)
            date = st.date_input("Transaction Date", date_value, disabled=False)
        
        col5, col6 = st.columns([1,0.000000000000001])

        with col5:
            with engine.begin() as conn:
                remarks_value = conn.execute(sa.text("select remarks from Transactions where transactionID = :transactionID"), {"transactionID": id_to_update}).fetchall()[0][0]
            remarks = st.text_area("Remarks", placeholder="", value = remarks_value)

        update_tran_button = st.button("Update Transaction", key = 'update_transaction')

        if update_tran_button:
            
            # Checks
            everything_filled = False
            valid_billFor = False
            valid_amount = False
            valid_remarks = False

            # Check if any of the fields are left unfilled
            if not (billFor and trans_ID and mode and amount and date and remarks):
                st.error("Please fill in all fields before submitting.")
            else:
                everything_filled = True
            
            # Check if the billFor is valid
            if all(x.isalpha() or x.isspace() or x.isnumeric() for x in billFor):
                valid_billFor = True
            else:
                st.error("Please enter a valid bill for.")
            
            # Check if the amount is valid
            if amount.isnumeric() == False:
                st.error("Please enter a valid amount.")
            else:
                valid_amount = True
            
            # Check if the remarks are valid
            if all(x.isalpha() or x.isspace() or x.isnumeric() for x in remarks):
                valid_remarks = True
            else:
                st.error("Please enter a valid remark.")
            
            # There shouldn't be error with date, mode and trans_ID as they are selected from the dropdowns or automatically filled.

            if everything_filled and valid_billFor and valid_amount and valid_remarks:
                with engine.begin() as conn:
                    conn.execute(sa.text(""" 
                    update Transactions
                    set modeID = (select modeID from Mode where mode = :mode), amount = :amount, billFor = :billFor, date = :date, remarks = :remarks
                    where transactionID = :transactionID
                    """), {"mode": mode, "amount": amount, "billFor": billFor, "date": date, "remarks": remarks, "transactionID": id_to_update})
                st.rerun()
        
        st.session_state.show_update_transaction_dialog = False
        st.caption('_:orange[Press Esc to Cancel]_')
    
    @st.experimental_dialog("Delete Transaction")
    def delete_transaction(id_to_delete):
        st.write('Are you sure you want to delete transaction of ID:', id_to_delete, '?')

        col1, col2 = st.columns(2)

        if col1.button("Yes", key = 'yes_transaction_delete'):
            with engine.begin() as conn:
                # we cannot actually delete any transactions but rather just set it to Null and amount to 0.
                # when showing the transactions we will filter out the ones with transactionID = Null
                conn.execute(sa.text("update Transactions set modeID = NULL, amount = 0, billFor = NULL, date = NULL, remarks = NULL where transactionID = :transactionID"), {"transactionID": id_to_delete})
            st.rerun()
        
        if col2.button("No", key = 'no_transaction_delete'):
            st.rerun()
        
        st.session_state.show_delete_transaction_dialog = False
        st.caption('_:orange[Press Esc to Cancel]_') 
    
    # Check if the session state exists or not
    if 'show_add_transaction_dialog' not in st.session_state:
        st.session_state.show_add_transaction_dialog = False
    if 'show_update_transaction_dialog' not in st.session_state:
        st.session_state.show_update_transaction_dialog = False
    if 'show_delete_transaction_dialog' not in st.session_state:
        st.session_state.show_delete_transaction_dialog = False

    # Table for Transactions
    with engine.begin() as conn:
        transaction_table_df = pd.read_sql_query(sa.text("""
                        select transactionID as 'Transaction ID', billFor as 'Bill For', amount as 'Amount', 
                        (select mode from Mode where Mode.modeID = Transactions.modeID) as 'Mode', remarks as 'Remarks', date as 'Date' from Transactions where modeID is not NULL"""), conn)
        

    transaction_table_df['Date'] = pd.to_datetime(transaction_table_df['Date']).dt.strftime('%d %b %Y')

    
    # Filtering and Final Table
    st.write('##### :orange[Filters:]')
    dates2 = transaction_table_df['Date'].unique()
    modes2 = transaction_table_df['Mode'].unique()

    col1, col2 = st.columns(2)
    with col1:
        selected_date2 = st.selectbox("Select Date", options=["No Filters"] + list(dates2), index=0, placeholder='Choose a Date', key='date_filter')
    with col2:
        selected_mode2 = st.selectbox("Select Mode", options=["No Filters"] + list(modes2), index=0, placeholder='Choose a Mode', key='mode_filter')

    if selected_date2 =='No Filters':
        filtered_df = transaction_table_df
    else:
        filtered_df = transaction_table_df[transaction_table_df['Date'] == selected_date2]

    if selected_mode2 != 'No Filters':
        filtered_df = filtered_df[filtered_df['Mode'] == selected_mode2]

    st.divider()
    
    col1, col2, col3, col4, col5, col6 = st.columns([4.4,1,0.6,0.6,0.6,1.15])

    # Add a New Transaction Button
    st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)
    new_transaction = col6.button("✙ New Transaction", on_click=add_transaction_dialog , key = "add_transaction")

    if st.session_state.show_add_transaction_dialog:
        add_transaction()
    
    # Display the Table
    transaction_table = st.dataframe(filtered_df, width=1500, height=600, hide_index=True, on_select="rerun", selection_mode="single-row") 

    # Update and Delete Buttons (Only for Admin though)
    if transaction_table["selection"]["rows"]: # if a row is selected

        row_selected = int(filtered_df.iat[transaction_table['selection']['rows'][0], 0])

        update_button = col4.button("Update", on_click = update_transaction_dialog, key = 'update_trans')
        delete_button = col5.button("Delete", on_click = delete_transaction_dialog, key = 'delete_trans')

        if st.session_state.show_update_transaction_dialog:
            update_transaction(row_selected)

        if st.session_state.show_delete_transaction_dialog:
            delete_transaction(row_selected)

    else:
        print("No row selected")

with open('../config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

name, logged_in, user_name = authenticator.login()

st.sidebar.write(f"Logged in as: _:orange[{name}]_")

if name is not None:
    with engine.connect() as conn:
        role = conn.execute(sa.text("select roleDesc from InternalRole, Users where Users.internalRoleID = InternalRole.internalRoleID and Users.userName = :name"), {"name":name}).fetchone()[0]        
    st.sidebar.write(f"Role: _:orange[{role}]_")
else:
    st.switch_page("LoginScreen.py")

if st.sidebar.button("🔓 Logout"):
    with st.sidebar:
        with st.spinner('Logging out...'):
            time.sleep(2)

    authenticator.logout(location = "unrendered")
    st.switch_page("LoginScreen.py")