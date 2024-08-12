# standard imports
import datetime
from PIL import Image
import time

# third party imports
import pandas as pd
import streamlit as st
import sqlalchemy as sa

#cusotm imports
from millify import prettify
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

#custome streamlit imports
from st_pages import Page, show_pages, add_page_title, hide_pages

# streamlit-authenticator package
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# database information ; will change when db hosting
# server = 'DESKTOP-67BT6TD\\FONTAINE' # IBAD
# server = 'DESKTOP-HT3NB74' # EMAN
server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA

database = 'DummyPawRescue'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

st.set_page_config(page_title="Cats", page_icon="🐈", layout="wide", initial_sidebar_state="expanded")

# Logo
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

# Sidebar better
st.sidebar.markdown(""" <style> [data-testid='stSidebarNav'] > ul { min-height: 54vh; } </style> """, unsafe_allow_html=True) 

hide_pages(["Login"])

#Creating columns for better formatting
col1, col2, col3, col4 = st.columns(4)

#Title
st.header("Cats", divider = "orange")

#Functions
def add_cat_dialog():
    st.session_state.show_add_cat_dialog = True
    st.session_state.show_view_cat_dialog = False
    st.session_state.update_cat_dialog = False
    # st.session_state.delete_cat_dialog = False

def view_cat_dialog():
    st.session_state.show_add_cat_dialog = False
    st.session_state.show_view_cat_dialog = True
    st.session_state.show_update_cat_dialog = False
    # st.session_state.show_delete_cat_dialog = False

def update_cat_dialog():
    st.session_state.show_add_cat_dialog = False
    st.session_state.show_view_cat_dialog = False
    st.session_state.show_update_cat_dialog = True
    # st.session_state.show_delete_cat_dialog = False

# Load custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Function to format contact number
def format_contact_number(contact):
    if '-' in contact:
        return contact
    return contact[:4] + '-' + contact[4:] if len(contact) > 4 else contact

#Funciton to extract number from cat id
def extract_cat_number(cat_id_str):
    # Remove the prefix "PA-"
    numberStr = cat_id_str.replace("PR-", "")
    
    # Convert to integer
    numberInt = int(numberStr)
    
    return numberInt

