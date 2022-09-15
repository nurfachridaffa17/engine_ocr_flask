from flask import request, jsonify
from . import ktp_image as ktpg
from genericpath import exists
from datetime import datetime as dt
from . import app
from .models import db, t_attachment, M_Member
import boto3
from . import entity as extractor
from . import kyc_config as cfg
from . import ocr_gcloud as ocr
import cv2
import os

@app.route('/dowload/ktp', methods=['POST', 'GET'])
def dowload_ktp():
    img_var ='ktp_ocr_crop/data_ktp_muslimat_nu/{}'.format(request.form.get('variabel_image'))
    s3_bucket = app.config['S3_BUCKET']
    s3_dir = app.config['S3_DIR']
    session = boto3.session.Session()
    client = session.client(
        's3',
        aws_access_key_id=app.config['S3_KEY'],
        aws_secret_access_key=app.config['S3_SECRET'],
        region_name='id-jkt01-dos',
        endpoint_url=app.config['S3_LOCATION']
    )
    if img_var is not exists:
        nama_file = request.form.get('variabel_image')
        client.download_file(s3_bucket, 'image/ktp/{}'.format(nama_file), 'ktp_ocr_crop/data_ktp_muslimat_nu/%s'%(nama_file))
        return jsonify(message='Image berhasil dowloads'), 200
    else:
        return jsonify(message='Image sudah ada'), 500


@app.route('/image/profile_picture', methods=['POST', 'GET'])
def image_ktp():
    id_attachment_ref = request.form.get('id_member')
    nama_file = request.form.get('variabel_image')
    img_var ='ktp_ocr_crop/data_ktp_muslimat_nu/{}'.format(nama_file)
    s3_bucket = app.config['S3_BUCKET']
    s3_dir = app.config['S3_DIR']
    session = boto3.session.Session()
    client = session.client(
        's3',
        aws_access_key_id=app.config['S3_KEY'],
        aws_secret_access_key=app.config['S3_SECRET'],
        region_name='id-jkt01-dos',
        endpoint_url=app.config['S3_LOCATION']
    )
    img = cv2.imread(img_var)
    contours = ktpg.get_contours(img)
    pts = ktpg.find_4_coord(contours)
    img_transform = ktpg.transform(img, pts)
    hasil_crop = cv2.imwrite('ktp_ocr_crop/resource/%s'%(nama_file), img_transform)
    if not hasil_crop:
        return jsonify(message='No File Uploaded'), 400
    else:
        with open('ktp_ocr_crop/resource/%s'%(nama_file), 'rb') as src:
            client.put_object(
                ACL='public-read',
                Bucket=s3_bucket,
                Key=f'{s3_dir}/{nama_file}',
                Body=src
            )
        t_attachemnt_member = t_attachment(
            id_ref = id_attachment_ref,
            type = 'm_member',
            nama_file = nama_file,
            path =f'{s3_dir}/{nama_file}' ,
            is_cropped = 1,
            desc = 'image_ktp_crop',
            createdby = 1,
            updatedby = 1
        )
        db.session.add(t_attachemnt_member)
        db.session.commit()
        db.session.close()
        
        return jsonify(message='Success'),200

@app.route('/put/picture_ktp', methods=['POST', 'GET', 'PUT'])
def get_ktp():
    if request.method == 'PUT':
        nama_file = request.form.get('variabel')
        img_path ='ktp_ocr_crop/data_ktp_muslimat_nu/{}'.format(request.form.get('variabel'))
        member_id = request.form.get('id')
        check_member = db.session.query(M_Member).filter_by(id=member_id).first()
        if check_member.nik is None:
            ocr.process_ocr(img_path)
            img_name = img_path.split('/')[-1].split('.')[0]
            ocr_path = cfg.json_loc+'ocr_'+img_name+'.npy'
            data_ktp = extractor.process_extract_entities(ocr_path).to_dict(orient='records')
            id_member = db.session.query(M_Member).get(member_id)
            query_graduates = db.session.query(M_Member).filter_by(nik=data_ktp[0]['identity_number']).first()
            if id_member is None:
                jsonify(message="Tidak Ada Member"), 500
            if query_graduates:
                return jsonify(message="NIK Sudah terdaftar"), 500
            else:
                id_member.nik = data_ktp[0]['identity_number']

                if data_ktp[0]['gender'] == 'Male':
                    id_member.id_jenis_kelamin = 1
                else:
                    id_member.id_jenis_kelamin = 2

                if data_ktp[0]['occupation'] == 'Mengurus Rumah Tangga':
                    id_member.id_pekerjaan = 1
                elif data_ktp[0]['occupation'] == 'Buruh Harian Lepas':
                    id_member.id_pekerjaan = 2
                elif data_ktp[0]['occupation'] == 'Pegawai Negeri Sipil':
                    id_member.id_pekerjaan = 3
                elif data_ktp[0]['occupation'] == 'Pelajar/Mahasiswa':
                    id_member.id_pekerjaan = 4
                elif data_ktp[0]['occupation'] == 'Karyawan Swasta':
                    id_member.id_pekerjaan = 5
                elif data_ktp[0]['occupation'] == 'Pegawai Negeri':
                    id_member.id_pekerjaan = 6
                elif data_ktp[0]['occupation'] == 'Wiraswasta':
                    id_member.id_pekerjaan = 7
                else :
                    id_member.id_pekerjaan = 8

                if data_ktp[0]['marital_status'] == 'Single':
                    id_member.id_kawin = 1
                elif data_ktp[0]['marital_status'] == 'Married':
                    id_member.id_kawin = 2
                elif data_ktp[0]['marital_status'] == 'Cerai Hidup':
                    id_member.id_kawin = 3
                else:
                    id_member.id_kawin = 4

                id_member.nama = data_ktp[0]['fullname']

                id_member.tempat_lahir = data_ktp[0]['birth_place']

                        # id_member.tanggal_lahir = data_ktp[0]['birth_date']
                if data_ktp[0]['birth_date'] == 'NaN':
                    id_member.tanggal_lahir = dt.today()
                else:
                    id_member.tanggal_lahir = data_ktp[0]['birth_date']

                id_member.alamat_ktp = data_ktp[0]['address']

                if data_ktp[0]['religion'] == 'ISLAM':
                    id_member.id_agama = 1
                else:
                    id_member.id_agama = 1

                db.session.add(id_member)
                db.session.commit()
                db.session.close()

                os.remove('ktp_ocr_crop/data_ktp_muslimat_nu/%s'%(nama_file))
                os.remove('ktp_ocr_crop/resource/%s'%(nama_file))
                
                return jsonify(message='Success OCR'), 200