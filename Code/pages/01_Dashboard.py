#standard imports
from PIL import Image
import time
from datetime import datetime, timedelta

# third party imports
import pandas as pd
import streamlit as st
import sqlalchemy as sa
import plotly.express as px # for pie chart

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
# server = 'DESKTOP-67BT6TD\\FONTAINE' # IBAD
server = 'DESKTOP-HT3NB74' # EMAN
# server = 'DESKTOP-HPUUN98\SPARTA' # FAKEHA

database = 'DummyPawRescue'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url)

st.set_page_config(page_title="Dashboard", page_icon="📊", initial_sidebar_state="expanded" ,layout = "wide")

# logo
logo = Image.open("assets/logo.png")
st.logo(logo)

# def implement_markdown():
#     # Button Styling
#     st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)

#     # fix the sidebar width
#     st.markdown(
#             """
#         <style>
#         [data-testid="stSidebar"][aria-expanded="true"]{
#             min-width: 250px;
#             max-width: 250px;
#         }
#         """,
#             unsafe_allow_html=True,
#     )

#     st.sidebar.markdown(""" <style> [data-testid='stSidebarNav'] > ul { min-height: 54vh; } </style> """, unsafe_allow_html=True) 

# # ----------------------------------------------------------------- #

# implement_markdown()

# show_pages(
#     [
#         Page("pages/01_Dashboard.py", "Dashboard", "📊"),
#         Page("pages/02_Cats.py", "Cats", "🐾"),
#         Page("pages/03_Treatments.py", "Treatments", "💊"),
#         Page("pages/04_Wards.py", "Wards", "🛏️"),
#         Page("pages/05_Finances.py", "Finances", "💰"),
#         Page("LoginScreen.py", "Login", "🔐"),
#         Page("pages/06_Teams.py", "Teams", "👥"),
#     ]
# )

# hide_pages(["Login"])

# #title
# st.header("Dashboard" , divider='orange')

# # Creating columns
# col1, col2, col3, col4 = st.columns(4)

# with col1: # fixed
#     with st.container( border = True):
#         with engine.begin() as conn:
#             total_cats_treated = pd.read_sql_query(sa.text("select count(*) from cats"), conn)
#         st.metric( label = "Total cats admitted", value = prettify(int(total_cats_treated.iat[0,0] )))

# with col2: # fixed
#     with st.container( border = True): 
#         with engine.begin() as conn:
#             total_cats_recovered = pd.read_sql_query(sa.text("select count( CATS.statusID) as 'Total Cats recovered' from Cats join CatStatus on cats.statusID = CatStatus.statusID where cats.statusID in (2, 3, 4, 6, 8, 11)"), conn)
#         st.metric( label = "Recovered",value = prettify(int(total_cats_recovered.iat[0,0] )))

# with col3: # status id = 1
#     with st.container( border = True):
#         with engine.begin() as conn:
#             total_cats_expired = pd.read_sql_query(sa.text("select count( CATS.statusID) as 'Total Cats expired' from Cats join CatStatus on cats.statusID = CatStatus.statusID where cats.statusID  = 1"), conn)
#         st.metric( label = "Expired", value = prettify(int(total_cats_expired.iat[0,0] )))
       
# with col4: # status id = 4
#     with st.container( border = True):
#         with engine.begin() as conn:
#             total_cats_discharged = pd.read_sql_query(sa.text("select count( CATS.statusID) as 'Total Cats discharged' from Cats join CatStatus on cats.statusID = CatStatus.statusID where cats.statusID = 4"), conn)
#         st.metric( label = "Discharged", value = prettify(int(total_cats_discharged.iat[0,0] )))

# # st.info("Need to confirm the logic for these metrics, abhi tak have done jo samjh aya..")

