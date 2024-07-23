import streamlit as st
import pandas as pd
import datetime

from st_pages import Page, show_pages, add_page_title, hide_pages
from PIL import Image

import sqlalchemy as sa
from millify import prettify
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

# streamlit-authenticator package
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Note the double backslashes
# server = 'DESKTOP-67BT6TD\\FONTAINE' # IBAD
server = 'DESKTOP-HT3NB74' # EMAN
# server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA

database = 'PawRescue' # EMAN :'Khidmat'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

st.set_page_config(page_title="Wards", page_icon="🛏️", initial_sidebar_state="expanded", layout='wide')

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

# Initialize session state for ward data if not already present
if 'wards_df' not in st.session_state:
    st.session_state.wards_df = pd.DataFrame(columns=["Name", "code", "total_cages", "free_cages"])

# Fetch existing wards from the database
with engine.begin() as conn:
    existing_wards = pd.read_sql_query(sa.text("""SELECT name, code, CapacityCages AS total_cages, capacityCages AS free_cages FROM Ward where name is not null"""), conn)

# Combine existing wards with session state wards
combined_wards_df = pd.concat([existing_wards, st.session_state.wards_df]).drop_duplicates(subset=["Name", "code"]).reset_index(drop=True)

st.header("Wards", divider='orange')

# Define the dialog for adding a new ward
def add_ward_dialog():
    st.session_state.show_add_ward_dialog = True # True
    st.session_state.show_update_ward_dialog = False
    st.session_state.show_delete_ward_dialog = False
    st.session_state.show_add_cages_dialog = False
    st.session_state.show_update_cages_dialog = False
    st.session_state.show_delete_cages_dialog = False

def update_ward_dialog():
    st.session_state.show_add_ward_dialog = False
    st.session_state.show_update_ward_dialog = True # True
    st.session_state.show_delete_ward_dialog = False
    st.session_state.show_add_cages_dialog = False
    st.session_state.show_update_cages_dialog = False
    st.session_state.show_delete_cages_dialog = False

def delete_ward_dialog():
    st.session_state.show_add_ward_dialog = False
    st.session_state.show_update_ward_dialog = False
    st.session_state.show_delete_ward_dialog = True # True
    st.session_state.show_add_cages_dialog = False
    st.session_state.show_update_cages_dialog = False
    st.session_state.show_delete_cages_dialog = False

def add_cages_dialog():
    st.session_state.show_add_ward_dialog = False
    st.session_state.show_update_ward_dialog = False
    st.session_state.show_delete_ward_dialog = False
    st.session_state.show_add_cages_dialog = True # True
    st.session_state.show_update_cages_dialog = False
    st.session_state.show_delete_cages_dialog = False

def update_cages_dialog():
    st.session_state.show_add_ward_dialog = False
    st.session_state.show_update_ward_dialog = False
    st.session_state.show_delete_ward_dialog = False
    st.session_state.show_add_cages_dialog = False
    st.session_state.show_update_cages_dialog = True # True
    st.session_state.show_delete_cages_dialog = False

def delete_cages_dialog():
    st.session_state.show_add_ward_dialog = False
    st.session_state.show_update_ward_dialog = False
    st.session_state.show_delete_ward_dialog = False
    st.session_state.show_add_cages_dialog = False
    st.session_state.show_update_cages_dialog = False
    st.session_state.show_delete_cages_dialog = True # True

