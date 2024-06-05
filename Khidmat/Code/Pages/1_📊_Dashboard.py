import streamlit as st
import pandas as pd
import plotly.express as px # for pie chart

#LOGO GOES HERE -- sidebar..
from PIL import Image
img= Image.open("logo.png")
st.logo(img )

# Custom CSS for centering text
st.markdown(
    """
    <style>
    .center-text {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Using HTML within st.markdown to center-align text
st.markdown("<h1 class='center-text'>Dashboard</h1>", unsafe_allow_html=True)

###############################
#Boxes
# Read the CSV file
df = pd.read_csv('Cats IDs.csv')

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


# # Display the dataframe for verification (optional)
# st.write("## Data Preview")
# st.dataframe(df)

###############################
## BAR GRAPH
# # Read the cleaned CSV data
# df = pd.read_csv('Donations.csv')
# # st.write(df)
# # Convert 'Date' column to datetime format
# df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# # Extract month from 'Date' column
# df['Month'] = df['Date'].dt.strftime('%b')

# # Group by month and sum the donations
# monthly_donations = df.groupby('Month')['Amount'].sum().reset_index()

# # Display bar chart
# st.write("## Donations Received Monthly")
# st.bar_chart(monthly_donations.set_index('Month')['Amount'])
########################

##PIE CHART
# st.write("## Donations Received Monthly")

# # Read the cleaned CSV data
# df = pd.read_csv('Donations.csv')

# # Convert 'Date' column to datetime format
# df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# # Extract month from 'Date' column
# df['Month'] = df['Date'].dt.strftime('%b')

# # Group by month and sum the donations
# monthly_donations = df.groupby('Month')['Amount'].sum().reset_index()

# # Create a pie chart using Plotly Express
# fig = px.pie(monthly_donations, values='Amount', names='Month')

# # Customize the layout
# fig.update_traces(textinfo='percent+label')  # Add percentage labels to the pie chart

# # Display the pie chart in Streamlit
# st.plotly_chart(fig)

############################

# # Filter the DataFrame to show only "Expired" cats
# expired_count = status_counts[status_counts['Status'] == 'Expired']['Count'].values[0]

# # Display the dataframe for verification (optional)
# st.write("## Data Preview")
# st.write(f"❃Number of cats who got expired: {expired_count}")

# ############

# # Count the number of cats by status
# status_counts = df['Status'].value_counts().reset_index()
# status_counts.columns = ['Status', 'Count']

# # Display the counts for each status
# for index, row in status_counts.iterrows():
#     st.write(f"❃{row['Status']}: {row['Count']}")

# # Create a bar chart using Plotly
# fig = px.bar(status_counts, x='Status', y='Count', title='Cats Status Distribution', text='Count')

# # Display the bar chart in Streamlit
# st.plotly_chart(fig)


###########################
##DONATION GRAPH":

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
    st.write("#### Donations Receive Monthly")
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
###########################
# CATS PIE CHART

# Read the CSV file
df = pd.read_csv('Cats IDs.csv')

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

############
#TOP REPORTER:

# Load the CSV file
df = pd.read_csv('Cats IDs.csv')

# Group the data by Owner name and count the number of cats
owner_counts = df['Owner name'].value_counts().reset_index()
owner_counts.columns = ['Name', 'Number of Cats']

# Get the top 5 owners
top_owners = owner_counts.head(5)

# with col6:
with st.container(border= True):
    st.write("#### Top 5 Owners/ Reporters")
    st.dataframe(top_owners,hide_index = True, width= 700)

