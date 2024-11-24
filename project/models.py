from project import db, loginmanager
from flask_login import login_user, LoginManager, logout_user, current_user, UserMixin
from datetime import datetime

@loginmanager.user_loader
def get_user(ident):
  return Member_tps.query.get(int(ident))

class Member_tps(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), nullable=False)
    profil = db.Column(db.String(30), unique=False, nullable=False, default='profil.jpg')
    profil = db.relationship('Profil_tps',cascade='all, delete', backref='profil')

    def __repr__(self):
        return f"Member_tps('{self.username}', '{self.email}', {self.password}, '{self.profil}')"
 
class Profil_tps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_tps = db.Column(db.String(25))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    emailName = db.Column(db.String(100), nullable=True, unique=True)
    kelurahan = db.Column(db.Integer, db.ForeignKey('kelurahan.id'))
    membert_id = db.Column(db.Integer, db.ForeignKey('member_tps.id'))
    aprove = db.Column(db.Boolean, default=False, nullable=False)
    posted_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    srguber = db.relationship('suara_guber', cascade='all, delete' ,backref='srguber')

    def __repr__(self):
        return f"Profil_tps('{self.nama_tps}','{self.lat}','{self.lon}','{self.emailName}','{self.kelurahan}','{self.membert_id}', {self.posted_on})"
        
class Kabupaten(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_kabupaten = db.Column(db.String(150), nullable=True, unique=True)
    profiltps = db.relationship('Kecamatan', backref='kec')

    def __repr__(self):
        return f"({self.nama_kabupaten})"

class Kecamatan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_kec = db.Column(db.String(150), nullable=True, unique=True)
    kabnid = db.Column(db.Integer, db.ForeignKey('kabupaten.id'))
    kelurahan = db.relationship('Kelurahan',cascade='all, delete', backref='kel')
    
    def __repr__(self):
        return f"({self.nama_kec})"


class Kelurahan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(150), nullable=True, unique=True)
    kecnid = db.Column(db.Integer, db.ForeignKey('kecamatan.id'))
    profiltps = db.relationship('Profil_tps', cascade='all, delete',  backref='profiltps')
    
    def __repr__(self):
        return f"({self.nama})"
        
  
class guber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(150), nullable=True, unique=True)
    suara = db.relationship('suara_guber', cascade='all, delete', backref='suara_guberT')
     

    def __repr__(self):
        return f"({self.nama})"
      
class suara_guber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calgid = db.Column(db.Integer, db.ForeignKey('guber.id'))
    kel_id = db.Column(db.Integer, db.ForeignKey('kelurahan.id'))
    tpsid = db.Column(db.Integer, db.ForeignKey('profil_tps.id'))
    tps_email = db.Column(db.String(100))
    total_s = db.Column(db.Integer)
    tgl_posting = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"({self.calgid}, {self.tpsid}, {self.tps_email}, {self.total_s}, {self.tgl_posting})"
     