# ADD DIALOG
catCodestr = ''
@st.experimental_dialog("Add a New Cat")
def add_cat():

    #cats info (in the form)
    st.write(" :orange[Cat related details]")

    # Creating columns for better formatting 
    col1, col2 = st.columns(2)

    with col1:
        
        #Cat ID Field
        with engine.begin()as conn:
            currentCatID = int(pd.read_sql_query(sa.text("select top 1 catID from Cats order by catID desc"), conn).iat[0,0]) + 1
            #TODO:
            catCodestr = "PR-" + str(currentCatID).zfill(5) # catCodestr = "PA-000" + str(currentCatID) #need to fix this logic , explore prettify
        st.text_input("Cat ID", value = catCodestr, disabled= True)

        # Age field
        age = st.number_input("Age (in years)", step=0.1, value=0.0)

        # Type field
        with engine.begin() as conn:
            typeSelection = pd.read_sql_query(sa.text("SELECT type FROM Type"), conn)
        type = st.selectbox("Type", typeSelection["type"].tolist())

    with col2:
        # Name field
        name = st.text_input("Cat Name", placeholder="Enter Cat's Name")

        # Gender field
        with engine.begin() as conn:
            genderSelection = pd.read_sql_query(sa.text("SELECT gender FROM Gender"), conn)
        gender = st.selectbox("Gender", genderSelection["gender"].tolist())

        # Cage no field
        with engine.begin() as conn:
            cage_code_id_df = pd.read_sql_query(sa.text("select cage.cageID, code,cageNo from ward, cage where ward.wardID = cage.wardID and cageStatusID = 2"), conn)
        
        cage_code_id_df["cagecodeID"] = cage_code_id_df.apply(lambda row: f"{row['code']}-C-{str(row['cageNo']).zfill(2)}", axis=1)
        cageID_list = cage_code_id_df["cagecodeID"].tolist()

        cageNum = st.selectbox("Cage Number", cageID_list)  # This should also show which Ward it is in and that Cage is free or not ofc.
        cageID = int(cage_code_id_df.iat[cageID_list.index(cageNum),0])
        
    with engine.begin() as conn:
        statusSelection = pd.read_sql_query(sa.text("SELECT statusType FROM CatStatus"), conn)
    status = st.selectbox("Status", statusSelection["statusType"].tolist())

    # Date
    date = st.date_input('Date', value=datetime.date.today(), disabled=False)

    # Owner related info (in the form)
    st.write(" :orange[Owner related details]")

    col1, col2 = st.columns(2)  # redefining to enter owner related details after cat details

    with col1:
        # Owner name text input
        ownerName = st.text_input("Owner's Name", placeholder="Enter Owner's Name")

    with col2:
        contactFromDB = ''
        if ownerName:
            with engine.begin() as conn:
                fetchall = conn.execute(sa.text("SELECT contactNum FROM Externals WHERE name = :name"), {"name": ownerName}).fetchall()
                if fetchall:
                    contactFromDB = fetchall[0][0]

        # Owner contact text input
        # contactFromDB = format_contact_number(contactFromDB)
        ownerContact = st.text_input("Owner's Contact", value=contactFromDB, placeholder="0300-7413639")

    # Address text area
    addressFromDB = ''
    if ownerName:
        with engine.begin() as conn:
            fetchall = conn.execute(sa.text("Select address from externals where name = :name"), {"name": ownerName}).fetchall()
            if fetchall:
                addressFromDB = fetchall[0][0]
    address = st.text_area("Address", value = addressFromDB , placeholder = "Enter your address" )

    # Submit and Cancel buttons
    st.caption(':orange[Press Esc to Cancel]')

    # Logic for inserting the data
    if st.button("Add"):
       
        # Checks
        everythingFilled = False
        valid_catname = False
        valid_age = False
        valid_ownername = False
        valid_contact = False
        valid_address = False

        # Check if any of the fields are left unfilled
        if not (age and type and name and gender and cageID and status and ownerName and ownerContact and address):
            st.error("Please fill in all the fields before submitting.")
            print("Please fill in all the fields.")
        else:
            everythingFilled = True

        if all(x.isalpha() or x.isspace() for x in name):
                valid_catname = True
        else:
            st.error("Please enter a valid cat name.")

        if age>0:
            valid_age = True
        else:
            st.error("Please enter a valid age for the cat.")

        if all(x.isalpha() or x.isspace() for x in ownerName):
                valid_ownername = True
        else:
            st.error("Please enter a valid Owner name.")

        if len(ownerContact)>0 and len(ownerContact)<12 and ownerContact.isnumeric:
            valid_contact = True
        else:
            st.error("Please enter a valid contact number.")

        if all(x.isalpha() or x.isspace() or x.isnumeric() for x in address):
                valid_address = True
        else:
            st.error("Please enter a valid address.")

        if (everythingFilled and valid_catname and valid_age and valid_ownername and valid_contact and valid_address):
            with engine.begin() as conn:
                conn.execute(sa.text(""" 
                IF NOT EXISTS (SELECT externalID FROM Externals WHERE name = :name)
                BEGIN
                    INSERT INTO Externals
                    VALUES
                    ((SELECT COALESCE(MAX(externalID), 0) + 1 FROM Externals), :name, :contactNum, :address)
                END

                INSERT INTO Cats (catID, catName, age, genderID, typeID, cageID, externalID, statusID, admittedOn)
                VALUES
                (:catID, :catName, :age, 
                (SELECT genderID FROM Gender WHERE gender = :gender),
                (SELECT typeID FROM Type WHERE type = :type), 
                :cageID, 
                (SELECT externalID FROM Externals WHERE name = :name), 
                (SELECT statusID FROM CatStatus WHERE statusType = :status), 
                :admittedOn)
                                     
                update cage set cageStatusID = 1 where cageID = :cageID -- updating the cage status as well while adding the cat
                                     """),
                {
                    "catID": currentCatID, "catName": name, "age": age, "gender": gender, 
                    "type": type, "cageID": cageID, "name": ownerName, 
                    "contactNum": ownerContact, "address": address, 
                    "status": status, "admittedOn": date
                })

            with st.spinner('Adding...'): # is this really necessary? lmao
                time.sleep(2)

            container = st.empty()
            container.success(f"Cat ID: {catCodestr} has been added successfully") # Create a success alert
            time.sleep(2)  # Wait  4seconds
            container.empty()  # Clear the success alert

            st.rerun()
            
    st.session_state.show_add_cat_dialog = False

