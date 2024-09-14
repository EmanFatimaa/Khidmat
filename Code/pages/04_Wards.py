import streamlit as st
import pandas as pd
import time

from st_pages import Page, show_pages, add_page_title, hide_pages
from PIL import Image
from datetime import datetime

import sqlalchemy as sa
from millify import prettify
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

# streamlit-authenticator package
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# database information ; will change when db hosting
server = 'DESKTOP-67BT6TD\\FONTAINE' # IBAD
# server = 'DESKTOP-HT3NB74' # EMAN
# server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA

database = 'DummyPawRescue'
# database = 'SchemaPawRescue'

connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

st.set_page_config(page_title="Wards", page_icon="🛏️", initial_sidebar_state="expanded", layout='wide')

def implement_markdown():
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

# ---------------------------------------------------------------------------------- #

# logo
logo = Image.open("assets/logo.png")
st.logo(logo)

implement_markdown()

hide_pages(["Login"])

#Funciton to extract number from cat id
def extract_cat_number(cat_id_str):
    # Remove the prefix "PA-"
    numberStr = cat_id_str.replace("PR-", "")
    
    # Convert to integer
    numberInt = int(numberStr)
    
    return numberInt

# Define the dialog for adding a new ward
def add_ward_dialog():
    st.session_state.show_add_ward_dialog = True # True
    st.session_state.show_update_ward_dialog = False
    st.session_state.show_delete_ward_dialog = False
    # st.session_state.show_add_cages_dialog = False
    st.session_state.show_update_cages_dialog = False
    st.session_state.show_delete_cages_dialog = False

def update_ward_dialog():
    st.session_state.show_add_ward_dialog = False
    st.session_state.show_update_ward_dialog = True # True
    st.session_state.show_delete_ward_dialog = False
    # st.session_state.show_add_cages_dialog = False
    st.session_state.show_update_cages_dialog = False
    st.session_state.show_delete_cages_dialog = False

def delete_ward_dialog():
    st.session_state.show_add_ward_dialog = False
    st.session_state.show_update_ward_dialog = False
    st.session_state.show_delete_ward_dialog = True # True
    # st.session_state.show_add_cages_dialog = False
    st.session_state.show_update_cages_dialog = False
    st.session_state.show_delete_cages_dialog = False

# def add_cages_dialog():
#     st.session_state.show_add_ward_dialog = False
#     st.session_state.show_update_ward_dialog = False
#     st.session_state.show_delete_ward_dialog = False
#     st.session_state.show_add_cages_dialog = True # True
#     st.session_state.show_update_cages_dialog = False
#     st.session_state.show_delete_cages_dialog = False

def update_cages_dialog():
    st.session_state.show_add_ward_dialog = False
    st.session_state.show_update_ward_dialog = False
    st.session_state.show_delete_ward_dialog = False
    # st.session_state.show_add_cages_dialog = False
    st.session_state.show_update_cages_dialog = True # True
    st.session_state.show_delete_cages_dialog = False

def delete_cages_dialog():
    st.session_state.show_add_ward_dialog = False
    st.session_state.show_update_ward_dialog = False
    st.session_state.show_delete_ward_dialog = False
    # st.session_state.show_add_cages_dialog = False
    st.session_state.show_update_cages_dialog = False
    st.session_state.show_delete_cages_dialog = True # True

