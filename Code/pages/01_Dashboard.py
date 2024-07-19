import streamlit as st
import pandas as pd
import plotly.express as px # for pie chart
from st_pages import Page, show_pages, add_page_title, hide_pages
from PIL import Image

import sqlalchemy as sa

# custom imports
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

# streamlit-authenticator package
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# database information ; will change when db hosting

# Note the double backslashes
# server = 'DESKTOP-67BT6TD\\FONTAINE' # IBAD
# server = 'DESKTOP-HT3NB74' # EMAN
server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA

database = 'PawRescue'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

st.set_page_config(page_title="Dashboard", page_icon="📊", initial_sidebar_state="expanded", layout="wide") # I think we should keep it wide and make it work this way? More information maybe or something.

# connectivity remains

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

show_pages(
    [
        Page("pages/01_Dashboard.py", "Dashboard", "📊"),
        Page("pages/02_Cats.py", "Cats", "🐾"),
        Page("pages/03_Treatments.py", "Treatments", "💊"),
        Page("pages/04_Wards.py", "Wards", "🛏️"),
        Page("pages/05_Finances.py", "Finances", "💰"),
        Page("LoginScreen.py", "Login", "🔐"),
        Page("pages/06_Teams.py", "Teams", "👥"),
    ]
)

hide_pages(["Login"])

# logo
logo = Image.open("assets/logo.png")
st.logo(logo)

#title
st.header("Dashboard" , divider='orange')

# Boxes

# Read the CSV file
df = pd.read_csv('assets/Cats_IDs.csv')

# Count the number of cats by status
status_counts = df['Status'].value_counts().to_dict()

# Calculate the values
total_cats_treated = len(df)
recovered = status_counts.get('Healthy in lower portion', 0) + status_counts.get('Move To healthy area', 0) + status_counts.get('Adopted', 0) + status_counts.get('Ready To discharge', 0)
expired = status_counts.get('Expired', 0)
discharged = status_counts.get('Discharged', 0)

# Creating columns
col1, col2, col3, col4 = st.columns(4)

# Create a container for each metric
with col1:
    with st.container( border= True):
        st.metric(label="Total Cats Treated", value=f"{total_cats_treated:,}")

with col2:
    with st.container(border= True):
        st.metric(label="Recovered", value=f"{recovered:,}")

with col3:
    with st.container(border= True):
        st.metric(label="Expired", value=f"{expired:,}")

with col4:
    with st.container(border= True):
        st.metric(label="Discharged", value=f"{discharged:,}")

# Donation graph

# Example data
data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "Donations": [5000, 7000, 10000, 22000, 15000, 17000, 11000, 5000, 16000, 14000, 15000, 13000]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create a container for the donation graph
with st.container(border = True,height= 500):
    
    # Title of the Streamlit app
    st.write("#### Donations Received Monthly")
    # Create a line chart using Plotly
    fig = px.line(
        df,
        x="Month",
        y="Donations",
        title= " ",
        markers=True,
        template="plotly_dark"
    )

    # Customize the chart to match the style in the image
    fig.update_traces(marker=dict(size=10, color="yellow"), line=dict(color="white", width=2))
    fig.update_layout(
        title_font_size=20,
        title_x=0.5,
        yaxis=dict(title="Donations", showgrid=False),
        xaxis=dict(title="Month", showgrid=False)
    )
    fig.update_yaxes(range=[0, 25000])

    # Display the chart in Streamlit
    st.plotly_chart(fig)

col5, col6 = st.columns(2)

# Cats pie chart

# Read the CSV file
df = pd.read_csv('assets/Cats_IDs.csv')

# Count the number of cats by status
status_counts = df['Status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']

# with col5:
#Contaier:
with st.container(border= True, height= 500):
    # Title of the Streamlit app
    st.write("#### Cats Status Summary")

    # Create a pie chart using Plotly
    fig = px.pie(status_counts, values='Count', names='Status')

    # Display the pie chart in Streamlit
    st.plotly_chart(fig)

# top reporter

# Load the CSV file
df = pd.read_csv('assets/Cats_IDs.csv')

# Group the data by Owner name and count the number of cats
owner_counts = df['Owner name'].value_counts().reset_index()
owner_counts.columns = ['Name', 'Number of Cats']

# Get the top 5 owners
top_owners = owner_counts.head(5)

# with col6:
with st.container(border= True):
    st.write("#### Top 5 Owners/ Reporters")
    st.dataframe(top_owners,hide_index = True, width= 700)

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

with engine.connect() as conn:
    role = conn.execute(sa.text("select roleDesc from InternalRole, Users where Users.internalRoleID = InternalRole.internalRoleID and Users.userName = :name"), {"name":name}).fetchone()[0]

st.sidebar.write(f"Role: _:orange[{role}]_")

if st.sidebar.button("🔓 Logout"):
    authenticator.logout(location = "unrendered")
    st.switch_page("LoginScreen.py")