#UPDATE DIALOG
@st.experimental_dialog("Update Cat Details")
def update_cat(id):
    
    #cats info (in the form)
    st.write(" :orange[Cat related details]")

    # Creating columns for better formatting 
    col1, col2 = st.columns(2)

    if cat_table["selection"]["rows"]: #if a row is selected
            # selectedID = cat_table_df.iat[cat_table["selection"]["rows"][0],0]
            selectedCatName = filtered_df.iat[cat_table["selection"]["rows"][0],1]
            old_cageCode = filtered_df.iat[cat_table["selection"]["rows"][0],6]
            selectedStatus = filtered_df.iat[cat_table["selection"]["rows"][0],7]
            selectedOwnerName = filtered_df.iat[cat_table["selection"]["rows"][0],2]
            selectedOwnerContact = filtered_df.iat[cat_table["selection"]["rows"][0],3]
            selectedDate = filtered_df.iat[cat_table["selection"]["rows"][0],4]
            selectedType = filtered_df.iat[cat_table["selection"]["rows"][0],5]

    with col1:
        
        # Cat ID Field
        catID = st.text_input("Cat ID", value = id, disabled=True) # disable if id should not be editable
        
        # Age field
        with engine.begin() as conn:
            ageValue= conn.execute(sa.text("Select age from cats where catID = :catID") ,{"catID": extract_cat_number(id)}).fetchall()[0][0]
        age = st.number_input("Age (in years)", step = 0.1, value = float(ageValue))

        # Type field
        with engine.begin() as conn:
            type_list = pd.read_sql_query(sa.text("SELECT type FROM Type"), conn)
            type_value = pd.read_sql_query(sa.text("SELECT type FROM Type where typeID in (select typeID from cats where catID = :catID)"), conn, params = {"catID": extract_cat_number(id)}).iat[0,0]
        type_df = type_list["type"].tolist()
        final_type_index = type_df.index(type_value)
        type = st.selectbox("Type", type_df, index = final_type_index)

    with col2:

        # Cat name field
        name = st.text_input("Cat Name", value = selectedCatName)

        # Gender field
        with engine.begin() as conn:
            gender_list = pd.read_sql_query(sa.text("SELECT gender FROM Gender"), conn)
            gender_value = pd.read_sql_query(sa.text(""" SELECT gender from gender where genderID in (select genderID from cats where catID = :catID)"""), conn, params = {"catID": extract_cat_number(id)}).iat[0,0]
        gender_df = gender_list["gender"].tolist()
        final_gender_index = gender_df.index(gender_value)
        gender = st.selectbox("Gender", gender_df, index = final_gender_index)

        # Cage no field
        with engine.begin() as conn:
            cage_code_id_df = pd.read_sql_query(sa.text("select cage.cageID, code,cageNo from ward, cage where ward.wardID = cage.wardID and cageStatusID = 2"), conn)
            selected_cage_id_df = pd.read_sql_query(sa.text("select cageID from cage where cageID in (select cageID from cats where catID = :catID)"), conn, params = {"catID": extract_cat_number(id)})

        old_cageID = int(selected_cage_id_df.iat[0,0])
        cage_code_id_df["cagecodeID"] = cage_code_id_df.apply(lambda row: f"{row['code']}-C-{str(row['cageNo']).zfill(2)}", axis=1)
        cage_code_id_df = cage_code_id_df._append({"cagecodeID": old_cageCode, "cageID": old_cageID}, ignore_index = True)
        cageID_list = cage_code_id_df["cagecodeID"].tolist()

        cageCode = st.selectbox("Cage Number", cageID_list, index=cageID_list.index(old_cageCode))
        cageID = int(cage_code_id_df.iat[cageID_list.index(cageCode),0])

    with engine.begin() as conn:
        status_list = pd.read_sql_query(sa.text("SELECT statusType FROM CatStatus"), conn)
        status_value = pd.read_sql_query(sa.text("SELECT statusType from catstatus where statusID in (select statusID from cats where catID = :catID)"), conn, params = {"catID": extract_cat_number(id)}).iat[0,0]
    status_df = status_list['statusType'].tolist()
    final_status_index = status_df.index(status_value)
    status = st.selectbox("Status", status_df, index = final_status_index)

    # Date
    with engine.begin() as conn:
        datefromDB = conn.execute(sa.text("Select admittedOn from cats where catID = :catID"), {"catID": extract_cat_number(id)}).fetchone()[0]
    date = st.date_input('Date', value=datefromDB, disabled=False)

    # Owner related info (in the form)
    st.write(" :orange[Owner related details]")

    col1, col2 = st.columns(2)  # redefining to enter owner related details after cat details

    with col1:
        # Name field
        with engine.begin() as conn:
            ownerNameValue = conn.execute(sa.text("Select name from Externals where externalID = (select externalID from cats where catID = :catID)"), {"catID": extract_cat_number(id)}).fetchall()[0][0]
        ownerName = st.text_input("Owner/Reporter's Name",  value = ownerNameValue)
    
    with col2:
        contactFromDB = ''
        if ownerName:
            with engine.begin() as conn:
                fetchall = conn.execute(sa.text("SELECT contactNum FROM Externals WHERE name = :name"), {"name": ownerName}).fetchall()
                if fetchall:
                    contactFromDB = fetchall[0][0]
        ownerContact = st.text_input("Owner's Contact", value=contactFromDB)

    # Address text area
    addressFromDB = ''
    if ownerName:
        with engine.begin() as conn:
            fetchall = conn.execute(sa.text("Select address from externals where name = :name"), {"name": ownerName}).fetchall()
            if fetchall:
                addressFromDB = fetchall[0][0]
    address = st.text_area("Address", value = addressFromDB , placeholder = "Enter your address" )

    if st.button("Update"):
        #checks
        everythingFilled = False
        valid_catname = False
        valid_age = False
        valid_ownername = False
        valid_contact = False
        valid_address = False

        # Check if any of the fields are left unfilled
        if not (age and type and name and gender and cageID and status and ownerName and ownerContact and address):
            st.error("Please fill in all the fields before submitting.")
            print("Please fill in all the fields.")
        else:
            everythingFilled = True

        if all(x.isalpha() or x.isspace() for x in name):
                valid_catname = True
        else:
            st.error("Please enter a valid cat name.")

        if age>0:
            valid_age = True
        else:
            st.error("Please enter a valid age for the cat.")

        if all(x.isalpha() or x.isspace() for x in ownerName):
                valid_ownername = True
        else:
            st.error("Please enter a valid Owner name.")

        if len(ownerContact)>0 and len(ownerContact)<12 and ownerContact.isnumeric:
            valid_contact = True
        else:
            st.error("Please enter a valid contact number.")

        if all(x.isalpha() or x.isspace() or x.isnumeric() for x in address):
                valid_address = True
        else:
            st.error("Please enter a valid address.")

        if (everythingFilled and valid_catname and valid_age and valid_contact and valid_ownername and valid_address):

            # query to update the cat details
            with engine.begin() as conn:
                conn.execute(sa.text(""" 
                                     
                update Externals
                set name = :name, contactNum = :contact, address = :address
                where externalID = (select externalID from Cats where catID = :catID)
                                    
                update cats
                set 
                catName = :catName, 
                age = :age, 
                genderID = (SELECT genderID FROM Gender WHERE gender = :gender), 
                typeID = (SELECT typeID FROM Type WHERE type = :type),
                cageID = :new_cageID,
                statusID = (SELECT statusID FROM CatStatus WHERE statusType = :status),
                admittedOn = :date
                where catID = :catID

                update cage set cageStatusID = 2 where cageID = :old_cageID                      
                
                update cage set cageStatusID = 1 where cageID = :new_cageID
                                     
                                     """), {"name": ownerName, 
                                            "contact": ownerContact,
                                            "address": address,
                                            "catID": extract_cat_number(id), 
                                            "catName": name, 
                                            "age": age, 
                                            "gender": gender,
                                            "type": type,
                                            "new_cageID": cageID,
                                            "status": status,
                                            "date": date,
                                            "old_cageID": old_cageID
                                            })

            container = st.empty()
            container.success(f"Cat ID: {catCodestr} has been updated successfully") # Create a success alert
            time.sleep(2)  # Wait  4seconds
            container.empty()  # Clear the success alert

            st.rerun()
    
    st.caption(':orange[Press Esc to Cancel]')
    st.session_state.show_update_cat_dialog = False