@st.experimental_dialog("Add New Ward")
def add_ward():
    try:
        with engine.begin() as conn:
                current_wardid = int(pd.read_sql_query(sa.text("select top 1 wardID from Ward order by wardID desc"), conn).iloc[0][0]) + 1
    except:
        current_wardid = 1
    # new_id = st.text_input("Ward ID", value = current_wardid, disabled=True)
    new_name = st.text_input("Ward Name", placeholder="Enter Ward Name")
    new_code = st.text_input("Ward Cage Code", placeholder="Enter Code for Cage e.g GW")
    new_cage = st.number_input("Total Cages", value=0, step=1, format="%d", min_value=0)

    add_ward_button = st.button("Add Ward", key='add_ward')

    if add_ward_button:
        everything_filled = False
        valid_wardName = False
        valid_code = False
        valid_cages = False

        current_date_str = datetime.now().strftime("%d-%m-%Y")
        date = datetime.strptime(current_date_str, "%d-%m-%Y").date()

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
                """), {"wardID": current_wardid, "name": new_name, "code": new_code, "CapacityCages": new_cage})

                try:
                    cage_id = int(pd.read_sql_query(sa.text("select top 1 cageID from Cage order by cageID desc"), conn).iloc[0][0]) + 1
                except:
                    cage_id = 1
                for i in range(new_cage):
                    
                    # Adding new cages to the Cage table
                    conn.execute(sa.text("""
                        INSERT INTO Cage (cageID, wardID, cageStatusID, date)
                        VALUES (:cageID, :wardID, :cageStatusID, :date)
                    """), {"cageID": cage_id + i, "wardID": current_wardid, "cageStatusID": 2, "date": date})

                    # Generating Cage IDs for the newly added cages
                    conn.execute(sa.text("""
                        UPDATE Cage
                        SET cageNo = :cageNo
                        WHERE cageID = :cageID
                    """), {"cageNo": 1 + i, "cageID": cage_id + i})

            new_row = pd.DataFrame({"code": [new_code], "total_cages": [new_cage]}, index=[new_name])
            st.session_state.wards_df = pd.concat([st.session_state.wards_df, new_row])
            
            # st.session_state.show_add_ward_dialog = False
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

    with engine.begin() as conn:
        wardid = conn.execute(sa.text("select wardID from Ward where name = :name"), {"name": index}).fetchall()[0][0]

    if st.button("Save", key='save'):
        everything_filled = False
        valid_code = False
        # valid_cages = False

        current_date_str = datetime.now().strftime("%d-%m-%Y")
        date = datetime.strptime(current_date_str, "%d-%m-%Y").date()
        
        loop = final_total_cages-edit_total_cages

        if not (final_code and final_total_cages):
                st.error("Please fill in all fields before submitting.")
        else:
            everything_filled = True

        if all(x.isalpha() for x in final_code) and (len(final_code)>0):
            valid_code = True
        else:
            st.error("Please enter valid Ward Code.")

        # if final_total_cages>edit_total_cages:
        #     valid_cages=True
        # else:
        #     st.error("Please select a higher capacity for Ward then before")
            
        if (everything_filled and index and valid_code): # and valid_cages):
            with engine.begin() as conn:
                
                conn.execute(sa.text("""
                UPDATE Ward
                SET name = :name, code = :code, capacityCages = :total_cages
                WHERE name  = :name
            """), {"code": final_code, "total_cages": final_total_cages, "name": index})
                
                cage_id = int(pd.read_sql_query(sa.text("select top 1 cageID from Cage order by cageID desc"), conn).iloc[0][0]) + 1
                cage_no = int(pd.read_sql_query(sa.text("select top 1 cageNo from Cage where wardID = :wardID order by cageID desc"), conn, params = {'wardID':wardid}).iloc[0][0]) + 1

                # do this in conn.execute method

                for i in range(loop):

                    # Adding new cages to the Cage table
                    conn.execute(sa.text("""
                        INSERT INTO Cage (cageID, wardID, cageStatusID, date)
                        VALUES (:cageID, :wardID, :cageStatusID, :date)
                    """), {"cageID": cage_id + i, "wardID": wardid, "cageStatusID": 2, "date": date})
                    
                    # Generating Cage IDs for the newly added cages
                    conn.execute(sa.text("""
                        UPDATE Cage
                        SET cageNo = :cageNo
                        WHERE cageID = :cageID
                    """), {"cageNo": cage_no + i, "cageID": cage_id + i})

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
            
        if status[0][0] > 0:
            st.warning('You need to delete the cages of this ward from the Cats data first in order to delete this ward', icon="⚠️")
            if st.button("Okay", key='okay'):
                st.rerun()  # Refresh the app to reflect changes
        else:
            with engine.begin() as conn:
                conn.execute(sa.text("update cage set wardID = NULL, cageStatusID = NULL, date = NULL, cageNo = NULL where wardID = (select wardID from ward where name = :name)"), {"name": name})
                conn.execute(sa.text("update ward set name = NULL, code = NULL, capacityCages = NULL where name = :name"), {"name": name})
            st.rerun()

    st.session_state.show_delete_ward_dialog = False
    st.caption('_:orange[Press Esc to Cancel]_')

# @st.experimental_dialog("Add Cages")
# def add_cages():
#     with engine.begin() as conn:
#         cage_id = int(pd.read_sql_query(sa.text("select top 1 cageID from Cage order by cageID desc"), conn).iloc[0][0]) + 1
#     cageid = st.text_input("Cage ID", value=cage_id, disabled=True)

#     with engine.begin() as conn:
#         df = pd.read_sql_query("SELECT * FROM Ward WHERE name IS NOT NULL", conn)
#         selected_name = df['name'].tolist()
#     name = st.selectbox("Ward Name", selected_name)

#     with engine.begin() as conn:
#         ward_data = conn.execute(sa.text("SELECT wardID, capacityCages FROM Ward WHERE name = :name"), {"name": name}).fetchone()
#         occupied = conn.execute(sa.text("""select count(cageID) as total_cages from Cage
#                         inner join Ward on Cage.wardID = Ward.wardID where name = :name"""), {"name": name}).fetchall()
        
