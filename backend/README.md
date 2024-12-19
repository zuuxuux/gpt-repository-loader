# Noovox App Backend

## **Project Overview**

This is the **backend** code for the Noovox App. The backend uses:

- **MySQL** as the database
- **Flask** for API development
- **Swagger** for API documentation

Follow the steps below to install, set up, and run the project seamlessly on your local environment.

---

## **1. Install Python 3.13**

Before proceeding, ensure you have Python 3.13 installed on your system.

### **Linux/macOS**

1. Check if Python is installed:
   ```bash
   python3 --version
   ```
2. If not installed, download and install Python 3.13 from the [official Python website](https://www.python.org/downloads/).
3. Alternatively, use your package manager:
   ```bash
   sudo apt update && sudo apt install python3.13
   ```

### **Windows**

1. Download the Python 3.13 installer from the [official Python website](https://www.python.org/downloads/).
2. Run the installer and ensure the following options are checked:
   - "Add Python to PATH"
   - "Install for all users"
3. Verify installation:
   ```cmd
   python --version
   ```

---

## **2. Clone the Repository**

1. Open your terminal and clone the repository:
   ```bash
   git clone https://github.com/NoovoxOrg/noovox-app.git
   ```
2. Change to the **backend** directory:
   ```bash
   cd noovox-app/backend
   ```

---

## **3. Set Up a Python Virtual Environment**

Create a Python virtual environment in the **backend** directory.

### **Linux/macOS**

```bash
python3 -m venv env
source env/bin/activate
```

### **Windows (Command Prompt)**

```cmd
python -m venv env
env\Scripts\activate
```

### **Windows (PowerShell)**

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

---

## **4. Install Project Dependencies**

While the virtual environment is active, install the required Python dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

---

## **5. Setting Up the Local MySQL Database**

### **A. Install MySQL Server**

#### **Manual Setup for All Operating Systems**
1. Download the MySQL installer from the [official MySQL website](https://dev.mysql.com/downloads/mysql/).
2. Follow the setup wizard to install MySQL Server.
3. During the installation, select the **Developer Default** setup type.
4. Configure MySQL with a root password and note it down.
5. Start the MySQL service using the MySQL Workbench or Command Line Client.

#### **macOS Using Homebrew**

```bash
brew update
brew install mysql
```

#### **Ubuntu/Linux**

```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl enable mysql
```

---

### **B. Start MySQL Service**

#### **Manual Steps (All Operating Systems)**

1. Open the **MySQL Workbench** or **Command Line Client**.
2. Ensure the MySQL server is running.

#### **macOS Using Homebrew**

```bash
brew services start mysql
```

#### **Ubuntu/Linux**

```bash
sudo systemctl start mysql
```

---

### **C. Create the Database Schema**

1. Run the SQL script located at `noovox/db_schema.sql` to set up the database schema. Use the following command:

#### **Manual Steps (All Operating Systems)**

1. Open the MySQL Command Line Client or Workbench.
2. Execute the following command manually:
   ```sql
   SOURCE noovox/db_schema.sql;
   ```

#### **Linux/macOS Command Line**

   ```bash
   mysql -u root -p < noovox/db_schema.sql
   ```

3. Verify the database and tables:

   ```bash
   mysql -u root -p -e "SHOW DATABASES; USE noovox; SHOW TABLES;"
   ```

---

## **6. Configure Database Credentials**

To set up the required database credentials and API keys, run the following interactive Python command:

### **Linux/macOS/Windows**

```bash
python -c "
import os;
print('Setting up credentials...');
credentials = {
    'MYSQL_HOST': input('Enter MySQL Host (default: localhost): ') or 'localhost',
    'MYSQL_USER': input('Enter MySQL User (default: root): ') or 'root',
    'MYSQL_PASSWORD': input('Enter MySQL Password: '),
    'MYSQL_DATABASE': input('Enter MySQL Database Name (default: noovox): ') or 'noovox',
    'OPEN_AI_KEY': input('Enter OpenAI API Key: ')
};
env_file_path = os.path.join(os.getcwd(), '.env');
with open(env_file_path, 'w') as env_file:
    for key, value in credentials.items():
        env_file.write(f'{key}={value}\\n');
print(f'.env file created at {env_file_path}');
"
```

### **Interactive Steps**
When you run the above command, you will be prompted to enter the following information:

1. **MySQL Host**: Defaults to `localhost` if no input is provided.
2. **MySQL User**: Defaults to `root` if no input is provided.
3. **MySQL Password**: Must be provided to connect to the database.
4. **MySQL Database Name**: Defaults to `noovox` if no input is provided.
5. **OpenAI API Key**: Must be provided for OpenAI services.

Ensure you provide accurate values for the password and API key to avoid connection issues.

The `.env` file will be generated automatically in the current directory.

### **Note**
- Include the `.env` file in your `.gitignore` to avoid committing sensitive credentials to version control.

---

## **7. Running the Backend**

You can run the backend server either through **PyCharm** or directly via the **terminal**.

### **A. Run the Server via Terminal**

1. **Ensure the Virtual Environment is Active**

   ```bash
   source env/bin/activate  # For Linux/macOS
   env\Scripts\activate    # For Windows
   ```

2. **Run the Backend Server**

   ```bash
   python noovox/server.py
   ```

3. **Access the API**
   Once the server is running, access the API at:

    - Base URL: `http://localhost:5000`
    - Swagger Documentation: `http://localhost:5000/swagger`

---

## **8. Final Steps**

After completing all the above steps, the backend should run seamlessly in your local environment. You can:

- Test the APIs using tools like **Postman** or directly through Swagger UI.
- Customize database credentials by modifying the `.env` file.

---
