# Paw Rescue Management System

**Paw Rescue Management System** is a comprehensive database-driven web application designed to assist the NGO Paw Rescue in managing their operations.

## Technologies Used

- **Frontend**: Streamlit (Python-based web app framework)
- **Backend**: Python
- **Database**: MSSQL Server

## Installation

### Prerequisites

- MSSQL Server installed and configured ([Download here](https://www.microsoft.com/en-us/sql-server/sql-server-downloads))
- Python installed (Version 3.8 or higher)
- Required Python libraries installed

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/EmanFatimaa/Khidmat.git
   ```

2. **Start MSSQL Server**:
   - Open MSSQL Server and run the `SchemaPawRescue.sql` file provided in the `BuildDB` Folder.
   - Alternatively, you can use the `DummyPawRescue.sql` file to populate the tables with some sample data.
   - If MSSQL Server is not installed, download and install it from [here](https://www.microsoft.com/en-us/sql-server/sql-server-downloads).

3. **Change the server name**:
   - Update the server name in all Python files in the `Code` and `pages` Folder to match the server name your computer is using.

4. **Install Python and libraries**:
   - Download and install Python (if not already installed).
   - Navigate to the `Khidmat` Folder and install the required libraries by running the command:
     ```bash
     pip install -r requirements.txt
     ```

5. **Run the application**:
   - Navigate to the `Code` Folder which contains the Python files.
   - Run the following command to start the application:
     ```bash
     streamlit run LoginScreen.py
     ```

6. **Login to the application**:
   - Use the following dummy credentials to log in:
     - **Username**: Ahmed Bilal
     - **Password**: bilal

## Features

- **Rescue Operations Management**: Track and update details of rescued animals, including species, medical condition, and assigned caretaker.

- **Interactive Dashboard**: Visualize key metrics such as number of rescues, adoptions, and donations.

- **User Roles**: Secure login for admins, doctors, and nurse with role-based access control.

- **Adoption Records**: Manage adoption requests, approvals, and post-adoption follow-ups.

- **Donor Contributions**: Track donations with details about donors and contribution amounts.