#     wardID = ward_data[0]
#     capacity = ward_data[1]
#     occupied = occupied[0][0]

#     new_cages = st.number_input("Add Cages", step=1, min_value=0, max_value=(capacity-occupied))
#     date = st.date_input("Date of Cage Addition")

#     add_new_cages = st.button("Add Cage", key='add_cage')
#     if add_new_cages:

#         valid_cages = False

#         if new_cages==0:
#             st.error("Please select number of cages to add")
#         else: 
#             valid_cages = True


#         if valid_cages:
#             with engine.begin() as conn:
#                 for i in range(new_cages):
#                     conn.execute(sa.text("""
#                         INSERT INTO Cage (cageID, wardID, cageStatusID, date)
#                         VALUES (:cageID, :wardID, :cageStatusID, :date)
#                     """), {"cageID": cage_id + i, "wardID": wardID, "cageStatusID": 2, "date": date})

#             st.rerun()

#     st.session_state.show_add_cages_dialog = False
#     st.caption('_:orange[Press Esc to Cancel]_')

# Free -> Occupied by putting a Cat in that Cage and making that Cage free. 
# Occupied -> Free by removing the Cat from that Cage and putting it elsewhere.
@st.experimental_dialog("Update Cages")
def update_cages(new_id_update, code_to_update, availability):

    if availability == 'Free':

        st.write(f"### Transferring a cat to: :orange[{code_to_update}]")

        col1, col2 = st.columns(2)

        with engine.begin() as conn:
            df = pd.read_sql_query("SELECT CatID FROM Cats where cageID is not NULL", conn)
        cat_ids = df['CatID'].tolist()
        
        with col1:
            selected_cat_code_id = st.selectbox("New Cat ID", map(lambda x: f"PR-{str(x).zfill(5)}", cat_ids))
            selected_cat_id = extract_cat_number(selected_cat_code_id)

        with engine.begin() as conn:
            name = conn.execute(sa.text("select catName from Cats where catID= :catID"), {"catID": selected_cat_id}).fetchall()[0][0]
            old_cage_id = conn.execute(sa.text("select cageID from Cats where catID= :catID"), {"catID": selected_cat_id}).fetchall()[0][0]
            old_cage_code = conn.execute(sa.text("select code from Ward where wardID = (select wardID from Cage where cageID = :cageID)"), {"cageID": old_cage_id}).fetchall()[0][0]
            old_cage_no = conn.execute(sa.text("select cageNo from Cage where cageID = :cageID"), {"cageID": old_cage_id}).fetchall()[0][0]
                
        with col2:
            st.text_input('Cat Name', value = name, disabled=True)
        
        old_cage_id_code = f"{old_cage_code}-C-{str(old_cage_no).zfill(2)}"
        st.write(f"#### The old cage will be made free after the transfer. (:orange[{old_cage_id_code}])")

        blank, yes, no = st.columns([3,1,1])
        yes_button = yes.button("Yes", key='yes', use_container_width=True)
        no_button = no.button("No", key='no', use_container_width=True)

        if yes_button:
            with engine.begin() as conn:
                conn.execute(sa.text("update Cats set cageID = :new_id_update where catID = :selected_cat_id"), {"new_id_update": new_id_update, "selected_cat_id": selected_cat_id})
                conn.execute(sa.text("update Cage set cageStatusID = 1 where cageID = :new_id_update"), {"new_id_update": new_id_update})
                conn.execute(sa.text("update Cage set cageStatusID = 2 where cageID = :old_cage_id"), {"old_cage_id": old_cage_id})
            st.rerun()
        
        elif no_button:
            st.session_state.show_delete_cages_dialog = False
            st.rerun()

        st.session_state.show_update_cages_dialog = False
        return
    
    elif availability == 'Occupied':
        
        with engine.begin() as conn:
            df = conn.execute(sa.text("SELECT CatID from Cats where cageID = :cageID"), {'cageID':new_id_update}).fetchone()[0]
        cat_transferred = f"PR-{str(df).zfill(5)}"

        st.write(f"### Transferring the cat :orange[{cat_transferred}] from :orange[{code_to_update}] to:")

        # Cage no field
        with engine.begin() as conn:
            cage_code_id_df = pd.read_sql_query(sa.text("select cage.cageID, code, cageNo from ward, cage where ward.wardID = cage.wardID and cageStatusID = 2"), conn)

        cage_code_id_df["cagecodeID"] = cage_code_id_df.apply(lambda row: f"{row['code']}-C-{str(row['cageNo']).zfill(2)}", axis=1)
        cage_code_id_df = cage_code_id_df._append({"cagecodeID": code_to_update, "cageID": new_id_update}, ignore_index = True)
        cageID_list = cage_code_id_df["cagecodeID"].tolist()

        cageCode = st.selectbox("New Cage ID", cageID_list, index=cageID_list.index(code_to_update))
        cageID = int(cage_code_id_df.iat[cageID_list.index(cageCode),0])

        st.write(f"##### The old cage will be made free after the transfer.")

        blank, yes, no = st.columns([3,1,1])
        yes_button = yes.button("Yes", key='yes', use_container_width=True)
        no_button = no.button("No", key='no', use_container_width=True)

        if yes_button:
            with engine.begin() as conn:
                conn.execute(sa.text("update Cats set cageID = :cageID where catID = :catID"), {"cageID": cageID, "catID": df})
                conn.execute(sa.text("update Cage set cageStatusID = 1 where cageID = :cageID"), {"cageID": cageID})
                conn.execute(sa.text("update Cage set cageStatusID = 2 where cageID = :new_id_update"), {"new_id_update": new_id_update})
            st.rerun()
        
        elif no_button:
            st.session_state.show_delete_cages_dialog = False
            st.rerun()

        st.session_state.show_update_cages_dialog = False
        return

    
