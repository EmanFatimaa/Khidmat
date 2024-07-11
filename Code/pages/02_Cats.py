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

# database information ; will change when db hosting

# server = 'DESKTOP-67BT6TD\\FONTAINE' # IBAD
server = 'DESKTOP-HT3NB74' # EMAN
# server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA # Note the double backslashes

database = 'PawRescue' # EMAN 'Khidmat'
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

if st.sidebar.button("🔓 Logout"):
    st.switch_page("LoginScreen.py")

hide_pages(["Login"])

#Creating columns for better formatting
col1, col2, col3, col4 = st.columns(4)

#Title
#with col1:
st.header("Cats", divider = "orange")


#Functions
def add_cat_dialog():
    st.session_state.show_add_cat_dialog = True
    st.session_state.show_view_cat_dialog = False
    st.session_state.update_cat_dialog = False
    st.session_state.delete_cat_dialog = False

def view_cat_dialog():
    st.session_state.show_add_cat_dialog = False
    st.session_state.show_view_cat_dialog = True
    st.session_state.show_update_cat_dialog = False
    st.session_state.show_delete_cat_dialog = False

def update_cat_dialog():
    st.session_state.show_add_cat_dialog = False
    st.session_state.show_view_cat_dialog = False
    st.session_state.show_update_cat_dialog = True
    st.session_state.show_delete_cat_dialog = False

