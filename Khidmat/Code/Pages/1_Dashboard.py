import streamlit as st
import pandas as pd
import plotly.express as px # for pie chart

st.write("# DashBoard!")

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