@st.experimental_dialog("Add New Ward")
def add_ward():
    with engine.begin() as conn:
            current_wardid = int(pd.read_sql_query(sa.text("select top 1 wardID from Ward order by wardID desc"), conn).iloc[0][0]) + 1
    new_id = st.text_input("Ward ID", value = current_wardid, disabled=True)
    new_name = st.text_input("Ward Name", placeholder="Enter Ward Name")
    new_code = st.text_input("Ward Cage Code", placeholder="Enter Code for Cage e.g GW")
    new_cage = st.number_input("Total Cages", value=0, step=1, format="%d", min_value=0)

    add_ward_button = st.button("Add Ward", key='add_ward')

    if add_ward_button:
        everything_filled = False
        valid_wardName = False
        valid_code = False
        valid_cages = False

        if not (new_code and new_name and new_cage):
                st.error("Please fill in all fields before submitting.")
        else:
            everything_filled = True

        if all(x.isalpha() or x.isspace() or x=='.' for x in new_name):
                valid_wardName = True
        else:
            st.error("Please enter valid Ward Name.")

        if all(x.isalpha() for x in new_code) and (len(new_code)>0):
            valid_code = True
        else:
            st.error("Please enter valid Ward Code.")

        if new_cage>0:
            valid_cages=True
        else:
            st.error("Please select a Capacity for the Cages")
            
        if everything_filled and valid_wardName and valid_code and valid_cages:
            with engine.begin() as conn:
                conn.execute(sa.text("""
                    insert into Ward (wardID, name, code, CapacityCages)
                    values (:wardID, :name, :code, :CapacityCages)
                """), {"wardID": new_id, "name": new_name, "code": new_code, "CapacityCages": new_cage})

            new_row = pd.DataFrame({"code": [new_code], "total_cages": [new_cage]}, index=[new_name])
            st.session_state.wards_df = pd.concat([st.session_state.wards_df, new_row])
            st.session_state.show_add_ward_dialog = False
            st.rerun()
        
    st.session_state.show_add_ward_dialog = False
    st.caption('_:orange[Press Esc to Cancel]_')

@st.experimental_dialog("Edit Ward")
def edit_ward():
    with engine.begin() as conn:
        df = pd.read_sql_query("SELECT name FROM Ward where name is not null", conn)
        selected_index = df['name'].tolist()
    index = st.selectbox("Ward Name", selected_index)


    with engine.begin() as conn:
        edit_code = conn.execute(sa.text("select code from Ward where name = :name"), {"name": index}).fetchall()[0][0]
    final_code = st.text_input("Ward Code", edit_code)

    with engine.begin() as conn:
        edit_total_cages = conn.execute(sa.text("select capacityCages from Ward where name = :name"), {"name": index}).fetchall()[0][0]
    final_total_cages = st.number_input("Total Cages", edit_total_cages)

    # print(index, final_name, final_code, final_total_cages)

    if st.button("Save", key='save'):
        everything_filled = False
        valid_code = False
        valid_cages = False

        if not (final_code and final_total_cages):
                st.error("Please fill in all fields before submitting.")
        else:
            everything_filled = True

        if all(x.isalpha() for x in final_code) and (len(final_code)>0):
            valid_code = True
        else:
            st.error("Please enter valid Ward Code.")

        if final_total_cages>edit_total_cages:
            valid_cages=True
        else:
            st.error("Please select a higher capcity for Ward then before")
            
        
        # print(index, final_name, final_code, final_total_cages)
        if (everything_filled and index and valid_code and valid_cages):
            with engine.begin() as conn:
                conn.execute(sa.text("""
                UPDATE Ward
                SET name = :name, code = :code, capacityCages = :total_cages
                WHERE name  = :name
            """), {"code": final_code, "total_cages": final_total_cages, "name": index})
            st.rerun()

    st.session_state.show_update_ward_dialog = False
    st.caption('_:orange[Press Esc to Cancel]_')

@st.experimental_dialog("Delete Ward")
def delete_ward():
    with engine.begin() as conn:
        df = pd.read_sql_query("SELECT * FROM Ward where name is not null", conn)
        selected_name = df['name'].tolist()
        wardID = df['wardID'].tolist()[0]
    name = st.selectbox("Ward Name", selected_name)
    # print(name)

    if st.button("Delete Ward", key='delete'):
        with engine.begin() as conn:
            status = conn.execute(sa.text("""
                    SELECT count(Cage.cageID) 
                    FROM Cage
                    inner JOIN cageStatus ON Cage.cageStatusID = cageStatus.cageStatusID
                    inner join Ward on Ward.wardID = Cage.wardID
                    WHERE cageStatus.cageStatusID = :cageStatusID and name = :name
                """), {"cageStatusID": 1, "name": name}).fetchall()
        # print(status)
        # print(status[0])
            
        if status[0][0] > 0:
            st.warning('You need to delete the cages of this ward from the Cats data first in order to delete this ward', icon="⚠️")
            if st.button("Okay", key='okay'):
                st.rerun()  # Refresh the app to reflect changes
        else:
            with engine.begin() as conn:
                conn.execute(sa.text("update ward set name = NULL, code = NULL, capacityCages = NULL where name = :name"), {"name": name})
            st.rerun()

    st.session_state.show_delete_ward_dialog = False
    st.caption('_:orange[Press Esc to Cancel]_')

