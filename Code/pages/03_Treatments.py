# standard imports 
from datetime import datetime, date, time  # Correct import
from PIL import Image

# third party imports
import sqlalchemy as sa
import streamlit as st
import pandas as pd

# custom imports
from millify import prettify
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

# custom streamlit imports
from st_pages import Page, show_pages, add_page_title, hide_pages

# server = 'DESKTOP-67BT6TD\\FONTAINE' # IBAD
server = 'DESKTOP-HT3NB74' # EMAN
# server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA # Note the double backslashes

database = 'PawRescue'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

st.set_page_config(page_title="Treatments", page_icon="💊", initial_sidebar_state="expanded", layout="wide")

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

if st.sidebar.button("🔓 Logout"):
    st.experimental_rerun("LoginScreen.py")

hide_pages(["Login"])

# Creating columns for better formatting
col1, col2, col3, col4 = st.columns(4)

st.header("Treatment", divider='orange')

def add_treatment_dialog():
    st.session_state.show_add_treatment_dialog = True
    st.session_state.show_update_treatment_dialog = False
    st.session_state.show_delete_treatment_dialog = False

def update_treatment_dialog():
    st.session_state.show_add_treatment_dialog = False
    st.session_state.show_update_treatment_dialog = True
    st.session_state.show_delete_treatment_dialog = False

def delete_treatment_dialog():
    st.session_state.show_add_treatment_dialog = False
    st.session_state.show_update_treatment_dialog = False
    st.session_state.show_delete_treatment_dialog = True

@st.experimental_dialog("Add Treatment")
def add_treatment():
    print("adding")
    with engine.begin() as conn:
        treatmentid = int(pd.read_sql_query(sa.text("SELECT TOP 1 treatmentID FROM Treatment ORDER BY treatmentID DESC"), conn).iat[0,0]) + 1
        df = pd.read_sql_query("SELECT CatID FROM Cats", conn)
        cat_ids = df['CatID'].tolist()

    col1, col2 = st.columns(2)
    with col1:
        selected_cat_id = st.selectbox("Select Cat ID", cat_ids)
    with col2:
        id = st.text_input("Treatment ID", value=treatmentid, disabled=True)

    col1, col2 = st.columns(2)
    
    with col1:
        treatment_time = st.time_input("Time")
    
    with col2:
        treatment_date = st.date_input("Treatment Date") 

    col1, col2 = st.columns(2)
    with col1:
        temperature = st.text_input("Temperature", value=float(100))
    with col2:
        with engine.begin() as conn:
            df = pd.read_sql_query("SELECT userName FROM Users", conn)
            user = df['userName'].tolist()
        givenby = st.selectbox("Given By", user)
    
    treatment_details = st.text_area("Treatment Details", placeholder="IV given, dressing done", value = '')

    add_treatment_button = st.button("Add Treatment", key="add_treatment")

    if add_treatment_button:
        print("button pressed")
        # check other individual fields for errors as well.
        everything_filled = False
        valid_treatment =   False

        if all(x.isalpha() or x.isspace() or x=='.' for x in treatment_details):
            valid_treatment = True
        else:
            st.error("Please enter valid treatment details.")

        # Check if any of the fields are left unfilled
        if not (id and selected_cat_id and treatment_time and temperature and givenby and treatment_date and treatment_details):
            st.error("Please fill in all fields before submitting.")
        else: 
            date_and_time = datetime.combine(treatment_date, treatment_time)
            everything_filled = True

        if everything_filled and valid_treatment:
            with engine.begin() as conn:
                userid = conn.execute(sa.text("""SELECT UserID FROM Users WHERE userName = :userName"""), {"userName": givenby}).fetchone()[0] 
                conn.execute(sa.text("""
                    INSERT INTO Treatment (TreatmentID, CatID, UserID, DateTime, Temperature, Treatment)
                    VALUES (:treatmentID, :CatID, :UserID, :DateTime, :Temperature, :Treatment)
                """), {
                    "treatmentID": treatmentid,
                    "CatID": selected_cat_id,
                    "UserID" : userid,
                    "DateTime": date_and_time,
                    "Temperature": temperature,
                    "Treatment": treatment_details              
                })
            st.rerun()
    
    st.session_state.show_add_treatment_dialog = False
    st.caption('_:orange[Press Esc to Cancel]_')