#DELETE
@st.experimental_dialog("Delete Cat Details")
def delete_cat(id):
    st.warning("Are you sure you want to delete cat ID: "+ str(id)+ " ?", icon = "⚠️")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    yes = col3.button("Yes")
    no = col4.button("No")
    # have to delete from treatments too to maintain referential integrity
    if yes:
        with engine.begin() as conn:
            conn.execute(sa.text("update cats set catName = NULL,  age = NULL, genderID = NULL, typeID = NULL, cageID = NULL, externalID = NULL, statusID = NULL, admittedOn = NULL where catID = :catID"),  {"catID" :  extract_cat_number(id)})
            # conn.execute(sa.text("update Cage set cageStatusID = 2 where catID = :catID"), {"catID" :  extract_cat_number(id)})
            # conn.execute(sa.text("update treatment set catID = Null, dateTime = NULL, temperature = NULL, treatment = NULL where catID = :catID"),  {"catID" : extract_cat_number(id)})
            
            with st.spinner('Deleting...'):
                time.sleep(2)
            # st.success(f"Cat ID: {id} has been deleted successfully")
            container = st.empty()
            container.success(f"Cat ID: {id} has been deleted successfully") # Create a success alert
            time.sleep(4)  # Wait  4seconds
            container.empty()  # Clear the success alert
        st.rerun()

    if no:
        st.session_state.show_delete_cat_dialog = False
        st.rerun()

    st.caption('_:orange[Press Esc to Cancel]_') 
    st.session_state.show_delete_cat_dialog = False
    
