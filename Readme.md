### Step 1: Download and install python version smaller than 3.11.5
Cause: The new version will conflict with the old version libraries
### Step 2: Download the library from the requriments.txt file
I recommend you create a venv to run django on another environment using the command
```
python -m venv venv
```
Then activate the environment with the command:
```
.\venv\Scripts\activate
```
Then load the library in the requirements.txt file:
```
pip install -r requirements.txt
```

### Step 3: Add environment variables in the .env file from the .env.example file
```


SQL_ENGINE=django.db.backends.mysql
SQL_DATABASE=
SQL_USER=
SQL_PASSWORD=
SQL_HOST=
SQL_PORT=3306


PAYOS_CREATE_PAYMENT_LINK_URL=https://api-merchant.payos.vn/v2/payment-requests

PAYOS_CLIENT_ID=
PAYOS_API_KEY=
PAYOS_CHECKSUM_KEY=

```
### Step 4: Run the project using the command
```
python manage.py runserver
```