@st.experimental_dialog("Update Treatment")
def update_treatment(ID_to_update):
    with engine.begin() as conn:
        df = pd.read_sql_query("SELECT CatID FROM Cats", conn)
        cat_ids = df['CatID'].tolist()

    col1, col2 = st.columns(2)
    with col1:
        treat_id =st.text_input("TreatmentID", value=ID_to_update, disabled=True)
    with col2:
        with engine.begin() as conn:
            current_catID = int(conn.execute(sa.text("select catId from Treatment where treatmentid = :t"), {"t":ID_to_update}).fetchall()[0][0])
            # print(current_catID)
        selected_cat_id = st.selectbox("Select Cat ID", cat_ids, index = current_catID - 1)

    col1, col2 = st.columns(2)
        
    with col1:
        with engine.begin() as conn:
            time_value = conn.execute(sa.text("select dateTime from Treatment where treatmentID = :treatmentID"), {"treatmentID": ID_to_update}).fetchall()[0][0]
        time_only = time_value.time()
        Time = st.time_input("Time", value=time_only)
    
    with col2:
        with engine.begin() as conn:
            date_value = conn.execute(sa.text("select convert(date, dateTime) from Treatment where treatmentID = :treatmentID"), {"treatmentID": ID_to_update}).fetchall()[0][0]
        date = st.date_input("Date", value=date_value)

    col1, col2 = st.columns(2)
        
    with col1:
        with engine.begin() as conn:
            temp_value = conn.execute(sa.text("select temperature from Treatment where treatmentID = :treatmentID"), {"treatmentID": ID_to_update}).fetchall()[0][0]
        temperature = st.number_input("Temperature", value=float(temp_value))
    
    with col2:
        with engine.begin() as conn:
            # current_givenby = conn.execute(sa.text("select mode from Mode where modeID = (select modeID from Donations where treatmentID = :t)"), {"t": ID_to_update}).fetchall()[0][0]
            user_value = conn.execute(sa.text("select userName from Users where userID = (select userID from Treatment where treatmentID = :treatmentID)"), {"treatmentID": ID_to_update}).fetchall()[0][0]
            df = pd.read_sql_query("SELECT userName FROM Users", conn)
            update_user = df['userName'].tolist()
        final_user_index = update_user.index(user_value)
        # print(final_user_index)
        user = st.selectbox("Given By", update_user, index = final_user_index)

            # with engine.begin() as conn:
            #     donation_mode = pd.read_sql_query(sa.text("select mode from Mode"), conn)
            #     mode_value = conn.execute(sa.text("select mode from Mode where modeID = (select modeID from Donations where donationID = :donationID)"), {"donationID": id_to_update}).fetchall()[0][0]
            #     final_mode_value = 1 if mode_value == 'Cash' else 0
            # mode = st.selectbox("Donation Mode", donation_mode["mode"].tolist(), index = final_mode_value)

        with engine.begin() as conn:
            Userid = conn.execute(sa.text("""SELECT UserID FROM Users WHERE userName = :userName"""), {"userName": user}).fetchall()[0][0]

    with engine.begin() as conn:
        treatment_value = conn.execute(sa.text("select treatment from Treatment where treatmentID = :treatmentID"), {"treatmentID": ID_to_update}).fetchall()[0][0]
    treatment = st.text_area("Treatment Details", value=treatment_value)

    update_treatment_button = st.button("Save Changes", key = 'update_treatment')


    if update_treatment_button:
        # check other individual fields for errors as well.
        everything_filled = False
        valid_treatment_details =   False
        
        if all(x.isalpha() or x.isspace() or x=='.' for x in treatment):
            valid_treatment_details = True
        else:
            st.error("Please enter valid treatment details for updation.")

        if not (treat_id and selected_cat_id and Time and date and user and temperature and treatment):
            st.error("Please fill in all fields before submitting.")
        else:
            date_and_time = datetime.combine(date, Time)
            everything_filled = True

        if everything_filled and valid_treatment_details:
            # print(selected_cat_id, Userid, Time, temperature, treatment, ID_to_update)
            with engine.begin() as conn:
                conn.execute(sa.text(""" 
                    UPDATE Treatment
                    SET catID = :catID, userID = :userID, dateTime = :dateTime, temperature = :temperature, treatment = :treatment
                    WHERE treatmentID = :treatmentID
                    """), {"catID": selected_cat_id, "userID": Userid, "dateTime": date_and_time, "temperature": temperature, "treatment": treatment, "treatmentID": ID_to_update})
            st.rerun()

    st.session_state.show_update_treatment_dialog = False  
    st.caption('_:orange[Press Esc to Cancel]_')