#VIEW CAT DETAILS
@st.experimental_dialog("View Cat's Details")
def view_cat(id):
    
    st.write("## :orange[ **Cat ID :**]" , id)
    # Gathering data
    with engine.begin() as conn:
        ageDB = conn.execute(sa.text("Select age from cats where catID = :catID") ,{"catID": extract_cat_number(id)}).fetchall()[0]
        genderDB = conn.execute(sa.text("Select genderID from cats where catID = :catID") ,{"catID": extract_cat_number(id)}).fetchall()[0]
        addressDB = conn.execute(sa.text("select address from Externals where externalID in (select externalID from cats where catID = :catID)") ,{"catID": extract_cat_number(id)}).fetchall()[0]

    if cat_table["selection"]["rows"]: #if a row is selected
            # selectedID = cat_table_df.iat[cat_table["selection"]["rows"][0],0]
            # print("selected cat id:", selectedID)
            selectedCatName = filtered_df.iat[cat_table["selection"]["rows"][0],1]
            # print("selected cat name:", selectedCatName)
            selectedCage = filtered_df.iat[cat_table["selection"]["rows"][0],6]
            # print("selected age:", selectedCage)
            selectedStatus = filtered_df.iat[cat_table["selection"]["rows"][0],7]
            # print("selected status:", selectedStatus)
            selectedOwnerName = filtered_df.iat[cat_table["selection"]["rows"][0],2]
            # print("selected owner name:", selectedOwnerName)
            selectedOwnerContact = filtered_df.iat[cat_table["selection"]["rows"][0],3]
            # print("selected owner contact:", selectedOwnerContact)
            selectedDate = filtered_df.iat[cat_table["selection"]["rows"][0],4]
            # print("selected date:", selectedDate)
            selectedType = filtered_df.iat[cat_table["selection"]["rows"][0],5]
            # print("selected type:", selectedType)

    general_info, owner_info, treatment_info = st.tabs([":orange[General Information]", ":orange[Owner/Reporter's Details]", ":orange[Treatment related Details]"])

    # Tabs
    with general_info:
        with st.container(border= True):
            col1, col2 = st.columns(2)

            with col1:
                st.text_input("***Name:***", value = selectedCatName, disabled= True)
                st.text_input("***Admitted On:***", value = selectedDate, disabled= True)
                st.text_input("***Age:***", value = str(ageDB[0]) + " yr(s)", disabled= True)
            # st.write("***Name:***",selectedCatName )
            
            with col2:
                st.text_input("***Cage ID:***", selectedCage, disabled= True)
            # st.write("***Cage ID:***", selectedCage)
            # st.write("***Admitted On:***",selectedDate)

                if str(int(genderDB[0])) == "1":
                    # st.write("***Gender:***", "Male")
                    st.text_input("***Gender:***", value = "Male", disabled= True)

                elif str(int(genderDB[0])) == "2":
                    # st.write("***Gender:***", "Female")
                    st.text_input("***Gender:***", value = "Female", disabled= True)

                st.text_input("***Status:***", value = selectedStatus, disabled= True)
            # st.write("***Age:***", str(ageDB[0]), "yr(s)")
            # st.write("***Status:***",selectedStatus)

    with owner_info:
        with st.container( border = True):
            col1, col2 = st.columns(2)

            with col1:
                
                st.text_input("***Name:***", value = selectedOwnerName, disabled= True)
                st.text_input("***Address:***", value = str(addressDB[0]), disabled= True)

            with col2:
                st.text_input("***Contact Number:***", value = selectedOwnerContact, disabled= True)
                st.text_input("***Pet Type:***", value = selectedType, disabled= True)
                # st.write("***Name:***", selectedOwnerName)
                # st.write("***Contact Number:***", selectedOwnerContact)
                # st.write("***Address:***", str(addressDB[0]))
                # st.write("***Pet Type:***", selectedType)
        
    with treatment_info:
        with st.container( border = True):
            
            # Define the SQL query with a parameter placeholder
            query = """
            SELECT dateTime AS 'Date/Time', 
                temperature AS 'Temp', 
                treatment AS 'Treatment', 
                users.userName AS 'Given by'
            FROM treatment
            JOIN cats ON treatment.catID = cats.catID
            JOIN users ON treatment.userID = users.userID
            WHERE treatment.catID = :catID
            """

            # Execute the query and fetch the results into a DataFrame
            with engine.begin() as conn:
                treatment_table_df = pd.read_sql_query(sa.text(query), conn, params={"catID": extract_cat_number(id)})

            treatment_table_df["Date/Time"] =pd.to_datetime(treatment_table_df["Date/Time"]).dt.strftime('%d %b %Y, %I:%M %p')

            st.dataframe(treatment_table_df, width = 600, height = 110, hide_index = True)

        st.session_state.show_view_cat_dialog = False