@st.experimental_dialog("Add Cages")
def add_cages():
    with engine.begin() as conn:
        cage_id = int(pd.read_sql_query(sa.text("select top 1 cageID from Cage order by cageID desc"), conn).iloc[0][0]) + 1
    cageid = st.text_input("Cage ID", value=cage_id, disabled=True)

    with engine.begin() as conn:
        df = pd.read_sql_query("SELECT * FROM Ward WHERE name IS NOT NULL", conn)
        selected_name = df['name'].tolist()
    name = st.selectbox("Ward Name", selected_name)

    with engine.begin() as conn:
        ward_data = conn.execute(sa.text("SELECT wardID, capacityCages FROM Ward WHERE name = :name"), {"name": name}).fetchone()
        occupied = conn.execute(sa.text("""select count(cageID) as total_cages from Cage
                        inner join Ward on Cage.wardID = Ward.wardID where name = :name"""), {"name": name}).fetchall()
        
    wardID = ward_data[0]
    capacity = ward_data[1]
    occupied = occupied[0][0]

    new_cages = st.number_input("Add Cages", step=1, min_value=0, max_value=(capacity-occupied))
    date = st.date_input("Date of Cage Addition")

    add_new_cages = st.button("Add Cage", key='add_cage')
    if add_new_cages:

        valid_cages = False

        if new_cages==0:
            st.error("Please select number of cages to add")
        else: 
            valid_cages = True


        if valid_cages:
            with engine.begin() as conn:
                for i in range(new_cages):
                    conn.execute(sa.text("""
                        INSERT INTO Cage (cageID, wardID, cageStatusID, date)
                        VALUES (:cageID, :wardID, :cageStatusID, :date)
                    """), {"cageID": cage_id + i, "wardID": wardID, "cageStatusID": 2, "date": date})

            st.rerun()
    st.session_state.show_add_cages_dialog = False
    st.caption('_:orange[Press Esc to Cancel]_')

@st.experimental_dialog("Update Cages")
def update_cages(id_to_update):
    st.write(id_to_update)

    

    if st.button("Update Cages", key='update_cages'):
        st.rerun()

    st.session_state.show_update_cages_dialog = False
    st.caption('_:orange[Press Esc to Cancel]_')
    
@st.experimental_dialog("Delete Cages")
def delete_cages(id_to_delete):

    id_to_delete = int(id_to_delete)

    st.write(f"You are deleting {id_to_delete}")

    with engine.begin() as conn:
        availabililty = conn.execute(sa.text("select cageStatus from cageStatus, cage where cageStatus.cageStatusID = Cage.cageStatusID and cageID = :id_to_delete"),{"id_to_delete":id_to_delete}).fetchone()[0]

    if availabililty == 'Free':
        yes, no = st.columns(2)
        yes_button = yes.button("Yes", key='yes')
        no_button = no.button("No", key='no')
        if yes_button:
            with engine.begin() as conn:
                conn.execute(sa.text("update cage set wardID=NULL, cageStatusID=NULL, date=NULL where cageID = :id_to_delete"), {"id_to_delete": id_to_delete})
            st.rerun()
        elif no_button:
            st.session_state.show_delete_cages_dialog = False
            st.rerun()
    else:
        st.write("You cannot currently delete this cage because it is occupied.")
        if st.button("Okay"):
            st.rerun()

    st.session_state.show_delete_cages_dialog = False
    st.caption('_:orange[Press Esc to Cancel]_')

if 'show_add_ward_dialog' not in st.session_state:
    st.session_state.show_add_ward_dialog = False
if 'show_update_ward_dialog' not in st.session_state:
    st.session_state.show_update_ward_dialog = False
if 'show_delete_ward_dialog' not in st.session_state:
    st.session_state.show_delete_ward_dialog = False