@st.experimental_dialog("Delete Cages")
def delete_cages(id_to_delete, code_to_delete):

    st.write(f"### You are deleting: :orange[{code_to_delete}]")

    blank, yes, no = st.columns([3,1,1])
    yes_button = yes.button("Yes", key='yes', use_container_width=True)
    no_button = no.button("No", key='no', use_container_width=True)
    if yes_button:
        with engine.begin() as conn:
            conn.execute(sa.text("update cage set wardID=NULL, cageStatusID=NULL, date=NULL where cageID = :id_to_delete"), {"id_to_delete": id_to_delete})
            conn.execute(sa.text("update ward set capacityCages = capacityCages - 1 where code = :code_to_delete"), {"code_to_delete": code_to_delete})
        st.rerun()
    elif no_button:
        st.session_state.show_delete_cages_dialog = False
        st.rerun()

    st.session_state.show_delete_cages_dialog = False
    st.caption('_:orange[Press Esc to Cancel]_')

if 'show_add_ward_dialog' not in st.session_state:
    st.session_state.show_add_ward_dialog = False
if 'show_update_ward_dialog' not in st.session_state:
    st.session_state.show_update_ward_dialog = False
if 'show_delete_ward_dialog' not in st.session_state:
    st.session_state.show_delete_ward_dialog = False

