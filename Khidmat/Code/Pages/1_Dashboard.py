import streamlit as st
import pandas as pd
import plotly.express as px # for pie chart

# st.write("# DashBoard!")

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
st.markdown("<h1 class='center-text'>DashBoard</h1>", unsafe_allow_html=True)

###############################
# Read the cleaned CSV data
df = pd.read_csv('Donations.csv')
# st.write(df)
# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# Extract month from 'Date' column
df['Month'] = df['Date'].dt.strftime('%b')

# Group by month and sum the donations
monthly_donations = df.groupby('Month')['Amount'].sum().reset_index()

# Display bar chart
st.write("## Donations Received Monthly")
st.bar_chart(monthly_donations.set_index('Month')['Amount'])
########################

st.write("## Donations Received Monthly")

# Read the cleaned CSV data
df = pd.read_csv('Donations.csv')

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# Extract month from 'Date' column
df['Month'] = df['Date'].dt.strftime('%b')

# Group by month and sum the donations
monthly_donations = df.groupby('Month')['Amount'].sum().reset_index()

# Create a pie chart using Plotly Express
fig = px.pie(monthly_donations, values='Amount', names='Month')

# Customize the layout
fig.update_traces(textinfo='percent+label')  # Add percentage labels to the pie chart

# Display the pie chart in Streamlit
st.plotly_chart(fig)

###########################

# CATS Status summary:

# Title of the Streamlit app
st.write("## Cats Status Summary")

# Read the CSV file
df = pd.read_csv('Cats.csv')

# Count the number of cats by status
status_counts = df['Status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']

# Create a pie chart using Plotly
fig = px.pie(status_counts, values='Count', names='Status', title='Cats Status Distribution')

# Display the pie chart in Streamlit
st.plotly_chart(fig)

# Filter the DataFrame to show only "Expired" cats
expired_count = status_counts[status_counts['Status'] == 'Expired']['Count'].values[0]

# Display the dataframe for verification (optional)
st.write("## Data Preview")
st.write(f"❃Number of cats who got expired: {expired_count}")

############

# Count the number of cats by status
status_counts = df['Status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']

# Display the counts for each status
for index, row in status_counts.iterrows():
    st.write(f"❃{row['Status']}: {row['Count']}")

# Create a bar chart using Plotly
fig = px.bar(status_counts, x='Status', y='Count', title='Cats Status Distribution', text='Count')

# Display the bar chart in Streamlit
st.plotly_chart(fig)
