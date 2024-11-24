from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField, HiddenField,DecimalField, IntegerField
from flask_wtf import FlaskForm

class dft_anggota(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=99)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    konf_pass = PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('tambah')
  
 
class editmemberForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=99)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('edit')
 
class kelurahanForm(FlaskForm):
    nama = StringField('Nama kelurahan', validators=[DataRequired()])
    kab_asal = SelectField('pilih kabupaten/kota', validators=[DataRequired()])
    tambah = SubmitField('Tambah')
    

class editkelurahanForm(FlaskForm):
    nama = StringField('Nama kelurahan', validators=[DataRequired()])

    tambah = SubmitField('Edit')

class dapilForm(FlaskForm):
    nama = StringField('Nama Dapil', validators=[DataRequired()])

    tambah = SubmitField('Tambah')
 
class calegForm(FlaskForm):
    nama = StringField('Nama Caleg', validators=[DataRequired()])
    dapilId = SelectField('Daerah Dapil', validators=[DataRequired()], choices=[])
    partaiId = SelectField('Partai', validators=[DataRequired()], choices=[])
    tipeid = SelectField('Type', validators=[DataRequired()], choices=[])
    tambah = SubmitField('Tambah')

class partaiForm(FlaskForm):
    nama = StringField('Nama Partai', validators=[DataRequired()])
    submit = SubmitField('Tambah')
    
class editCalegForm(FlaskForm):
    ed_dapilId = SelectField('Daerah Dapil', validators=[DataRequired()], choices=[])
    ed_tipeid = SelectField('Type', validators=[DataRequired()], choices=[])
    partaiId = SelectField('Partai', validators=[DataRequired()], choices=[])
    ed_nama = StringField('Nama Caleg', validators=[DataRequired()])
    ed_edit = SubmitField('Edit')

class kecamatanForm(FlaskForm):
    nama = StringField('Nama kecamatan', validators=[DataRequired()])
    kmtn = SelectField('pilih kabupaten/kota', validators=[DataRequired()])
    dapil = SelectField('pilih Dapil', validators=[DataRequired()])
    tambah = SubmitField('Tambah')

class kabupatenForm(FlaskForm):
    nama_kab = SelectField(u'pilih kabupaten/kota')
    dapil = SelectField('pilih Dapil', validators=[DataRequired()])