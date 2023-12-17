# Iligan Stray Feeders (ISF) Web Application

Welcome to the **Iligan Stray Feeders (ISF)** web application! Our platform is dedicated to connecting stray animals in Iligan City with potential adopters and donors. Additionally, we provide valuable resources for lost and found pets. ISF is a project that aims to unite volunteers and individuals who want to make a difference in the lives of stray animals.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

ISF offers a range of features to support our mission:

- **Pet Listings**: Browse profiles of stray animals in need of loving homes.
- **Lost and Found**: Access resources and tools for reporting lost or found pets and facilitating reunions.
- **Donations**: Contribute to our cause through monetary or in-kind donations, helping us feed and care for stray animals.
- **Volunteer Opportunities**: Sign up as a volunteer and use your time and skills to make a positive impact within the Iligan Stray Feeders organization.
- **User Profiles**: Create and manage your user profile to monitor your activity and contributions.

## Prerequisites

Before you get started with ISF, ensure that you meet the following requirements:

- Node.js (version 16.x)
- Python (version 3.x)
- Flask (for the web app)
- MySQL (for the database)
- Tailwind CSS (for styling)

## Getting Started

To begin your journey with ISF, follow these steps:

1.  **Clone the Repository:**

    Clone this repository to your local machine using the following command:

    ```shell
    git clone https://mjcarnaje@bitbucket.org/isf-team/isf-web.git
    ```

2.  **Install Dependencies:**

    Install [pipenv](https://pipenv.pypa.io/en/latest/) on your system to manage project dependencies. You can install pipenv with this command:

        ```shell
        pip install --user pipenv
        ```

    Once pipenv is installed, use the following command to install project dependencies:

        ```shell
        pipenv install
        ```

3.  **Set Up the Database:**

    Create a MySQL database for the project and update the database connection configuration within your Flask app.

4.  **Set Up the Environment:**

    Create a `.env` file in the project's root directory. Add the following environment variables or copy them from the `.env.sample` file and update their values:

        ```
        SECRET_KEY=
        MYSQL_HOST=<your_mysql_host>
        MYSQL_USER=<your_mysql_user>
        MYSQL_PASSWORD=<your_mysql_password>
        MYSQL_DATABASE=<your_mysql_database>
        #cloudinary config
        CLOUDINARY_CLOUD_NAME=
        CLOUDINARY_API_KEY=
        CLOUDINARY_API_SECRET=
        CLOUDINARY_FOLDER=
        # google auth
        GOOGLE_CLIENT_ID=
        GOOGLE_CLIENT_SECRET=
        GOOGLE_DISCOVERY_URL=
        # flask config
        PIPENV_VENV_IN_PROJECT=1
        FLASK_DEBUG=1
        ```

    The `SECRET_KEY` is used by Flask to encrypt session cookies. You can generate a secret key using the following Python code:

        ```python
        python -c 'import secrets; print(secrets.token_hex())'
        ```

5.  **Run the Application (Development):**

    To run the application, follow these steps:

    - Compile the Tailwind CSS stylesheets:

      ```shell
      npm run compile:css
      ```

    - Run the Flask app:

      ```shell
      flask run
      ```

    - Run the Celery:
      ```
            celery -A app.celery_app worker --loglevel INFO
      ```

6.  Access the web app in your browser at `http://localhost:5000`.

Thank you for joining us in our mission to make a difference in the lives of stray animals in Iligan City! We appreciate your support and involvement in the Iligan Stray Feeders (ISF) community.
