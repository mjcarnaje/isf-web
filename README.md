# Iligan Stray Feeders (ISF) Web Application

**Iligan Stray Feeders (ISF)** is a web application designed to connect stray animals in Iligan City with potential adopters and donors while also providing valuable resources for lost and found pets. This project also serves as a platform for volunteers who want to contribute to the cause of Iligan Stray Feeders.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Pet Listings**: Easily browse through profiles of stray animals in need of adoption.
- **Lost and Found**: Find resources and tools for reporting lost or found pets and reuniting them with their owners.
- **Donations**: Support the cause by making monetary or in-kind donations to help feed and care for stray animals.
- **Volunteer Opportunities**: Sign up as a volunteer and contribute your time and skills to the Iligan Stray Feeders organization.
- **User Profiles**: Create and manage user profiles to track your activity and contributions.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python (version 3.x)
- Flask (a Python web framework)
- MySQL (for the database)
- Tailwind CSS (for styling)

## Getting Started

1. **Clone the Repository:**

   ```bash
   git clone https://mjcarnaje@bitbucket.org/isf-team/isf-web.git
   ```

2. **Install Pipenv (if not yet installed):**

   ```bash
   pip install --user pipenv
   ```

3. **Install Dependencies:**

   ```bash
   pipenv install
   ```

4. **Set Up the Database:**

   - Create a MySQL database for the project and update the database connection configuration in your Flask app.

5. **Setup the Environment:**

   - Create a `.env` file in the root directory of the project and add the following environment variables:

     ```bash
        PIPENV_VENV_IN_PROJECT=1
        SECRET_KEY=<your_secret_key>
        MYSQL_HOST=<your_mysql_host>
        MYSQL_USER=<your_mysql_user>
        MYSQL_PASSWORD=<your_mysql_password>
        MYSQL_DATABASE=<your_mysql_database>
     ```

     **Note:** The `SECRET_KEY` is used by Flask to encrypt session cookies. You can generate a secret key using the following Python code:

     ```python
     python -c 'import secrets; print(secrets.token_hex())'
     ```

6. **Run the Application (Development):**

   To run the application, you can use the following commands:

   - To run compile the Tailwind CSS stylesheets:

     ```bash
     ./tailwindcss -i web/static/css/tailwind.css -o web/static/css/styles.css --watch
     ```

   - To run the Flask app:

     ```bash
     python app.py
     ```

7. Access the web app in your browser at `http://localhost:5000`.