# # Donation graph
# with engine.begin() as conn:
#     jan = conn.execute(sa.text("select sum(amount) from donations where month(date) = 1")).fetchall()[0][0]
#     feb = conn.execute(sa.text("select sum(amount)  from donations where month(date) = 2")).fetchall()[0][0]
#     march = conn.execute(sa.text("select sum(amount)  from donations where month(date) = 3")).fetchall()[0][0]
#     april = conn.execute(sa.text("select sum(amount)  from donations where month(date) = 4")).fetchall()[0][0]
#     may = conn.execute(sa.text("select sum(amount)  from donations where month(date) = 5")).fetchall()[0][0]
#     june = conn.execute(sa.text("select sum(amount)  from donations where month(date) = 6")).fetchall()[0][0]
#     july = conn.execute(sa.text("select sum(amount)  from donations where month(date) = 7")).fetchall()[0][0]
#     aug = conn.execute(sa.text("select sum(amount)  from donations where month(date) = 8")).fetchall()[0][0]
#     sep = conn.execute(sa.text("select sum(amount)  from donations where month(date) = 9")).fetchall()[0][0]
#     oct = conn.execute(sa.text("select sum(amount)  from donations where month(date) = 10")).fetchall()[0][0]
#     nov = conn.execute(sa.text("select sum(amount)  from donations where month(date) = 11")).fetchall()[0][0]
#     dec = conn.execute(sa.text("select sum(amount)  from donations where month(date) = 12")).fetchall()[0][0]

# lstDonations = [jan, feb, march, april, may, june, july, aug, sep, oct, nov, dec]

# # Iterate over the list and replace None values with 0
# for i in range(len(lstDonations)):
#     if lstDonations[i] is None:
#         lstDonations[i] = 0

# max = max(lstDonations)
# # print(max)

# # # Print each element in the list
# # for donation in lstDonations:
# #     print(donation)

# data = {
#     "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
#     "Donations": lstDonations
# }

# # Create a DataFrame
# df = pd.DataFrame(data)

# # Create a container for the donation graph
# with st.container(border = True,height= 570):
    
#     # Title of the Streamlit app
#     st.write("#### :white[Donations Received Monthly]")
#     # Create a line chart using Plotly
#     fig = px.line(
#         df,
#         x="Month",
#         y="Donations", #  title= " ",
#         markers=True,
#         template="plotly_dark"
#     )

#     # Customize the chart to match the style in the image
#     fig.update_traces(marker=dict(size=10, color="yellow"), line=dict(color="white", width=2))
#     fig.update_layout(
#         yaxis=dict(
#         title="Donations",
#         showgrid=False,
#         showline=True,  # Add this line to show the y-axis line
#         linecolor="grey",  # Color of the y-axis line
#         linewidth= 1.9  # Width of the y-axis line
#         ),
#         xaxis=dict(
#         title="Month",
#         showgrid=False
#         )

#         # title_font_size=20,
#         # title_x=0.5,
#         # yaxis=dict(title="Donations", showgrid=False),
#         # xaxis=dict(title="Month", showgrid=False)
#     )
#     fig.update_yaxes(range=[0, max+ (max/2)])

#     # Display the chart in Streamlit
#     st.plotly_chart(fig)

# col5, col6 = st.columns(2)

# # Cats pie chart

# # SQL query to fetch data
# catsQuery = """
# select count(cats.statusID) as 'Count', statusType
# from cats join CatStatus 
# on cats.statusID = CatStatus.StatusID
# group by cats.statusID, statusType
# """

# # Fetch data from the database into a Pandas DataFrame
# with engine.begin() as conn:
#     status_df= pd.read_sql_query(sa.text(catsQuery), conn)
# # print(status_df)

# # Streamlit container
# with st.container(border=True, height=570):

#     #Title
#     st.write("#### :white[Cats Status Summary]")

#     # Create the pie chart
#     fig = px.pie(status_df, values='Count', names='statusType')
#     st.plotly_chart(fig)

# # Top reporter
# query = """
# select top 5 name as 'Name', count (catID) as 'Count' 
# from cats join Externals
# on cats.externalID = externals.externalID
# where cats.externalID is not NULL
# GROUP BY cats.externalID, name
# order by count(catID) desc
# """
# with engine.begin() as conn:
#     reporter_table = pd.read_sql_query(sa.text(query), conn)
# # print(reporter_table)
# reporter_table.columns = ['Name','Number of Cats' ]

# with st.container(border=True):
#     st.write("#### :white[Top 5 Owners/ Reporters]")
#     st.dataframe(reporter_table, hide_index=True, width=1000)

#     # st.info("What if multiple owners with count as 1... kis basis pe top choose krna hai phir")

# # Login - Logout
# with open('../config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['pre-authorized']
# )

# name, logged_in, user_name = authenticator.login()

# st.sidebar.write(f"Logged in as: _:orange[{name}]_")

