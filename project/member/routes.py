from project.models import Profil_tps, suara_caleg, Kelurahan, Kecamatan, Dapil, Member_tps, Caleg, Partai
from .forms import submitCaleg, profilTPS, editProfilTPS, editCaleg, edit_anggota
from project import db, bcrypt
from flask import render_template, Blueprint, redirect,url_for, g, flash, request, abort, jsonify
from functools import wraps
from flask_login import login_user, LoginManager, logout_user, current_user, login_required
from project.member.forms import LoginMem
import sqlalchemy


member = Blueprint('member',__name__)

def isiProfiltps(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        daftar = Profil_tps.query.filter_by(emailName=current_user.email).first()
        if daftar:
             return f(*args, **kwargs)
        else:
            flash('Anda Harus mengisi profil TPS terlebih Daluhu')
            return redirect(url_for('member.profiltps', next=request.url))
    return decorated_function

@member.route('/profil-member')
@login_required
@isiProfiltps
def profil_member():
    prof = Profil_tps.query.filter_by(emailName=current_user.email).first()
    password = Member_tps.query.filter_by(email=current_user.email).first()
    return render_template('member-tps.html', prof=prof, passw=password)
   
  
@member.route('/isi-suara-caleg', methods=['GET','POST'])
@login_required
@isiProfiltps
def isi_suara():
    form=submitCaleg()
    form.kecamatanId.choices = [(str(kecamatan.id),kecamatan.nama_kec) for kecamatan in Kecamatan.query.all()]
    if request.method == "POST":
        hcg = suara_caleg(calgid=form.nm_calon.data, dapilid=form.drdpil.data, partaiId=form.partaiId.data ,kel_id=form.kelurahanId.data, tpsid=form.no_tpsid.data, total_s = form.total.data, tps_email=form.emailName.data)
        db.session.add(hcg)
        db.session.commit()
        return redirect(request.referrer)
    clg = suara_caleg.query.filter_by(tps_email=current_user.email).all()
    return render_template('suara_caleg.html', form=form, title='isi suara caleg', clg=clg)


@member.route('/hapus-suara/<int:id>', methods=['GET','POST'])
@login_required
def hapus_suara(id):
    hps = suara_caleg.query.filter_by(id=id).first()
    if request.method == "POST":
        db.session.delete(hps)
        db.session.commit()
        return redirect(url_for('member.isi_suara'))
        
@member.route('/desa/<int:id>')
def desa(id):
    ds = Kelurahan.query.filter_by(kecnid=id).all()
    dsarray = []
    for d in ds :
        dsobj = {}
        dsobj['id'] = d.id
        dsobj['nama_kelurahan'] = d.nama
        dsarray.append(dsobj)
    return jsonify({'kelurahan': dsarray})   
      
@member.route('/edit-suara-caleg/<int:id>', methods=['GET','POST'])
@login_required
def edit_suara(id):
    form=editCaleg()
    edit_s = suara_caleg.query.filter_by(id=id).first()
    if edit_s.tps_email == current_user.email:
        form.ed_kecamatanId.choices = [(str(kecamatan.id),kecamatan.nama_kec) for kecamatan in Kecamatan.query.all()]
        form.ed_drdpil.choices = [(str(dapil.id), dapil.nama_dapil) for dapil in Dapil.query.all()]
        form.ed_partaiId.choices = [(str(nm_partai.id), nm_partai.partai) for nm_partai in Partai.query.all()]
        if request.method == "GET":
            form.ed_nm_calon.data = edit_s.calgid
            form.ed_drdpil.data = edit_s.dapilid
            form.ed_kelurahanId.data = edit_s.partaiId
            form.ed_kelurahanId.data = edit_s.kel_id
            form.ed_no_tpsid.data = edit_s.tpsid
            form.ed_total.data=edit_s.total_s
        elif request.method == "POST":
            edit_s.calgid = form.ed_nm_calon.data
            edit_s.dapilid = form.ed_drdpil.data
            edit_s.partaiId = form.ed_partaiId.data
            edit_s.kel_id = form.ed_kelurahanId.data
            edit_s.tpsid = form.ed_no_tpsid.data
            edit_s.total_s = form.ed_total.data
            db.session.commit()
            return redirect(url_for('member.isi_suara'))
        return render_template('edit-suara.html', form=form)
    else:
        flash('bukan suara anda')
        return redirect(url_for('client.index'))

@member.route('/profil-tps', methods=['GET','POST'])
@login_required
def profiltps():
    form=profilTPS( )
    flash('anda harus mengisi profil tps terlebih dahulu')
    try:
      form.kecamatan.choices = [(str(kecamatan .id), kecamatan.nama_kec) for kecamatan in Kecamatan.query.all()]
      if request.method == "POST":
          tmbh = Profil_tps(nama_tps=form.nama_tps.data, lat=form.lokasi_lat.data, lon=form.lokasi_lon.data, kelurahan=form.kelurahanId.data,emailName=form.emailName.data, membert_id=form.user_id.data)
          db.session.add(tmbh)
          db.session.commit()
          return redirect(url_for('member.isi_suara'))
    except sqlalchemy.exc.IntegrityError:
      abort(403)
      #flash("anda sudah mendaftar sebelum nya", "danger")  
    return render_template('profil-tps.html', form=form, title='isi profil')
    
  
 
@member.route('/edit-profil-tps/<int:id>', methods=['GET','POST'])
@login_required
def edit_profil_tps(id):
    dt_pfl = Profil_tps.query.filter_by(id=id).first()
    formeditpfl = editProfilTPS()
    formeditpfl.ed_kecamatan.choices = [(str(kecamatan.id), kecamatan.nama_kec) for kecamatan in Kecamatan.query.all()]
    if request.method == "GET":
      formeditpfl.ed_nama_tps.data = dt_pfl.nama_tps
      formeditpfl.ed_lokasi_lat.data = dt_pfl.lat
      formeditpfl.ed_lokasi_lon.data = dt_pfl.lon
      formeditpfl.ed_kelurahan.data = dt_pfl.kelurahan 
    elif request.method == "POST":
      dt_pfl.nama_tps = formeditpfl.ed_nama_tps.data
      dt_pfl.lat = formeditpfl.ed_lokasi_lat.data
      dt_pfl.lon = formeditpfl.ed_lokasi_lon.data
      dt_pfl.kelurahan = formeditpfl.ed_kelurahan.data 
      db.session.commit()
      return redirect(url_for("member.isi_suara"))
    return render_template('edit_profil.html', formeditpfl=formeditpfl)

@member.route('/edit-password/<email>', methods=['GET','POST'])
@login_required
def edit_password(email):
    member = Member_tps.query.filter_by(email=email).first()
    form=edit_anggota()
    if request.method == 'GET':
        form.password.data = member.password
    elif request.method == "POST":
        member.password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        db.session.commit()
        return redirect(url_for('member.profil_member'))
    return render_template('edit-password.html', form=form, title='edit password')

@member.route("/login-member", methods=["GET","POST"])
def login_adm():
    form=LoginMem()
    if form.validate_on_submit():
        cekmail = Member_tps.query.filter_by(email=form.email.data).first()
        if cekmail and bcrypt.check_password_hash(cekmail.password, form.password.data):
            login_user(cekmail)
            # socketio.emit('user_active', 'hai')
            return redirect(url_for("client.index"))
        else:
            flash("login salah harap periksa email dan password")
    return render_template("login.html", form=form, title='Login Page')

@member.route('/nama-caleg/<int:id>')
def nama_caleg(id):
    clg  = Caleg.query.filter_by(dapilid=id).all()
    array = []
    for c in clg:
        caldict = dict()
        caldict['id'] = c.id
        caldict['nama_caleg'] = c.nama
        array.append(caldict)
    return jsonify({'nama': array})

@member.route('/nama-partai/<int:id>/<int:idP>')
def nama_partai(id, idP):
    clg  = Caleg.query.filter_by(partaiId=id).filter_by(dapilid=idP).all()
    array = []
    for c in clg:
        caldict = dict()
        caldict['id'] = c.id
        caldict['nama_caleg'] = c.nama
        array.append(caldict)
    return jsonify({'nama': array})


# @member.route('/pilih-dapkec/<int:id>')
# def kecamatan_pil(id):
    # clg  = Kecamatan.query.filter_by(dapilId=id).all()
    # array = []
   # if id in clg:
    # for c in clg:
    #    if id in c:
        #  caldict = dict()
        #  caldict['id'] = c.id
        #  caldict['nama_kec'] = c.nama_kec
        #  array.append(caldict)
# 
    # else:
        #    print('bukan ararai')
    # return jsonify({'nama': array})
                    

@member.route('/profiljson/<int:id>')
def profiljson(id):
    pfrl = Profil_tps.query.filter_by(kelurahan=id).all()
    prArray = []
    for p in pfrl:
        prObj = {}
        prObj['id'] = p.id
        prObj['nama_kelurahan'] = p.nama_tps
        prArray.append(prObj)
    return jsonify({'TPS':prArray})
    
@member.route('/pilihkel/<int:id>')
def pilihkel(id):
    pfrl = Kelurahan.query.filter_by(kecnid=id).all()
    prArray = []
    for p in pfrl:
        prObj = {}
        prObj['id'] = p.id
        prObj['nama_kecamatan'] = p.nama
        prArray.append(prObj)
    return jsonify({'Kelurahan':prArray})
    
@member.route('/editprofiljson/<int:id>')
def editprofiljson(id):
    pfrl = Profil_tps.query.filter_by(kelurahan=id).all()
    prArray = []
    for p in pfrl:
        prObj = {}
        prObj['id'] = p.id
        prObj['nama_kelurahan'] = p.nama_tps
        prArray.append(prObj)
    return jsonify({'TPS':prArray})   

@member.route('/logout')
def logoutmem():
    logout_user()
    return redirect(url_for('client.index'))