def delete_cat_dialog():
    st.session_state.show_add_cat_dialog = False
    st.session_state.show_view_cat_dialog = False
    st.session_state.show_update_cat_dialog =  False
    st.session_state.show_delete_cat_dialog = True

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
    numberStr = cat_id_str.replace("PA-", "")
    
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
            catCodestr = "PA-000" + str(currentCatID) #need to fix this logic , explore prettify
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
            cageID = pd.read_sql_query(sa.text("SELECT cageID FROM Cage WHERE cageID NOT IN (SELECT cageID FROM Cats)"), conn)  # OR: select cageID from Cage where cageStatus = 'Free'
            wardID =pd.read_sql_query(sa.text("Select wardID from ward where wardID in (select WardID from cage)"),conn)
        cageNum = st.selectbox("Cage Number", cageID["cageID"].tolist())  # This should also show which Ward it is in and that Cage is free or not ofc.
        
        
    with engine.begin() as conn:
        statusSelection = pd.read_sql_query(sa.text("SELECT statusType FROM CatStatus"), conn)
    status = st.selectbox("Status", statusSelection["statusType"].tolist())

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

    # Date
    date = st.date_input('Date', value=datetime.date.today(), disabled=True)

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
    if st.button("Add cat"):
       
        # Checks
        everythingFilled = False

        # Check if any of the fields are left unfilled
        if not (age and type and name and gender and cageNum and status and ownerName and ownerContact and address):
            st.error("Please fill in all fields before submitting.")
            print("Please fill in all fields.")
        else:
            everythingFilled = True

        if everythingFilled:
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
                :admittedOn)"""),
                {
                    "catID": currentCatID, "catName": name, "age": age, "gender": gender, 
                    "type": type, "cageID": cageNum, "name": ownerName, 
                    "contactNum": ownerContact, "address": address, 
                    "status": status, "admittedOn": date
                })

            with st.spinner('Adding...'):
                time.sleep(2)
            st.rerun()
    st.session_state.show_add_cat_dialog = False
    
# with engine.begin() as conn:
#         catDB = int(pd.read_sql_query(sa.text("select top 1 catID from cats order by catID desc "), conn).iat[0,0])
#     if catDB == currentCatID:
#         st.success("Cat with CatID: "+ str(catCodestr)+ " has been added successfully", icon = "🎉")
#         st.balloons() # why not working

# Check if the session state exists or not
if 'show_add_cat_dialog' not in st.session_state:
    st.session_state.show_add_cat_dialog = False

col1, col2, col3, col4, col5, col6 = st.columns([4.4,1.2,1,1,1,1.6])

#Add a new cat button
st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)
new_cat = col6.button("✙ Add New Cat", on_click = add_cat_dialog) # ✙, ⊹, ➕

if st.session_state.show_add_cat_dialog:
    add_cat()
#-------------------------------------------------------------------

#UPDATE DIALOG
@st.experimental_dialog("Update Cat Details")
def update_cat(id):
    
    #cats info (in the form)
    st.write(" :orange[Cat related details]")

    # Creating columns for better formatting 
    col1, col2 = st.columns(2)

    with col1:
        
        #Cat ID Field
        catID = st.text_input("Cat ID", value = id) # disable if id should not be editable
        
        # Age field
        with engine.begin() as conn:
            ageValue= conn.execute(sa.text("Select age from cats where catID = :catID") ,{"catID": extract_cat_number(id)}).fetchall()[0][0]
        age = st.number_input("Age (in years)", step = 0.1, value = float(ageValue))

         # Type field
        with engine.begin() as conn:
            typeSelection = pd.read_sql_query(sa.text("SELECT type FROM Type"), conn)
        type = st.selectbox("Type", typeSelection["type"].tolist())

        # # Type field
        # with engine.begin() as conn:
        #     typeValue = conn.execute(sa.text("SELECT type FROM Type where typeID in (select typeID from cats where catID = :catID)", {"catID":  extract_cat_number(id)}).fetchall())[0][0]
        # type = st.selectbox("Type", typeValue["type"].tolist())

    with col2:
        name = st.text_input("Cat Name", placeholder="Enter Cat's Name")

        # with engine.begin() as conn:
        #     catNameValue = conn.execute(sa.text("Select catName from cats where  catID = :catID)"), {"catID": extract_cat_number(id)}).fetchall()[0]
        #     # catNameValue = conn.execute(sa.text("Select name from Externals where externalID = (select externalID from cats where catID = :catID)"), {"catID": extract_cat_number(id)}).fetchall()[0][0]
        # catName = st.text_input("Cat Name", value =  catNameValue)
        
        # Gender field
        
        with engine.begin() as conn:
            genderSelection = pd.read_sql_query(sa.text("SELECT gender FROM Gender"), conn)
        gender = st.selectbox("Gender", genderSelection["gender"].tolist())
        
        # with engine.begin() as conn:
        #     genderValue = int(conn.execute(sa.text("SELECT gender FROM Gender where genderID in (select genderID from cats where catID = : catID"), {"catID": extract_cat_number(id)}).fetchall()[0][0])
        #     print(genderValue)
        # gender = st.selectbox("Gender", genderValue["gender"].tolist())

        # Cage no field
        with engine.begin() as conn:
            cageID = pd.read_sql_query(sa.text("SELECT cageID FROM Cage WHERE cageID NOT IN (SELECT cageID FROM Cats)"), conn)  # OR: select cageID from Cage where cageStatus = 'Free'
            wardID =pd.read_sql_query(sa.text("Select wardID from ward where wardID in (select WardID from cage)"),conn)
        cageNum = st.selectbox("Cage Number", cageID["cageID"].tolist())  # This should also show which Ward it is in and that Cage is free or not ofc.
        
    with engine.begin() as conn:
        statusSelection = pd.read_sql_query(sa.text("SELECT statusType FROM CatStatus"), conn)
        status = st.selectbox("Status", statusSelection["statusType"].tolist())

       # Owner related info (in the form)
    st.write(" :orange[Owner related details]")

    col1, col2 = st.columns(2)  # redefining to enter owner related details after cat details

    with col1:
        # Name field
        with engine.begin() as conn:
            ownerNameValue = conn.execute(sa.text("Select name from Externals where externalID = (select externalID from cats where catID = :catID)"), {"catID": extract_cat_number(id)}).fetchall()[0][0]
        ownerName = st.text_input("Owner/Reporter's Name",  value = ownerNameValue)
    
    with col2:
        # Owner contact text input
        # with engine.begin() as conn:
        #     contactValue = conn.execute(sa.text("select contact from externals where externalID in (select externalID from cats where catID = :catID"),{"catID": extract_cat_number(id)}).fetchall()[0][0]
        # contact = st.text_input("Owner's Contact", value = contact)

        contactFromDB = ''
        if ownerName:
            with engine.begin() as conn:
                fetchall = conn.execute(sa.text("SELECT contactNum FROM Externals WHERE name = :name"), {"name": ownerName}).fetchall()
                if fetchall:
                    contactFromDB = fetchall[0][0]
        ownerContact = st.text_input("Owner's Contact", value=contactFromDB)

    # Date
    date = st.date_input('Date', value=datetime.date.today())

    # Address text area
    # with engine.begin() as conn:
        # addressValue = conn.execute("select address from externals where externalID in (select externalID from cats where catID = :catID)", {"catID": extract_cat_number(id)}).fetchall()[0][0]
    address = st.text_area("Address", placeholder="Enter Address")

    # Submit and Cancel buttons
    st.caption(':orange[Press Esc to Cancel]')
    st.session_state.show_update_cat_dialog = False

#------------------------------------------------------------

#DELETE
@st.experimental_dialog("Delete Cat Details")
def delete_cat(id):
    st.warning("Are you sure you want to delete cat ID: "+ str(id)+ " ?", icon = "⚠️")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    if col3.button("Yes"):
        # with engine.begin() as conn:
        #     conn.execute(sa.text())
        st.rerun()

    if col4.button("No ", key = "no"):
        st.rerun()

    st.caption('_:orange[Press Esc to Cancel]_') 
    st.session_state.show_delete_cat_dialog = False
    

# Check if the session state exists or not
if 'show_add_cat_dialog' not in st.session_state:
    st.session_state.show_add_cat_dialog = False
if 'show_view_cat_dialog' not in st.session_state:
    st.session_state.show_view_cat_dialog = False
if 'show_update_cat_dialog' not in st.session_state:
    st.session_state.show_update_cat_dialog = False
if 'show_delete_cat_dialog' not in st.session_state:
    st.session_state.show_delete_cat_dialog = False
# ------------------------------------------------------------
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
            selectedCatName = cat_table_df.iat[cat_table["selection"]["rows"][0],1]
            # print("selected cat name:", selectedCatName)
            selectedCage = cat_table_df.iat[cat_table["selection"]["rows"][0],6]
            # print("selected age:", selectedCage)
            selectedStatus = cat_table_df.iat[cat_table["selection"]["rows"][0],7]
            # print("selected status:", selectedStatus)
            selectedOwnerName = cat_table_df.iat[cat_table["selection"]["rows"][0],2]
            # print("selected owner name:", selectedOwnerName)
            selectedOwnerContact = cat_table_df.iat[cat_table["selection"]["rows"][0],3]
            # print("selected owner contact:", selectedOwnerContact)
            selectedDate = cat_table_df.iat[cat_table["selection"]["rows"][0],4]
            # print("selected date:", selectedDate)
            selectedType = cat_table_df.iat[cat_table["selection"]["rows"][0],5]
            # print("selected type:", selectedType)

    # Expanders:
    with st.expander(":orange[General Information]", expanded= False):
        
        st.write("***Name:***",selectedCatName )
        st.write("***Cage ID:***", selectedCage)
        st.write("***Admitted On:***",selectedDate)

        if str(int(genderDB[0])) == "1":
            st.write("***Gender:***", "Male")

        elif str(int(genderDB[0])) == "2":
            st.write("***Gender:***", "Female")

        st.write("***Age:***", str(int(ageDB[0])), "yr(s)")
        st.write("***Status:***",selectedStatus)

    
    with st.expander(":orange[Owner/Reporter's Details]", expanded = False):
            st.write("***Name:***", selectedOwnerName)
            st.write("***Contact Number:***", selectedOwnerContact)
            st.write("***Address:***", str(addressDB[0]))
            st.write("***Pet Type:***", selectedType)

    with st.expander(":orange[Treatment related Details]", expanded = False):
        # with st.table():
        # st.write("*To add a new treatment kindly click the button below to be redirected to treatments page*" )
        col1, col2= st.columns([1.7, 1])
        
        with col2:
            treatment = st.button(" ✙ Add Treatment")
        if treatment:
            st.switch_page("pages/03_Treatments.py") 

        with engine.begin() as conn:
            treatment_table_df = pd.read_sql_query(sa.text("""
            select dateTime as 'Date/Time', temperature as 'Temp', treatment as 'Treatment' , users.userName as 'Given by'
            from treatment
            join cats on treatment.catID = cats.catID
            join users on treatment.userID = users.userID"""), conn)

        treatment_table_df["Date/Time"] =pd.to_datetime(treatment_table_df["Date/Time"]).dt.strftime('%d %b %Y, %I:%M %p')
        st.write("Table:")
        st.table(treatment_table_df)
        st.write("Dataframe:")
        st.dataframe(treatment_table_df, width = 600, height = 110, hide_index = True)

    st.caption('_:orange[Press Esc to Cancel]_') 
    st.session_state.show_view_cat_dialog = False
# ------------------------------------------------------------
#Table for Cats:
with engine.begin() as conn:
    cat_table_df = pd.read_sql_query(sa.text(""" 
                        select catID as 'Cat ID', catName as 'Cat Name', Externals.name as 'Owner/Reporter', Externals.contactNum as 'Contact Number', admittedOn as 'Admitted On',
                                Type.type as 'Type', Cage.cageID as 'Cage ID', CatStatus.statusType as 'Status'

                        from Cats, Externals, Type, Cage, CatStatus 
                        where Cats.externalID = Externals.externalID and 
                        Type.typeID = Cats.typeID and 
                        Cage.cageID = Cats.cageID and
                        Cats.statusID = CatStatus.StatusID"""), conn)

# Convert 'Admitted On' to datetime and format as "date month year"
cat_table_df['Admitted On'] = pd.to_datetime(cat_table_df['Admitted On']).dt.strftime('%d %b %Y')

# Format the contact number to insert a hyphen after the first four digits
cat_table_df['Contact Number'] = cat_table_df['Contact Number'].apply(format_contact_number)

# Generate catCodestr for each catID
cat_table_df['Cat ID'] = cat_table_df['Cat ID'].apply(lambda x: f"PA-{str(x).zfill(4)}")

# Generate cage for each catID
cat_table_df['Cage ID'] = cat_table_df['Cage ID'].apply(lambda x: f"GW-C-{str(x).zfill(2)}")

# Display the DataFrame
cat_table = st.dataframe(cat_table_df, width=1500, height=600, hide_index=True, on_select="rerun", selection_mode="single-row")

# UPDATE AND DELETE BUTTONS
if cat_table["selection"]["rows"]: #if a row is selected
    selectedRow = cat_table_df.iat[cat_table["selection"]["rows"][0], 0]
    # filteredRow = extract_cat_number(selectedRow)
    # print("filteredRow: ", filteredRow)

    # print("selected row is :", selectedRow) -- PA-0001
    view = col3.button("View", on_click= view_cat_dialog) # 👀 🧐
    update = col4.button("Update  ", on_click= update_cat_dialog) # 📝
    delete = col5.button("Delete  ", on_click= delete_cat_dialog) #🗑️

    if st.session_state.show_view_cat_dialog:
        view_cat(selectedRow)
        
    if st.session_state.show_update_cat_dialog:
        update_cat(selectedRow)

    if st.session_state.show_delete_cat_dialog:
        delete_cat(selectedRow)
else:
    print("No row selected")

# --------------------------------------------------------------------------------------------------------------------------- #
# Edit and Delete Remains
# Filtering Remains
# Lastly, Aesthestics ofc
# Checks remain for each field as well (Refer to Treatments.py or Finances.py)
# Error of when inserting a new queryy
# Wards and Cage should update by their own
# Code for upfating cage id for managing when cages get free/occupied