# if name is not None:
#     with engine.connect() as conn:
#         role = conn.execute(sa.text("select roleDesc from InternalRole, Users where Users.internalRoleID = InternalRole.internalRoleID and Users.userName = :name"), {"name":name}).fetchone()[0]        
#     st.sidebar.write(f"Role: _:orange[{role}]_")
# else:
#     st.switch_page("LoginScreen.py")

# # empty
# st.sidebar.write(" ")
# st.sidebar.write(" ")
# st.sidebar.write(" ")

# if st.sidebar.button("🔓 Logout"):
#     with st.sidebar:
#         with st.spinner('Logging out...'):
#             time.sleep(2)

#     authenticator.logout(location = "unrendered")
#     st.switch_page("LoginScreen.py")

# TODO:
# Autoscale the y-axis of the donation graph
# Need a Filter for the whole Dashboard. Week, Month, 3-Month, Year.

#-------------------------------------------------------------------------

def implement_markdown():
    # Button Styling
    st.markdown('<style>div.stButton > button:first-child {background-color: #FFA500; color: black}</style>', unsafe_allow_html=True)

    # Fix the sidebar width
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

    st.sidebar.markdown(""" <style> [data-testid='stSidebarNav'] > ul { min-height: 54vh; } </style> """, unsafe_allow_html=True) 

# Implement styling
implement_markdown()

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

# Title
st.header("Dashboard", divider='orange')

#NEWW ADDITION
# Filter selection
time_filter = st.selectbox(":orange[Select Time Period:]", ["Last Week", "Last Month", "Last Six Months","Last Year"])


end_date = datetime.now()

# Calculate date range based on selection
if time_filter == "Last Week":
    start_date = end_date - timedelta(days=7)
elif time_filter == "Last Month":
    start_date = end_date - pd.DateOffset(months=1)
elif time_filter == "Last Six Months":
    start_date = end_date - pd.DateOffset(months=6)
elif time_filter == "Last Year":
    start_date = end_date - pd.DateOffset(years=1)

# Create columns for metrics
col1, col2, col3, col4 = st.columns(4)

# Fetch metrics based on the selected time period
with col1:  # fixed
    with st.container(border=True):
        with engine.begin() as conn:
            total_cats_treated = pd.read_sql_query(
                sa.text("select count(*) from cats where admittedOn >= :start_date"),
                conn,
                params={"start_date": start_date}
            )
        st.metric(label="Total cats admitted", value=prettify(int(total_cats_treated.iat[0, 0])))

with col2:  # fixed
    with st.container(border=True):
        with engine.begin() as conn:
            total_cats_recovered = pd.read_sql_query(
                sa.text("select count(CATS.statusID) as 'Total Cats recovered' from Cats join CatStatus on cats.statusID = CatStatus.statusID where cats.statusID in (2, 3, 4, 6, 8, 11) and admittedOn >= :start_date"),
                conn,
                params={"start_date": start_date}
            )
        st.metric(label="Recovered", value=prettify(int(total_cats_recovered.iat[0, 0])))

with col3:  # status id = 1
    with st.container(border=True):
        with engine.begin() as conn:
            total_cats_expired = pd.read_sql_query(
                sa.text("select count(CATS.statusID) as 'Total Cats expired' from Cats join CatStatus on cats.statusID = CatStatus.statusID where cats.statusID  = 1 and admittedOn >= :start_date"),
                conn,
                params={"start_date": start_date}
            )
        st.metric(label="Expired", value=prettify(int(total_cats_expired.iat[0, 0])))

with col4:  # status id = 4
    with st.container(border=True):
        with engine.begin() as conn:
            total_cats_discharged = pd.read_sql_query(
                sa.text("select count(CATS.statusID) as 'Total Cats discharged' from Cats join CatStatus on cats.statusID = CatStatus.statusID where cats.statusID = 4 and admittedOn >= :start_date"),
                conn,
                params={"start_date": start_date}
            )
        st.metric(label="Discharged", value=prettify(int(total_cats_discharged.iat[0, 0])))
#--------
# # Donation graph
# with engine.begin() as conn:
#     donations_query = """
#     select month(date) as Month, sum(amount) as Total
#     from donations
#     where date >= :start_date
#     group by month(date)
#     order by month(date)
#     """
#     donations_data = pd.read_sql_query(sa.text(donations_query), conn, params={"start_date": start_date})

# # Fill missing months with 0 donations
# donations_data = donations_data.reindex(range(1, 13), fill_value=0)
# donations_data.columns = ["Month", "Donations"]

