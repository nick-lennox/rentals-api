# rentals-api

## Overview

This Django project encompasses a simple API for managing vacation home rentals, focusing on the functional requirements of the assignment while maintaining extensibiltiy and scalability. There is a provided [design document](DESIGN.md) which provides specification for the API.

## Requirements

- Python 3.12
- Pipenv (or another dependency manager)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/nick-lennox/rentals-api.git
   cd rentals-api
   ```

2. **Install dependencies:**
These instructions are tailored for usage with [Pipenv](https://pipenv.pypa.io/en/latest/). If you prefer a different dependency manager, a `requirements.txt` file is also provided.
    ```bash
    pipenv install
    ```

    2a. **Optional:** Set up environment
    For the sake of keeping the project simple there are no secrets to configure, though it does support a `.env` file should you want to build on top of the existing codebase. 
    </br>

3. **Apply Migrations:**
    This project uses a SQLite DB, therefore some migrations must first be applied to propogate [model](https://docs.djangoproject.com/en/5.0/topics/db/models/) data to the database.
    ```bash
    cd src/
    python manage.py migrate
    ```
    3a. **Optional:** Load fake data
    There is a starter [fixture](https://docs.djangoproject.com/en/5.0/topics/db/fixtures/) to load some initial fake data into the database. If you'd like to start with this data, you can load it into your database from the `starter.json` file:
    ```bash
    django-admin loaddata fixtures/starter.json
    ```

## Running the Server

To start the API locally, run:
```bash
python manage.py runserver
```

The server will start at `http://localhost:8000/` by default.

## Running Tests

To start the API locally, run:
```bash
python manage.py test
```

## Accessing the Admin Portal
The Django Admin site provides CRUD operations per model with a convenient UI. To access it, you must first create a superuser user.

```bash
python manage.py createsuperuser
```

Follow the prompts to create the user record. Once created, go to `http://localhost:8000/admin` and sign in using the credentials you used to create the superuser.