# if 'show_add_cages_dialog' not in st.session_state:
#     st.session_state.show_add_cages_dialog = False
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

# if st.session_state.show_add_cages_dialog:
#     add_cages()

# Initialize session state for ward data if not already present
if 'wards_df' not in st.session_state:
    st.session_state.wards_df = pd.DataFrame(columns=["Name", "code", "total_cages", "free_cages"])

# Fetch existing wards from the database
with engine.begin() as conn:
    existing_wards = pd.read_sql_query(sa.text("""SELECT name, code, CapacityCages AS total_cages, capacityCages AS free_cages FROM Ward where name is not null"""), conn)

# Combine existing wards with session state wards
combined_wards_df = pd.concat([existing_wards, st.session_state.wards_df]).drop_duplicates(subset=["Name", "code"]).reset_index(drop=True)

st.header("Wards", divider='orange')

# Display the ward information
wards_df = combined_wards_df

# "Add Ward" button
col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,2.5,2,1])
try:
    if st.session_state.role == 'Administrator':
        with col1:
            updateWard = st.button("Edit Ward", on_click=update_ward_dialog, use_container_width=True, disabled=len(wards_df)==0)

        with col2:
            deleteWard = st.button("Delete Ward", on_click=delete_ward_dialog, use_container_width=True, disabled=len(wards_df)==0)
except:
    pass

with col6:
    newWard = st.button("✙ New Ward", on_click=add_ward_dialog, use_container_width=True)

def reset_filters_function(a):
    st.session_state[f"{a}_start_date_filter"] = min_date
    st.session_state[f"{a}_end_date_filter"] = max_date
    st.session_state[f"{a}_status"] = 'No Filters'
    
