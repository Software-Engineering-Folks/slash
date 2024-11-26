
# Installation Guide for Slash

Welcome to the installation guide for **Slash**. Follow these steps to set up the environment and run the application.

## Table of Contents
- [Installation Guide for Slash](#installation-guide-for-slash)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Set Up a Virtual Environment (Optional)](#step-2-set-up-a-virtual-environment-optional)
  - [Step 3: Install Dependencies](#step-3-install-dependencies)
  - [Step 4: MongoDB Setup](#step-4-mongodb-setup)
  - [Step 5: Google OAuth Setup](#step-5-google-oauth-setup)
  - [Step 6: Configure Environment Variables](#step-6-configure-environment-variables)
  - [Step 7: Initialize Database](#step-7-initialize-database)
  - [Step 8: Run the Application](#step-8-run-the-application)
  - [Troubleshooting](#troubleshooting)

---

## Prerequisites

Ensure you have the following installed:

1. **Python 3.8+**
2. **Git**
3. **MongoDB Compass** (Optional)

## Step 1: Clone the Repository

Clone the repository from GitHub. Open a terminal and run:

```bash
git clone https://github.com/Software-Engineering-Folks/slash.git
cd slash
git checkout main
```

## Step 2: Set Up a Virtual Environment (Optional)

Creating a virtual environment is **recommended** to manage dependencies. Run the following:

**macOS/Linux**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

## Step 3: Install Dependencies

Install all required dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Step 4: MongoDB Setup
If you're using MongoDB Atlas, follow these steps to set up your cluster:

1. Log in to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Create a free cluster and choose your cloud provider and region.
3. Set up a username and password for your database.
4. Check for IP Address in Access List and **Whitelist** your IP address:
   - Navigate to **Network Access** in the Security section and add your IP.
5. Obtain the MongoDB connection string:
   - Go to **Clusters > Connect > Connect Your Application**.
   - Copy the connection string and replace `<password>` with your database password.

## Step 5: Google OAuth Setup

1. **Log in to Google Cloud Console:**
   - Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. **Create or Select a Project:**
   - Create a new project or choose an existing one.
3. **Enable OAuth Credentials:**
   - Navigate to **APIs & Services > Credentials**.
   - Click **Create Credentials > OAuth 2.0 Client IDs**.
   - Configure the consent screen and set the application type to **Web Application**.
4. **Add Redirect URIs:**
   - Add `http://127.0.0.1:5000/login` under redirect URIs.
5. **Download Credentials:**
   - Save the generated JSON file and place it in the `src` directory.


## Step 6: Configure Environment Variables

In the project root directory, create a `.env` file for environment-specific variables.

`.env` file contents:

```plaintext
FLASK_APP=.\src\modules\app 
FLASK_ENV=development
SECRET_KEY=SECRET_KEY
GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET=GOOGLE_CLIENT_SECRET
GOOGLE_DISCOVERY_URL=https://accounts.google.com/.well-known/openid-configuration
GOOGLE_REDIRECT_URI=http://127.0.0.1:5000/login
MONGO_URI=MONGO_CLUSTER_URI
DB_NAME=slashdb
```

## Step 7: Initialize Database

Run the `init_db.py` script to set up the database schema and initial data:

```bash
python init_db.py
```
Ensure that your database configuration is correctly set up in your environment variables before running this script.

## Step 8: Run the Application

After setting up the environment and dependencies, start the Flask application:

```bash
flask run
```
Add ```--debug``` to run in debug mode.

By default, the app will run at `http://127.0.0.1:5000/`. Ensure Flask picks up the `.env` file configuration. If you encounter CORS issues, configure Flask to allow cross-origin requests in development mode.


## Troubleshooting

- **Database Connection Issues:** 
  - Ensure the `MONGO_URI` in `.env` is correct.
  - Check that your MongoDB cluster allows connections from your IP address.

- **OAuth Errors:** 
  - Verify that the Google OAuth credentials are in the correct location (`src` directory).
  - Check that the redirect URI matches `http://127.0.0.1:5000/login`.

- **Environment Variables Not Loading:** 
  - On macOS/Linux, run `source .env` to load variables.

---

This guide should help you set up the development environment from the main branch. For any further assistance, please consult the project documentation or reach out to the development team.
