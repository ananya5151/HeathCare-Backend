# Healthcare Backend API

This is a robust backend system for a healthcare application built with Django and Django REST Framework. It provides a secure, token-based authentication system and a comprehensive RESTful API for managing patient and doctor records securely in a PostgreSQL database.

## Features

-   **Secure User Authentication**: Complete user registration and login system using JSON Web Tokens (JWT) for stateless, secure authentication.
-   **Doctor Management**: Full CRUD (Create, Read, Update, Delete) functionality for doctor records.
-   **Patient Management**: Full CRUD functionality for patient records, where each patient is securely associated with the authenticated user who created them. A user can only view and manage their own patient records.
-   **Patient-Doctor Mapping**: Endpoints to assign doctors to patients and manage these relationships.
-   **Custom API Actions**: Includes custom endpoints for advanced queries, such as retrieving all doctors assigned to a specific patient.
-   **Secure & Scalable**: All data-related endpoints are protected, requiring a valid JWT for access. The system uses a powerful and scalable PostgreSQL database.
-   **Environment-Based Configuration**: All sensitive data (like database credentials) is managed securely via environment variables.

## Tech Stack

-   **Backend**: Django, Django REST Framework
-   **Database**: PostgreSQL
-   **Authentication**: djangorestframework-simplejwt
-   **Environment Variables**: python-dotenv

## Local Setup and Installation

Follow these steps to get the project running on your local machine.

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/ananya5151/HeathCare-Backend.git](https://github.com/ananya5151/HeathCare-Backend.git)
    cd HeathCare-Backend
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    *(Note: You will need to generate the `requirements.txt` file first using `pip freeze > requirements.txt`)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up PostgreSQL Database:**
    -   Ensure PostgreSQL is installed and running.
    -   Create a new database and a new user.
    -   Grant the user all privileges on the new database.

5.  **Configure Environment Variables:**
    -   In the project root, create a file named `.env`.
    -   Copy the contents of `.env.example` into it and fill in your actual database credentials.
    ```env
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=localhost
    DB_PORT=5432
    ```

6.  **Run Database Migrations:**
    This command will create all the necessary tables in your database.
    ```bash
    python manage.py migrate
    ```

7.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```
    The API will now be available at `http://127.0.0.1:8000/`.

## API Endpoint Documentation

**Base URL**: `http://127.0.0.1:8000/api/`

### Authentication

| Method | Endpoint             | Auth Required | Description                                       |
| :----- | :------------------- | :------------ | :------------------------------------------------ |
| `POST` | `/auth/register/`    | No            | Register a new user (`username`, `email`, `password`, `password2`). |
| `POST` | `/auth/login/`       | No            | Log in (`username`, `password`) to get JWT tokens.  |
| `POST` | `/auth/login/refresh/` | No            | Use a `refresh` token to get a new `access` token.  |

### Doctors

| Method   | Endpoint        | Auth Required | Description                  |
| :------- | :-------------- | :------------ | :--------------------------- |
| `GET`    | `/doctors/`     | Yes (JWT)     | Get a list of all doctors.   |
| `POST`   | `/doctors/`     | Yes (JWT)     | Create a new doctor.         |
| `GET`    | `/doctors/<id>/`| Yes (JWT)     | Get details of a single doctor. |
| `PUT`    | `/doctors/<id>/`| Yes (JWT)     | Update a doctor's record.    |
| `DELETE` | `/doctors/<id>/`| Yes (JWT)     | Delete a doctor.             |

### Patients

| Method   | Endpoint         | Auth Required | Description                                         |
| :------- | :--------------- | :------------ | :-------------------------------------------------- |
| `GET`    | `/patients/`     | Yes (JWT)     | Get a list of patients created **by the current user**. |
| `POST`   | `/patients/`     | Yes (JWT)     | Create a new patient (auto-assigned to current user). |
| `GET`    | `/patients/<id>/`| Yes (JWT)     | Get details of one of your patients.                |
| `PUT`    | `/patients/<id>/`| Yes (JWT)     | Update one of your patient's records.               |
| `DELETE` | `/patients/<id>/`| Yes (JWT)     | Delete one of your patients.                        |
| `GET`    | `/patients/<id>/doctors/` | Yes (JWT) | **(Custom)** Get all doctors assigned to this patient. |

### Patient-Doctor Mappings

| Method   | Endpoint         | Auth Required | Description                              |
| :------- | :--------------- | :------------ | :--------------------------------------- |
| `GET`    | `/mappings/`     | Yes (JWT)     | Get a list of all patient-doctor maps.   |
| `POST`   | `/mappings/`     | Yes (JWT)     | Assign a doctor to a patient (`doctor` ID, `patient` ID). |
| `GET`    | `/mappings/<id>/`| Yes (JWT)     | Get details of a specific mapping.       |
| `DELETE` | `/mappings/<id>/`| Yes (JWT)     | Remove a patient-doctor assignment.      |