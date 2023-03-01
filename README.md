# Engine OCR KTP Muslimat NU

# Introduction

This is a simple engine to extract data from KTP Muslimat NU. This engine is based on Google Cloud Vision API. This engine is running in Flask Framework and dockerized. The engine doesn't have a view there is only have a REST API, So the engine just only background machine learning. For storage this engine using AWS S3. And the database using PostgreSQL.

# Installation
- Clone this repository
- Install docker and docker-compose and install portainer for monitoring docker container 
- Run docker-compose up -d --build

# Requirements
For requirements you can see in requirements.txt

# How to use
- You can use postman to test the API
- You can use curl to test the API
- You can use python requests to test the API

# Configuration
You have to create configuration file first. You can create the file outisdse the file ktp_ocr_crop. The file name is config.py. The configuration file is like this:

```python

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'super secret key'
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{USER_DATABASE}:{PASSWORD_USER}@{IP DATABASE {PORT}/{NAMA DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    S3_BUCKET = '{NAMA BUCKET}'
    S3_KEY = '{S3 KEY}'
    S3_SECRET = '{SECRET PASSWORD}'
    S3_LOCATION = '{LOCATION S3}'
    S3_DIR = '{DIRECTORY S3}'

```

# Certificate
To running this repository you have to create a certificate. And for access the API you have to use https.







