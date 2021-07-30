# WeConnectDevs Django source templete files

## To get started

Ensure you have python => 3 and postgreSQL installed, clone the repo and run the following command within your development environment:

### `pip install -r requirements.txt`

This will install all required software. (If you installed requirements.txt from mastar branch, consider recreating virtual environment and installing current requirements.txt)

## Setup necessary environment variables with django-environ from the newly installed software. 

For a quick tutorial on how to do so, visit: [How to setup env variables in django](https://alicecampkin.medium.com/how-to-set-up-environment-variables-in-django-f3c4db78c55f).

## Make migrations

### `python manage.py makemigrations`

### `python manage.py migrate`

## Running the server

### `python manage.py runserver`

Open [http://localhost:8000/account/](http://localhost:8000/account/) to view url map endpoint.

## Follow endpoint map to use api.

Urls: account/

Register: account/register/

Email Verification: account/verify-email/

Resend Email Verification: account/resend-verification/

Login: account/login/

Logout: account/logout

User Email List + Add: account/emails/

View, Delete Email: account/emails/<pk>/

Change Password: account/password/change/

Request Password Reset: account/request-password-reset/

Password Rest Confirmation: account/reset-password/

### Tokens recieved via email must be entered in the endpoint manually for now. In future commits we will have working links that autofill the key form.