@st.experimental_dialog("Delete Treatment")
def delete_treatment(Id_to_delete):
    st.write('Are you sure you want to delete treatment of ID:', Id_to_delete, '?')

    col1, col2 = st.columns(2)
    if col1.button("Yes"):
        with engine.begin() as conn:
            # conn.execute(sa.text("update Treatment set catID = NULL, temperature = NULL, dateTime = NULL, treatment = NULL FROM Treatment where treatmentID = :treatmentID"), {"treatmentID": Id_to_delete})
            conn.execute(sa.text("update Treatment set catID = NULL, userID = NULL, dateTime = NULL, temperature = NULL, treatment = NULL where treatmentID = :treatmentID"), {"treatmentID": Id_to_delete})
        st.rerun()

    if col2.button("No", key = 'no'):
        st.rerun()

    st.session_state.show_delete_treatment_dialog = False
    st.caption('_:orange[Press Esc to Cancel]_') 

col1, col2, col3, col4, col5, col6 = st.columns(6)

if 'show_add_treatment_dialog' not in st.session_state:
    st.session_state.show_add_treatment_dialog = False
if 'show_update_treatment_dialog' not in st.session_state:
    st.session_state.show_update_treatment_dialog = False
if 'show_delete_treatment_dialog' not in st.session_state:
    st.session_state.show_delete_treatment_dialog = False

# Table for treatments
with engine.begin() as conn:
    treatment_table_df = pd.read_sql_query(sa.text("""
    SELECT 
        treatmentID as TreatmentID,
        Cats.CatID, 
        Cats.CatName AS Name, 
        Cats.CageID AS CageNo, 
        Treatment.Temperature AS Temperature, 
        Treatment.Treatment AS Treatment, 
        CONVERT(VARCHAR, Treatment.DateTime, 108) AS Time, 
        convert(date, dateTime) as Date,
        Users.UserName AS GivenBy
    FROM 
        Cats
    INNER JOIN 
        Treatment ON Treatment.CatID = Cats.CatID
    INNER JOIN 
        Users ON Treatment.UserID = Users.UserID
    """), conn)


#  Filtering and Final Table
st.write("Filters")

# Add a New treatment Button
st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)
new_treatment = col6.button("✙ Add Treatment", on_click = add_treatment_dialog)

if st.session_state.show_add_treatment_dialog:
    add_treatment()

# Display the Table
treatment_table = st.dataframe(treatment_table_df, width=1500, height=600, hide_index = True, on_select = "rerun", selection_mode = "single-row") 

if treatment_table["selection"]["rows"]: # if a row is selected
        
        row_selected = int(treatment_table_df.iat[treatment_table['selection']['rows'][0], 0])
        # print(treatment_table_df)

        update_button = col4.button("Update Treatment", on_click = update_treatment_dialog)
        delete_button = col5.button("Delete Treatment", on_click = delete_treatment_dialog)

        if st.session_state.show_update_treatment_dialog:
            update_treatment(row_selected)

        if st.session_state.show_delete_treatment_dialog:
            delete_treatment(row_selected)

else:
    print("No row selected")