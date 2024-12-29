
# Paw Rescue Management System

**Paw Rescue Management System** is a comprehensive database-driven web application designed to assist the NGO Paw Rescue in managing their operations.

## Technologies Used

- **Frontend**: Streamlit (Python-based web app framework)
- **Backend**: Python
- **Database**: MSSQL Server

## Installation

### Prerequisites

- MSSQL Server installed and configured
  - Windows: [Download here](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)
  - Linux: Follow the steps below under Linux Installation
- Python installed (Version 3.8 or higher)
- Required Python libraries installed

---

### Installation for Windows

1. **Clone the repository**:
   ```bash
   git clone https://github.com/EmanFatimaa/Khidmat.git
   ```

2. **Install Python and libraries**:
   - Download and install Python (if not already installed).
   - Navigate to the `Khidmat` folder and install the required libraries by running:
     ```bash
     pip install -r requirements.txt
     ```
   
3. **Start MSSQL Server**:
   - Create a new database named `SchemaPawRescue`.
   - Open MSSQL Server and run the `SchemaPawRescue.sql` file provided in the `BuildDB` folder.
   - Alternatively, you can use the `DummyPawRescue.sql` file to populate the tables with sample data. (database should be named accordingly)
   - If MSSQL Server is not installed, download and install it from [here](https://www.microsoft.com/en-us/sql-server/sql-server-downloads).

4. **Change the server name**:
   - Update the server name in all Python files in the `Code` and `pages` folder to match your server name.

5. **Run the application**:
   - Navigate to the `Code` folder containing the Python files.
   - Run the following command to start the application:
     ```bash
     python -m streamlit run LoginScreen.py
     ```

6. **Login to the application**:
   - Use the following dummy credentials to log in (only on `DummyPawRescue.sql` database):
     - **Username**: Ahmed Bilal
     - **Password**: bilal

---

### Installation for Linux

1. **Clone the repository**:
   ```bash
   git clone https://github.com/EmanFatimaa/Khidmat.git
   ```

2. **Install Python and libraries**:
   - Install Python and pip if not already installed.
   - Navigate to the `Khidmat` folder and install the required libraries:
     ```bash
     pip3 install -r requirements.txt
     ```

3. **Install MSSQL Server**:
   - Run the following commands to install MSSQL Server:
      ```bash
      sudo apt-get install curl
      curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | sudo gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg
      sudo cp /usr/share/keyrings/microsoft-prod.gpg /etc/apt/trusted.gpg.d/

      curl -fsSL https://packages.microsoft.com/config/ubuntu/22.04/mssql-server-2022.list | sudo tee /etc/apt/sources.list.d/mssql-server-2022.list

      sudo apt-get update
      sudo apt-get install -y mssql-server

      sudo ACCEPT_EULA='Y' MSSQL_PID='Developer' MSSQL_SA_PASSWORD='PawRescue!1' MSSQL_TCP_PORT=1433 /opt/mssql/bin/mssql-conf setup

      systemctl status mssql-server --no-pager

      curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | sudo tee /etc/apt/sources.list.d/ms-prod.list

      sudo apt-get install -y mssql-tools18 unixodbc-dev

      sudo /opt/mssql/bin/mssql-conf set sqlagent.enabled true
      sudo systemctl restart mssql-server
      ```

4. **Install ODBC Drivers**:
   - Run the following commands
      ```bash
      curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc

      curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

      sudo apt-get update
      sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18

      sudo ACCEPT_EULA=Y apt-get install -y mssql-tools18
      echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
      source ~/.bashrc

      sudo apt-get install -y unixodbc-dev
      ```

5. **Install Azure Data Studio (optional)**:
   - For a GUI interface, download and install Azure Data Studio:
      - download the `.deb` file from [here](https://learn.microsoft.com/en-us/azure-data-studio/download-azure-data-studio?tabs=linux-install%2Cwin-user-install%2Cubuntu-install%2Cwindows-uninstall%2Credhat-uninstall).
   - Run the following command
     ```bash
     sudo dpkg -i azuredatastudio-linux-1.50.0.deb
     ```

6. **Import the Database**:
   - Create a new database named `SchemaPawRescue`.
   - Run the `SchemaPawRescue.sql` file provided in the `BuildDB` folder to create the database schema.
   - Alternatively, use the `DummyPawRescue.sql` file for sample data. (database should be named accordingly)
   - Update the server name in all Python files in the `Code` and `pages` folder to `localhost (127.0.0.1)`.

7. **Run the application**:
   - Navigate to the `Code` folder containing the Python files.
   - Start the application:
     ```bash
     python3 -m streamlit run LoginScreen.py
     ```

8. **Login to the application**:
   - Use the following dummy credentials to log in (only on `DummyPawRescue.sql` database):
     - **Username**: Ahmed Bilal
      - **Password**: bilal

## Features

- **Rescue Operations Management**: Track and update details of rescued animals, including species, medical condition, and assigned caretaker.

- **Interactive Dashboard**: Visualize key metrics such as number of rescues, adoptions, and donations.

- **User Roles**: Secure login for admins, doctors, and nurses with role-based access control.

- **Adoption Records**: Manage adoption requests, approvals, and post-adoption follow-ups.

- **Donor Contributions**: Track donations with details about donors and contribution amounts.