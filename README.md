SCAN KTP OCR WITH FLASK AND GOOGLE CLOUD VISION

- Buat Folder data_ktp_muslimat_nu
- buat folder resource
- Buat folder OCR_texts and Output_data
- Buat file config.py di luar file ktp_ocr_crop
- Build docker compose "docker-compose build -t"
- Next compose "docker-compose up -d"

CERTIFICATE 
- FILE CERTIFICATE DITARO DILUAR SEPERTI FILE RUN.PY

PYTHON
- BUAT FILE CONFIG.PY
ISINYA:

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'super secret key'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{USER_DATABASE}:{PASSWORD_USER}@{IP DATABASE}:{PORT}/{NAMA DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    S3_BUCKET = 'nekosa-muslimat'
    S3_KEY = '{S3 KEY}'
    S3_SECRET = '{SECRET PASSWORD}'
    S3_LOCATION = '{LOCATION S3}'
    S3_DIR = '{DIRECTORY S3}'