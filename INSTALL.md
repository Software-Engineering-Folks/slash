
# Installation Guide for Slash [Maybe add how to make MongoDB cluster info and how to get credentials for Google OAuth]

Welcome to the installation guide for **Slash**. Follow these steps to set up the environment and run the application.

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

### macOS/Linux
```bash
python -m venv venv
source venv/bin/activate
```

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

## Step 3: Install Dependencies

Install all required dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Step 4: Google OAuth Setup

1. **Obtain Google OAuth Credentials**: 
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or use an existing one.
   - Navigate to **APIs & Services** > **Credentials** and click **Create Credentials** > **OAuth 2.0 Client IDs**.
   - Set the application type to **Web application**.
   - Specify `http://127.0.0.1:5000/login` as the redirect URI.
   - Download the JSON file containing the client secrets.

2. **Client Secrets File**: Place the downloaded JSON file in ```src``` directory.

## Step 5: Configure Environment Variables

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

## Step 6: Initialize Database

Run the `init_db.py` script to set up the database schema and initial data:

```bash
python init_db.py
```
Ensure that your database configuration is correctly set up in your environment variables before running this script.

## Step 7: Run the Application

After setting up the environment and dependencies, start the Flask application:

```bash
flask run
```
Add ```--debug``` to run in debug mode.

By default, the app will run at `http://127.0.0.1:5000/`. Ensure Flask picks up the `.env` file configuration. If you encounter CORS issues, configure Flask to allow cross-origin requests in development mode.


## Troubleshooting

- **Database Issues**: Run `http://127.0.0.1:5000/test` to test database connection.
- **OAuth Errors**: Check that your OAuth credentials are valid and stored at the specified location.
- **Environment Variable [Mac Users only]**: Run ```source .env``` after updated .env file.

---

This guide should help you set up the development environment from the main branch. For any further assistance, please consult the project documentation or reach out to the development team.
