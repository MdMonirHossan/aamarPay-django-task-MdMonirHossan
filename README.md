# Payment Gateway Integration and Files Uploading System
This project is a Django-based application that integrates with **aamarPay** for payments and allows users to upload `.docx` or `.txt` files after successful payment. Uploaded files are processed with Celery to count words, and results are stored in the database.


## Features
- User registration and authentication
- aamarPay sandbox payment gateway integration
- File uploads (`.docx` or `.txt` only)
- Word count processing with Celery
- Admin panel for managing users, payments, and files (With custom Permission)
- REST API endpoints (JWT authentication)
- Docker & docker-compose setup
- Frontend for Dashboard and File upload form

## Setup Instructions
- **Clone the repo.**
```bash
$ git clone git@github.com:MdMonirHossan/aamarPay-django-task-MdMonirHossan.git
    
$ cd aamarPay-django-task-MdMonirHossan
```

## Configure Environment Variables
Create `.env` file in the project
```
SECRET_KEY=your-secret-key
DEBUG=True

# MySQL 
MYSQL_DATABASE=db_name
MYSQL_USER=db_username
MYSQL_PASSWORD=db_password
MYSQL_ROOT_PASSWORD=db_root_pass
DB_HOST=db
DB_PORT=3306

# Redis 
REDIS_URL=redis://redis:6379/0

# Aamarpay sandbox 
PAYMENT_URL=https://sandbox.aamarpay.com/jsonpost.php
STORE_ID=aamarpaytest
SIGNATURE_KEY=dbb74894e82415a2f7ff0ec3a97e4183
SUCCESS_URL=/api/payment/success
CANCEL_URL=/api/payment/cancel
FAIL_URL=/api/payment/failed
```

## Running with Docker (No Configuration)
**Make sure docker is available in your system**
```bash
$ docker-compose up --build
```

## Running with Manual Configuration
#### 1. Create a virtual environment & Activate
```bash 
# virtual environment

$ python -m venv env

# Activate 
$ source env/bin/activate   # Linux/Mac
$ env\Scripts\activate      # Windows
```
#### 2. Install dependencies
```bash
# Project dependencies
$ pip install -r requirements.txt
```

#### 3. Run Migrations and Migrate
```bash
$ python manage.py makemigrations

$ python manage.py migrate
```

#### 4. Create Superuser
```bash
$ python manage.py createsuperuser
```

#### 5. Run Redis Server
**If redis is already installed in your system**
```bash
$ redis-server
```
**Or with Docker**
```bash
$ docker run -d --name redis -p 6379:6379 redis
```

#### 6. Start Celery Worker
```bash
$ celery -A payment_gateway worker -l info
```

#### 7. Start Django Development Server 
```bash
$ python manage.py runserver
```
---
**App will be available at:**
[http://localhost:8000](http://localhost:8000)

**Registration will be available at:**
[http://localhost:8000/signup](http://localhost:8000/signup)

**Login will be available at:**
[http://localhost:8000/login](http://localhost:8000/login)

**Dashboard will be available at:**
[http://localhost:8000/dashboard](http://localhost:8000/dashboard)

**Admin will be available at:**
[http://localhost:8000/admin](http://localhost:8000/admin)

**Swagger Docs**
[http://localhost:8000/api/swagger](http://localhost:8000/api/swagger)

**Redoc Docs**
[http://localhost:8000/api/redoc](http://localhost:8000/api/redoc)


## Notes
- Only `.docx` and `.txt` files are allowed for upload.
- Staff users can view all in the admin but can not add edit or delete.
- Superusers have full permissions.


## Project workflow/planning available at
**=> [Workflow/Planning](https://github.com/MdMonirHossan/aamarPay-django-task-MdMonirHossan/blob/main/Development_Planning.txt)**

## Postman API collection available at
**=> [Postman Collection](https://github.com/MdMonirHossan/aamarPay-django-task-MdMonirHossan/blob/main/Aamarpay.postman_collection.json)**

## Postman Environment Variables available at
**=> [Postman Collection](https://github.com/MdMonirHossan/aamarPay-django-task-MdMonirHossan/blob/main/Aamarpay.postman_environment.json)**


## Testing the API with Postman

This project includes a json files for **Postman collection** and **environment** .

**Import Postman Collection & Environment files and test all API's** 

## Test File Upload from Dashboard

**The file upload form will be available only if the user has a successful payment and then the user can upload `.docx` or `.txt` file**

`There will be an API named 'File Upload' in Postman collection. You can also test upload file functionality in there.`


## Payment Flow 
- Uer initiate a payment to `aamarpay` sandbox.
- User will get a payment url after successful payment initiate.
- User will be able to perform payment by redirecting to payment url.
- After payment success/failed/cancel user will redirect to the appropriate ui (success/failed/cancel page).


## File Upload Flow
- User make payment via `Aamarpay`.
- After payment confirmation, user uploads `.docx` or `.txt` file.
- Celery processes the file and count words.
- Database is updated with word count and status to complete in FileUpload.

## API Endpoints

| Method | Endpoint                                  | Description                   |
| ------ | ----------------------------------------- | ----------------------------- |
|        |                       **Auth**                                            |
| POST   | `/api/user/register`                      | User registration             |
| POST   | `/api/auth/token`                         | Get JWT tokens                |
| POST   | `/api/auth/refresh-token`                 | Get JWT tokens with Refresh   |
|        |                        **Transactions**                                   | 
| POST   | `/api/initiate-payment`                   | Payment Initiate              |
| POST   | `/api/payment/success`                    | Payment Success Callback      |
| POST   | `/api/payment/failed`                     | Payment Failed Callback       |
| GET    | `/api/payment/cancel`                     | Payment Cancel Callback       |
| POST   | `/api/upload`                             | File upload                   |
| GET    | `/api/files`                              | User Uploaded Files           |
| GET    | `/api/transactions`                       | User Transactions             |
|        |                        **Activity Log**                                             |
| GET    | `/api/activity`                           | User Activity                 |