# # Create a container for the donation graph
# with st.container(border=True, height=570):
#     st.write("#### :white[Donations Received Monthly]")
#     fig = px.line(
#         donations_data,
#         x="Month",
#         y="Donations",
#         title= " ",
#         markers=True,
#         template="plotly_dark"
#     )

#     # Customize the chart
#     fig.update_traces(marker=dict(size=10, color="yellow"), line=dict(color="white", width=2))
#     fig.update_layout(
#         yaxis=dict(title="Donations", showgrid=False, showline=True, linecolor="grey", linewidth=1.9),
#         xaxis=dict(title="Month", showgrid = False),
#         title_font_size = 20,
#         title_x = 0.5
#     )
#     # fig.update_yaxes(range=[ 0, max +(max/2)])
    
#     st.plotly_chart(fig)
#-------

with engine.begin() as conn:
    donations_query = """
    select month(date) as Month, sum(amount) as Total
    from donations
    where date >= :start_date
    group by month(date)
    order by month(date)
    """
    donations_data = pd.read_sql_query(sa.text(donations_query), conn, params={"start_date": start_date})

# Fill missing months with 0 donations
full_months = pd.DataFrame({"Month": range(1, 13)})  # All months from 1 (Jan) to 12 (Dec)
donations_data = pd.merge(full_months, donations_data, on="Month", how="left").fillna(0)

# Map the Month numbers to short month names
donations_data["Month"] = donations_data["Month"].apply(lambda x: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][x-1])

# Create a container for the donation graph
with st.container(border=True, height=570):
    st.write("#### :white[Donations Received Monthly]")
    fig = px.line(
        donations_data,
        x="Month",
        y="Total",
        markers=True,
        template="plotly_dark"
    )

    # Customize the chart to match the style in CODE 1
    fig.update_traces(marker=dict(size=10, color="yellow"), line=dict(color="white", width=2))
    fig.update_layout(
        yaxis=dict(title="Donations", showgrid=False, showline=True, linecolor="grey", linewidth=1.9),
        xaxis=dict(title="Months", showgrid=False),
    )
    
    # Adjust y-axis range similar to CODE 1
    # max_donations = donations_data["Total"].max()
    # fig.update_yaxes(range=[0, max_donations + (max_donations / 2)])

    # Display the chart in Streamlit
    st.plotly_chart(fig)

col5, col6 = st.columns(2)

# Cats pie chart
catsQuery = """
select count(cats.statusID) as 'Count', statusType
from cats join CatStatus 
on cats.statusID = CatStatus.StatusID
where admittedOn >= :start_date
group by cats.statusID, statusType
"""
with engine.begin() as conn:
    status_df = pd.read_sql_query(sa.text(catsQuery), conn, params={"start_date": start_date})

# Streamlit container
with st.container(border=True, height=570):
    st.write("#### :white[Cats Status Summary]")
    fig = px.pie(status_df, values='Count', names='statusType')
    st.plotly_chart(fig)

# Top reporter
query = """
select top 5 name as 'Name', count (catID) as 'Count' 
from cats join Externals
on cats.externalID = externals.externalID
where cats.externalID is not NULL and admittedOn >= :start_date
GROUP BY cats.externalID, name
order by count(catID) desc
"""
with engine.begin() as conn:
    reporter_table = pd.read_sql_query(sa.text(query), conn, params={"start_date": start_date})

reporter_table.columns = ['Name', 'Number of Cats']

with st.container(border=True):
    st.write("#### :white[Top 5 Owners/ Reporters]")
    st.dataframe(reporter_table, hide_index=True, width=1000)

# Login - Logout
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
        role = conn.execute(sa.text("select roleDesc from InternalRole, Users where Users.internalRoleID = InternalRole.internalRoleID and Users.userName = :name"), {"name": name}).fetchone()[0]
    st.sidebar.write(f"Role: _:orange[{role}]_")
else:
    st.switch_page("LoginScreen.py")

# Empty space in sidebar
st.sidebar.write(" ")
st.sidebar.write(" ")

if st.sidebar.button("🔓 Logout"):
    with st.sidebar:
        with st.spinner('Logging out...'):
            time.sleep(2)

    authenticator.logout(location="unrendered")
    st.switch_page("LoginScreen.py")

# TODO:
# Autoscale the y-axis of the donation graph
# Need a Filter for the whole Dashboard. Week, Month, 3-Month, Year.