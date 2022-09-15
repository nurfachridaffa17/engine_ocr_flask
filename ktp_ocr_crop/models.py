from . import db

class M_Member(db.Model):
    __tablename__ = 'm_member'
    id = db.Column(db.Integer, primary_key = True)
    id_user = db.Column(db.Integer)
    id_jenis_kelamin = db.Column(db.Integer)
    id_kawin = db.Column(db.Integer)
    id_status = db.Column(db.Integer)
    id_pekerjaan = db.Column(db.Integer)
    id_struktur = db.Column(db.Integer)
    id_agama = db.Column(db.Integer)
    kode_member = db. Column(db.String, nullable = False)
    nik = db.Column(db.String, nullable = False)
    nama = db.Column(db.String)
    desc = db.Column(db.String)
    tempat_lahir = db.Column(db.String, nullable = False)
    tanggal_lahir = db.Column(db.Date, nullable = False)
    jabatan = db.Column(db.String, nullable = False)
    no_hp = db.Column(db.String, nullable = False)
    alamat_ktp = db.Column(db.String, nullable = False)

class t_attachment(db.Model):
    __tablename__ = 't_attachment'
    id = db.Column(db.Integer, primary_key = True)
    id_ref = db.Column(db.Integer)
    type = db.Column(db.String, nullable = False)
    nama_file = db.Column(db.String, nullable = False)
    hash_file = db.Column(db.String, nullable = False)
    path = db.Column(db.String, nullable = False)
    is_cropped = db.Column(db.Integer)
    desc = db.Column(db.String, nullable = False)
    createdby = db.Column(db.Integer)
    updatedby = db.Column(db.Integer)

class t_log_attachment(db.Model):
    __tablename__ = 't_log_attachment'
    id = db.Column(db.Integer, primary_key = True)
    id_status = db.Column(db.Integer)
    id_attachment = db.Column(db.Integer)
    desc = db.Column(db.String, nullable = False)

class m_status(db.Model):
    __tablename__ = 'm_status'
    id = db.Column(db.Integer, primary_key = True)
    kode = db.Column(db.String)
    nama = db.Column(db.String, nullable = False)
    desc = db.Column(db.String, nullable = False)