# ------------------------------------------------------------ #

# Check if the session state exists or not
if 'show_add_cat_dialog' not in st.session_state:
    st.session_state.show_add_cat_dialog = False
if 'show_add_cat_dialog' not in st.session_state:
    st.session_state.show_add_cat_dialog = False
if 'show_view_cat_dialog' not in st.session_state:
    st.session_state.show_view_cat_dialog = False
if 'show_update_cat_dialog' not in st.session_state:
    st.session_state.show_update_cat_dialog = False

if st.session_state.show_add_cat_dialog:
    add_cat()

# Table for Cats:
with engine.begin() as conn:
    cat_table_df = pd.read_sql_query(sa.text(""" 
                        select catID as 'Cat ID', catName as 'Cat Name', Externals.name as 'Owner/Reporter', Externals.contactNum as 'Contact Number', admittedOn as 'Admitted On',
                                Type.type as 'Type', cage.cageNo as 'Cage ID', ward.code as 'Ward Code', CatStatus.statusType as 'Status'

                        from Cats, Externals, Type, Cage, ward, CatStatus
                        where Cats.externalID = Externals.externalID and 
                        Type.typeID = Cats.typeID and 
                        Cage.cageID = Cats.cageID and
                        Cage. wardID = ward.wardID and
                        Cats.statusID = CatStatus.StatusID"""), conn)

# Convert 'Admitted On' to datetime and format as "date month year"
cat_table_df['Admitted On'] = pd.to_datetime(cat_table_df['Admitted On']).dt.strftime('%d %b %Y')

# Format the contact number to insert a hyphen after the first four digits
cat_table_df['Contact Number'] = cat_table_df['Contact Number'].apply(format_contact_number)

# Generate catCodestr for each catID
cat_table_df['Cat ID'] = cat_table_df['Cat ID'].apply(lambda x: f"PR-{str(x).zfill(5)}")

# Merge Cage ID and Ward Code into one column
cat_table_df['Cage ID'] = cat_table_df.apply(lambda row: f"{row['Ward Code']}-C-{str(row['Cage ID']).zfill(2)}", axis=1)

# Drop the 'Ward Code' column as it is now integrated into the 'Cage ID'
cat_table_df.drop(columns=['Ward Code'], inplace=True)

