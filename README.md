# Iligan Stray Feeders (ISF) Web Application

**Iligan Stray Feeders (ISF)** is a web application designed to connect stray animals in Iligan City with potential adopters and donors, while also providing valuable resources for lost and found pets. This project serves as a platform for volunteers who want to contribute to the cause of Iligan Stray Feeders.

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

Before you begin, make sure you meet the following requirements:

- Python (version 3.x)
- Flask (for the web app)
- MySQL (for the database)
- Tailwind CSS (for styling)

## Getting Started

1. **Clone the Repository:**

   - Clone this repository to your local machine using the following command:

     ```shell
     git clone https://mjcarnaje@bitbucket.org/isf-team/isf-web.git
     ```

2. **Install Dependencies:**

   - You need to have [pipenv](https://pipenv.pypa.io/en/latest/) installed on your system to install the project's dependencies. You can install pipenv using the following command:

     ```shell
     pip install --user pipenv
     ```

   - Once pipenv is installed, you can install the dependencies for this project using the following command:

     ```shell
     pipenv install
     ```

3. **Set Up the Database:**

   - Create a MySQL database for the project and update the database connection configuration in your Flask app.

4. **Set Up the Environment:**

   - Create a `.env` file in the root directory of the project and add the following environment variables, or copy the `.env.sample` file and update the values:

     ```
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

5. **Run the Application (Development):**

   - To run the application, you can use the following commands:

     - To compile the Tailwind CSS stylesheets:

     ```shell
     ./tailwindcss -i web/static/css/tailwind.css -o web/static/css/styles.css --watch
     ```

     - To run the Flask app:

     ```shell
     python app.py
     ```

6. Access the web app in your browser at `http://localhost:5000`.