if 'show_add_cages_dialog' not in st.session_state:
    st.session_state.show_add_cages_dialog = False
if 'show_update_cages_dialog' not in st.session_state:
    st.session_state.show_update_cages_dialog = False
if 'show_delete_cages_dialog' not in st.session_state:
    st.session_state.show_delete_cages_dialog = False

if st.session_state.show_add_ward_dialog:
    add_ward()

if st.session_state.show_update_ward_dialog:
    edit_ward()

if st.session_state.show_delete_ward_dialog:
    delete_ward()

if st.session_state.show_add_cages_dialog:
    add_cages()

# "Add Ward" button
col1, col2, col3, col4, col5, col6 = st.columns([1.5,5,2,1,1,1.6])

#Add a new cat button
with col1:
    updateWard = st.button("Edit Ward", on_click=update_ward_dialog)

with col2:
    deleteWard = st.button("Delete Ward", on_click=delete_ward_dialog)

with col3:
    deleteWard = st.button("Increase Cages", on_click=add_cages_dialog)

with col6:
    newWard = st.button("✙ Add Ward", on_click=add_ward_dialog)

# Display the ward information
wards_df = combined_wards_df

for index, row in wards_df.iterrows():

    ward_name = row['name']

    with st.expander(f"**{ward_name}**", expanded=False):
        col1, col2, col3, col4, col5, col6= st.columns([0.1, 0.5, 0.7, 0.7, 1, 1])  # Adjusted column widths

        with col1:
            st.write("")  # Placeholder for the button

        with col2:
            st.write(f"Code: {row['code']}")
            # print(f"Code: {row['code']}")

        with col3:
            with engine.begin() as conn:
                totalCages = conn.execute(sa.text("""
                    select count(cageID)as total_cages from Cage
                    inner join Ward on Cage.wardID = Ward.wardID
                    where code = :code
                """), {"code": row['code']}).fetchall()
            totalCages = totalCages[0][0]
            st.write(f"Available Cages: {totalCages}")

        with col4:
            with engine.begin() as conn:
                freeCage = conn.execute(sa.text("""
                    select count(cageID)as free_cages from Cage
                    inner join Ward on Cage.wardID = Ward.wardID
                    where cageStatusID = :cageStatusID and code = :code
                """), {"cageStatusID": 2, "code": row['code']}).fetchall()

            freeCage = freeCage[0][0]
            st.write(f"Free Cages: {freeCage}")
        
        with engine.begin() as conn:
            capacity = conn.execute(sa.text("select capacityCages from Ward where name = :name"), {"name": f"{row['name']}"}).fetchall()[0][0]
        
        total = st.text_input("Capacity", value=capacity, disabled=True)
        
        with engine.begin() as conn: # there is a problem here!
            result = pd.DataFrame(conn.execute(sa.text(""" 
                    SELECT 
                    Cage.cageID as CageID,
                    Cats.catID as CatID,
                    Cats.catName as CatName,
                    Cage.date as Date,
                    cageStatus.cageStatus as Status
                FROM 
                    Cage
                INNER JOIN 
                    Ward ON Cage.wardID = Ward.wardID
                INNER JOIN 
                    cageStatus ON Cage.cageStatusID = cageStatus.cageStatusID
                LEFT JOIN 
                    Cats ON Cage.cageID = Cats.cageID 
                WHERE name = :name"""), {"name": ward_name}).fetchall())
    
        cages_table = st.dataframe(result, width=1500, height=300, hide_index = True, selection_mode="single-row", on_select='rerun', key = ward_name)

        if cages_table["selection"]["rows"]:

            cage_id_selected = result.iat[cages_table["selection"]["rows"][0],0]

            with col5:
                update_button = col5.button("Transfer", key=str(index)+'update_cages')
                if update_button:
                    st.session_state.show_update_cages_dialog = True
                    update_cages(cage_id_selected)

            with col6:
                delete_button = col6.button("Delete", key = str(index)+'delete_cages')
                if delete_button:
                    st.session_state.show_delete_cages_dialog = True
                    delete_cages(cage_id_selected)
        
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
    authenticator.logout(location = "unrendered")
    st.switch_page("LoginScreen.py")