# st.info("Add, view, delete are done (conditions done in add and update), thora sa update left...")

cat_table_df['Admitted On'] = pd.to_datetime(cat_table_df['Admitted On']).dt.date

st.write(" ")
st.write('##### :orange[Filters:]')
dates2 = cat_table_df['Admitted On'].unique()
status = cat_table_df['Status'].unique()
owner = cat_table_df['Owner/Reporter'].unique()

min_date = min(dates2)
max_date = max(dates2)

col1, col2, col3, col4 = st.columns(4)
with col1:
    start_date_value = st.date_input("Select From Date", min_value=min_date, max_value=max_date, value=min_date, key = 'start_date_filter')
with col2:
    end_date_value = st.date_input("Select To Date", min_value=min_date, max_value=max_date, value=max_date, key = 'end_date_filter')
with col3:
    selected_status = st.selectbox(":white[Select Status:]", options=["No Filters"] + list(status), index=0, placeholder='Choose an option', key='cat_status_filter')
with col4:
    selected_owner = st.selectbox(":white[Select Owner/Reporter:]", options= ["No Filters"] + list(owner), index=0, placeholder='Choose an option', key='cat_owner_filter')

# Reset Filters Button (Do it exactly like this in every page :)
def reset_filters_function():
    st.session_state.start_date_filter = min_date
    st.session_state.end_date_filter = max_date
    st.session_state.cat_status_filter = 'No Filters'
    st.session_state.cat_owner_filter = 'No Filters'

blank, blank, blank, blank, blank, reset = st.columns([3,1,1,1,1,1])

reset_filter_button = reset.button("Reset Filters", on_click=reset_filters_function, use_container_width=True)

if start_date_value and end_date_value:
    filtered_df = cat_table_df[(cat_table_df['Admitted On'] >= start_date_value) & (cat_table_df['Admitted On'] <= end_date_value)]
else:
    filtered_df = cat_table_df

if selected_status!='No Filters':
    filtered_df = filtered_df[filtered_df['Status'] == selected_status]

if selected_owner!="No Filters":
    filtered_df = filtered_df[filtered_df['Owner/Reporter'] == selected_owner]

st.divider()

col1, col2, col3, col4, col5, col6 = st.columns([2,2,2,0.8,0.8,1]) # updated: [3.1,0.6,0.6,0.6,0.6,0.8] , prev: [4.4,1,0.6,0.6,0.6,0.8]

#Add a new cat button
st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)
new_cat = col6.button("✙ New Cat", on_click = add_cat_dialog, use_container_width=True) # ✙, ⊹, ➕

# Display the DataFrame
filtered_df['Admitted On'] = pd.to_datetime(filtered_df['Admitted On']).dt.strftime('%d %b %Y')
cat_table = st.dataframe(filtered_df, width=1500, height=600, hide_index=True, on_select="rerun", selection_mode="single-row", use_container_width=True)


# UPDATE AND DELETE BUTTONS
if cat_table["selection"]["rows"]: #if a row is selected
    selectedRow = filtered_df.iat[cat_table["selection"]["rows"][0], 0]
    # filteredRow = extract_cat_number(selectedRow)
    # print("filteredRow: ", filteredRow)

    # print("selected row is :", selectedRow) -- PA-0001
    view = col4.button("View", on_click= view_cat_dialog, use_container_width=True) # 👀 🧐

    # Admin Rights here
    try:
        if st.session_state.role == 'Administrator':
            update = col5.button("Update", on_click= update_cat_dialog, use_container_width=True) # 📝
        else:
            col5.button("Update", on_click= update_cat_dialog, use_container_width=True, disabled = True)
    except:
        pass
    
    if st.session_state.show_view_cat_dialog:
        view_cat(selectedRow)
        
    if st.session_state.show_update_cat_dialog:
        update_cat(selectedRow)

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

# empty
st.sidebar.write(" ")
st.sidebar.write(" ")
st.sidebar.write(" ")

if st.sidebar.button("🔓 Logout"):
    with st.sidebar:
        with st.spinner('Logging out...'):
            time.sleep(2)

    authenticator.logout(location = "unrendered")
    st.switch_page("LoginScreen.py")

# ---------------------------------------------------------------------------------------------------------------------------#

# TODO:
# Adding, Updating, Viewing, Filtering a cat when NO OWNER ???