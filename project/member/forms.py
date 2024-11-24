from project import db 
from flask_wtf import FlaskForm
from project.models import Profil_tps
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField, HiddenField,DecimalField, IntegerField

class LoginMem(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    login = SubmitField('Login')

class edit_anggota(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    konf_pass = PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Edit')
  

class profilTPS(FlaskForm):
    nama_tps = StringField('Nama TPS', validators=[DataRequired(), Length(min=3, max=20)])
    lokasi_lat = DecimalField('Lat', validators=[DataRequired()])
    lokasi_lon = DecimalField('Lon', validators=[DataRequired()])
    kecamatan = SelectField('Kecamatan', validators=[DataRequired()])
    kelurahanId = SelectField('Kelurahan', validators=[DataRequired()],  choices=[])
    user_id  = HiddenField(' user_id ')
    emailName  = HiddenField(' email ')
    prflT = SubmitField('Isi Profil')
   
    def validate_userid(self, userid):
      cekuser = Profil_tps.query.filter_by(membert_id=userid.data).first()
      if cekuser:
        raise ValidationError('tps sudah terdaftar')
        
    def validate_email(self, emailName):
      cektpsemail = Profil_tps.query.filter_by(emailName=emailName.data).first()
      if cektpsemail:
        raise ValidationError('Akun email Dari tps sudah terdaftar')

class editProfilTPS(FlaskForm):
    ed_nama_tps = StringField('Nama TPS', validators=[DataRequired(), Length(min=3, max=20)])
    ed_lokasi_lat = DecimalField('Lat', validators=[DataRequired()])
    ed_lokasi_lon = DecimalField('Lon', validators=[DataRequired()])
    ed_kecamatan = SelectField('Kecamatan', validators=[DataRequired()])
    ed_kelurahan = SelectField('Kelurahan', validators=[DataRequired()], choices=[])
    ed_user_id  = HiddenField(' user_id ')
    ed_emailName  = HiddenField(' email ')
    ed_prflT = SubmitField('Edit') 

class submitCaleg(FlaskForm):
    nm_calon = SelectField('Nama Calon', validators=[DataRequired()], choices=[('', "pilih caleg")])

    partaiId = SelectField('Partai', validators=[DataRequired()], choices=[])
    drdpil = SelectField('Dapil', validators=[DataRequired()], choices=[])
    kecamatanId = SelectField('Kecamatan', validators=[DataRequired()], choices=[])
    kelurahanId = SelectField('Kelurahan', validators=[DataRequired()], choices=[('', "pilih kelurahan")])
    no_tpsid = SelectField('Nama Tps', choices=[], validators=[DataRequired()])
    total = IntegerField('perolehan', validators=[DataRequired()])
    emailName  = HiddenField(' ')
    submit = SubmitField("Submit")

class editCaleg(FlaskForm):
    ed_nm_calon = SelectField('Nama Calon', validators=[DataRequired()], choices=[])
    ed_drdpil = SelectField('Dapil', validators=[DataRequired()], choices=[])
    ed_partaiId = SelectField('Partai', validators=[DataRequired()], choices=[])
    ed_kecamatanId = SelectField('Kecamatan', validators=[DataRequired()], choices=[])
    ed_kelurahanId = SelectField('Kelurahan', validators=[DataRequired()], choices=[])
    ed_no_tpsid = SelectField('Nama Tps', choices=[], validators=[DataRequired()])
    ed_total = IntegerField('perolehan', validators=[DataRequired()])
    ed_submit = SubmitField("Submit")
    