# Main Loop
for index, row in wards_df.iterrows():

    ward_name = row['name']

    if pd.isna(ward_name):
        continue

    with st.expander(f"**{ward_name}**", expanded=False):
        col2, col3, col4, blank, col5, col6= st.columns([1,1.5,1.5,3,1,1])  # Adjusted column widths

        with col2:
            st.write(f"###### Code: :orange[{row['code']}]")

        with col3:
            with engine.begin() as conn:
                totalCages = conn.execute(sa.text("""
                    select capacityCages from Ward where name = :name
                """), {"name": row['name']}).fetchall()
            totalCages = totalCages[0][0]
            st.write(f"###### Total Cages: :orange[{totalCages}]")

        with col4:
            with engine.begin() as conn:
                freeCage = conn.execute(sa.text("""
                    select count(cageID) as free_cages from Cage
                    inner join Ward on Cage.wardID = Ward.wardID
                    where cageStatusID = :cageStatusID and code = :code
                """), {"cageStatusID": 2, "code": row['code']}).fetchall()

            freeCage = freeCage[0][0]
            st.write(f"###### Free Cages: :orange[{freeCage}]")
        
        with engine.begin() as conn: # there is a problem here!
            result = pd.DataFrame(conn.execute(sa.text(""" 
                    SELECT 
                    Cage.cageID as 'Cage ID',
                    Cats.catID as 'Cat ID',
                    Cats.catName as 'Cat Name',
                    Cage.date as Date,
                    cageStatus.cageStatus as Status,
                    cageNo as 'Cage No', 
                    ward.code as 'Ward Code'
                FROM 
                    Cage
                INNER JOIN 
                    Ward ON Cage.wardID = Ward.wardID
                INNER JOIN 
                    cageStatus ON Cage.cageStatusID = cageStatus.cageStatusID
                LEFT JOIN 
                    Cats ON Cage.cageID = Cats.cageID 
                WHERE name = :name"""), {"name": ward_name}).fetchall())
            
        # Convert 'Date' to datetime and format as "date month year"
        result['Date'] = pd.to_datetime(result['Date']).dt.strftime('%d %b %Y')

        # Merge Cage ID and Ward Code into one column
        result['Cage ID'] = result.apply(lambda row: f"{row['Ward Code']}-C-{str(row['Cage No']).zfill(2)}", axis=1)

        # Generate catCodestr for each catID
        def generate_cat_id(x):
            try:
                return f"PR-{str(int(x)).zfill(5)}"
            except:
                return x
        result['Cat ID'] = result['Cat ID'].apply(lambda x: generate_cat_id(x))
        result['Date'] = pd.to_datetime(result['Date']).dt.date

        st.write('##### :orange[Filters:]')
        dates2 = result['Date'].unique()
        if len(dates2) == 0:
            dates2 = [datetime.date.today()]
        status_id = result['Status'].unique()

        min_date = min(dates2)
        max_date = max(dates2)

        col1, col2, col3 = st.columns(3)
        with col1:
            start_date_value = st.date_input("Select From Date", min_value=min_date, max_value=max_date, value=min_date, key=f"{ward_name}_start_date_filter")
        with col2:
            end_date_value = st.date_input("Select To Date", min_value=min_date, max_value=max_date, value=max_date, key=f"{ward_name}_end_date_filter")
        with col3:
            selected_status2 = st.selectbox("Select Status", options=["No Filters"] + list(status_id), index=0, placeholder='Choose an option', key=f"{ward_name}_status")

        blank, blank, blank, blank, blank, reset = st.columns([3,1,1,1,1,1])
        reset_filter_button = reset.button("Reset Filters", on_click=reset_filters_function, args = (ward_name, ), use_container_width=True, key=f"{ward_name}_reset_button")

        if start_date_value and end_date_value:
            filtered_df = result[(result['Date'] >= start_date_value) & (result['Date'] <= end_date_value)]
        else:
            filtered_df = result

        if selected_status2 != 'No Filters':
            filtered_df = filtered_df[filtered_df['Status'] == selected_status2]

        st.divider()

        filtered_df['Date'] = pd.to_datetime(filtered_df['Date']).dt.strftime('%d %b %Y')
            
        try:
            if st.session_state.role == 'Administrator':

                cages_table = st.dataframe(filtered_df, width=1500, height=300, hide_index = True, selection_mode="single-row", on_select='rerun', key = ward_name, column_order=["Cage ID", "Cat ID", "Cat Name", "Date", "Status"], use_container_width=True)

                if cages_table["selection"]["rows"]:

                    cage_id_selected = result.iat[cages_table["selection"]["rows"][0],0]

                    code, blank, cage_no = cage_id_selected.split('-')
                    with engine.begin() as conn:
                        cage_id = conn.execute(sa.text("select cageID from Cage where cageNo = :cage_no and wardID = (select wardID from Ward where code = :code)"), {"cage_no":cage_no, "code":code}).fetchall()[0][0]
                        availability = pd.read_sql_query(sa.text("select cageStatus from cageStatus, cage where cageStatus.cageStatusID = Cage.cageStatusID and cageID = :id_to_delete"), conn, params = {"id_to_delete":cage_id}).iloc[0][0]

                    if availability == 'Free':
                        disabled_delete = False
                    else: 
                        disabled_delete = True

                    with col5:
                        update_button = col5.button("Transfer", key=str(index)+'update_cages', use_container_width=True)
                        if update_button:
                            st.session_state.show_update_cages_dialog = True
                            update_cages(cage_id, cage_id_selected, availability)

                    with col6:
                        delete_button = col6.button("Delete", key = str(index)+'delete_cages', use_container_width=True, disabled=disabled_delete)
                        
                        if delete_button:
                            st.session_state.show_delete_cages_dialog = True
                            delete_cages(cage_id, cage_id_selected)
            else:
                cages_table = st.dataframe(filtered_df, width=1500, height=300, hide_index = True, key = ward_name, column_order=["Cage ID", "Cat ID", "Cat Name", "Date", "Status"], use_container_width=True)
        except:
            pass

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

st.sidebar.write("Press 🛏️ *Wards* to fix the site.")

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