from project.admin.forms import dft_anggota, calegForm, editCalegForm, dapilForm, editkelurahanForm, editmemberForm
from project.models import Dapil, Member_tps, Kabupaten, Kelurahan, Caleg, Kecamatan,Type, Profil_tps, suara_caleg, Partai
from project import db, socketio, bcrypt
from project.admin.forms import kecamatanForm, kabupatenForm, kelurahanForm, partaiForm
from flask import render_template,redirect, url_for, Blueprint, jsonify, request
from flask_login import current_user, login_required
from flask_socketio import emit, join_room, leave_room

admin = Blueprint('admin',__name__)

@admin.route('/daftar-anggota', methods=['GET','POST'])
@login_required
def daftar_angggota():
    form=dft_anggota()
    if current_user.email == "as-admin@gmail.com":
        if form.validate_on_submit():
            pass_hash = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
            mbr = Member_tps(username=form.username.data, email=form.email.data, password=pass_hash)
            db.session.add(mbr)
            db.session.commit()
            return redirect(request.referrer)
    else:
        return redirect(request.referrer)
    return render_template('daftar-anggota.html', form=form, title='tambah anggota')
    

@admin.route('/member-active')
@login_required
def actMem():
    return render_template('login-noB.html') 

@admin.route('/tambah-caleg', methods=['GET','POST'])
def tambah_caleg():
    halaman = request.args.get('page',1, type=int)
    page = Caleg.query.order_by(Caleg.id.desc()).paginate(page=halaman, per_page=10)
    #caleg = Caleg.query.order_by(Caleg.dapilid.desc())
    form = calegForm()
    form.dapilId.choices = [(str(dapil.id), dapil.nama_dapil) for dapil in Dapil.query.all()]
    form.partaiId.choices = [(str(partai_nama.id), partai_nama.partai) for partai_nama in Partai.query.all()]
    form.tipeid.choices = [(str(tipe.id), tipe.tipe) for tipe in Type.query.all()]
    if request.method == "POST":
        legis = Caleg(nama=form.nama.data, dapilid=form.dapilId.data, partaiId =form.partaiId.data ,tipeid=form.tipeid.data)
        db.session.add(legis)
        db.session.commit()
        return redirect(request.referrer)
    return render_template('tambah_caleg.html', title='tambah-caleg', form=form, page=page)

@admin.route('/edit-caleg/<int:id>',  methods=['GET','POST'])
def edit_caleg(id):
    form = editCalegForm()
    form.ed_dapilId.choices = [(str(dapil.id), dapil.nama_dapil) for dapil in Dapil.query.all()]
    form.ed_tipeid.choices = [(str(tip.id), tip.tipe) for tip in Type.query.all()]
    form.partaiId.choices = [(str(pai.id), pai.partai) for pai in Partai.query.all()]
    edit = Caleg.query.filter_by(id=id).first()
    if request.method == "GET":
        form.ed_nama.data = edit.nama
        form.ed_dapilId.data = edit.dapilid
        form.ed_tipeid.data = edit.tipeid
        form.partaiId.data = edit.partaiId
    if request.method == "POST":
        edit.nama = form.ed_nama.data
        edit.dapilid = form.ed_dapilId.data
        edit.tipeid = form.ed_tipeid.data
        edit.partaiId = form.partaiId.data
        db.session.commit()
        return redirect(url_for('admin.tambah_caleg'))
    return render_template('edit-caleg.html', form=form)
    
 
@admin.route('/tambah-dapil',  methods=['GET','POST'])
def tambah_dapil():
    form=dapilForm()
    if form.validate_on_submit():
        dpl = Dapil(nama_dapil=form.nama.data)
        db.session.add(dpl)
        db.session.commit()
        return redirect(request.referrer)
    return render_template('tambah_dapil.html', form=form)

 
@admin.route('/tambah-partai',  methods=['GET','POST'])
def tambah_partai():
    form=partaiForm()
    if form.validate_on_submit():
        prt = Partai(partai=form.nama.data)
        db.session.add(prt)
        db.session.commit()
        return redirect(request.referrer)
    return render_template('tambah_partai.html', form=form)

@admin.route('/tambah-kelurahan',  methods=["GET","POST"])
def tambah_kelurahan():
    form=kelurahanForm()
    form.kab_asal.choices =  [(str(kecamatan.id), kecamatan.nama_kec) for kecamatan in Kecamatan.query.all()]
    if form.validate_on_submit():
            kel = Kelurahan(nama=form.nama.data, kecnid=form.kab_asal.data)
            db.session.add(kel)
            db.session.commit()
            return redirect(url_for("admin.tabel_kelurahan"))
    return render_template('tambah-kelurahan.html', form=form, title='Tambah Kelurahan')
   

@admin.route('/tambah-kecamatan',  methods=["GET","POST"])
def tambah_kecamatan():
    form=kecamatanForm()
    form.kmtn.choices =  [(str(kabupaten.id), kabupaten.nama_kabupaten) for kabupaten in Kabupaten.query.all()]
    form.dapil.choices =  [(str(dapil.id),dapil.nama_dapil) for dapil in Dapil.query.all()]  
    if form.validate_on_submit():
            kec = Kecamatan(nama_kec=form.nama.data, kabnid=form.kmtn.data, dapilId=form.dapil.data)
            db.session.add(kec)
            db.session.commit()
            return redirect(request.referrer)
    kec = Kecamatan.query.all()
    return render_template('tambah-kecamatan.html', form=form, title='Tambah kecamatan', kec=kec)

@admin.route('/edit-kecamatan/<int:id>')
def edit_kec(id):
    if current_user.email == "as-admin@gmail.com":
        kcmtn = Kecamatan.query.filter_by(id=id).first()
        form = kecamatanForm()
        if request.method == 'GET':
            form.nama.data = kcmtn.nama_kec
            form.kmtn.data = kcmtn.kabnid
        elif form.validate_on_submit():
            kcmtn.nama_kec = form.nama.data
            kcmtn.kabnid = form.kmtn.data
            db.session.commit()
            return redirect(request.referrer)
    else:
        return redirect(request.referrer)
    return render_template('edit-kecamatan.html', form=form)
    
@admin.route('/tabel-kelurahan')
def tabel_kelurahan():
        halaman = request.args.get('page',1, type=int)
        kel = Kelurahan.query.order_by(Kelurahan.id.desc()).paginate(page=halaman, per_page=10)
        return render_template('tabel-kelurahan.html', kel=kel, title='Tabel kelurahan')

@admin.route('/hapus-kelurahan/<int:id>', methods=['GET','POST'])
def hapus_kel(id):
  klrh= Kelurahan.query.filter_by(id=id).first()
  if request.method == "POST":
        db.session.delete(klrh)
        db.session.commit()
        return redirect(request.referrer)

@admin.route('/edit-kelurahan/<int:id>', methods=['GET','POST'])
def edit_kelurahan(id):
    if current_user.email == "as-admin@gmail.com":
        ed_kel = Kelurahan.query.filter_by(id=id).first()
        form = editkelurahanForm()
        if request.method == 'GET':
            form.nama.data = ed_kel.nama
        elif form.validate_on_submit():
            ed_kel.nama = form.nama.data
            db.session.commit()
            return redirect(url_for('admin.tabel_kelurahan'))
    else:
        return "<h3>anda bukan admin tertinggi</h3>"
    return render_template('edit-kelurahan.html', form=form)

@admin.route('/tabel-member')
@login_required
def tabel_member():
    if current_user.email == "as-admin@gmail.com":
        halaman = request.args.get('page',1, type=int)
        mbr = Member_tps.query.order_by(Member_tps.id.desc()).paginate(page=halaman, per_page=10)
        return render_template('tabel-member.html', mbr=mbr, title='table member')
    else:
        return "<h3>Anda bukan superadmin</h3>"
    
@admin.route('/tabel-profil-tps')
@login_required
def tabel_profilTPS():
    halaman = request.args.get('page',1, type=int)
    prfl = Profil_tps.query.order_by(Profil_tps.id.desc()).paginate(page=halaman, per_page=3)
    return render_template('tabel-profil-tps.html', prfl=prfl)

@admin.route('/hapus-profil-tps/<int:id>')
def hapus_tps(id):
    hapus = Profil_tps.query.filter_by(id=id).first()
    if request.method == "POST":
        db.session.delete(hapus)
        db.session.commit()
        return redirect(url_for('admin.tabel_profil'))



@admin.route('/edit-tabel-member/<int:id>', methods=['GET','POST'])
def edit_member(id):
    if current_user.email == "as-admin@gmail.com":
        e_mbr = Member_tps.query.filter_by(id=id).first()
        if request.method == 'GET':
           request.form['username'] =  e_mbr.username 
           request.form['email'] = e_mbr.email
           request.form['password'] = e_mbr.password
        elif request.method == 'POST': 
            pass_hash = bcrypt.generate_password_hash(request.form['password']).decode('UTF-8')
            e_mbr.username = request.form['username']
            e_mbr.email =request.form['email']
            e_mbr.password = pass_hash 
            db.session.commit()
            return redirect(url_for('admin.tabel_member'))
    else:
        return "<h3>Anda bukan superadmin</h3>"   
    
 
@admin.route('/cari-caleg/<string:nama>',  methods=['GET','POST'])
def cari_caleg(nama):
    search = "%{0}%".format(nama)
    name = db.session.query(Caleg.id, Caleg.nama, Profil_tps.nama_tps, Dapil.nama_dapil ,suara_caleg.total_s).join(Caleg, suara_caleg.calgid == Caleg.id)\
    .join(Profil_tps, suara_caleg.tpsid == Profil_tps.id).join(Dapil, suara_caleg.dapilid == Dapil.id).filter(suara_caleg.tps_email == current_user.email).filter(Caleg.nama.like(search)).all()
    parJson= [{
            'ID' : dt[0],
            'Nama': dt[1],
            'TPS': dt[2],
            'Dapil':dt[3],
            'total_suara':dt[4]
                    } for dt in name]
    return jsonify({'nameparjson': parJson})  
  
@admin.route('/hapus-caleg/<int:id>',  methods=['GET','POST'])
@login_required
def hapus_caleg(id):
    hapus_cal = Caleg.query.filter_by(id=id).first()
    if request.method == "POST":
        db.session.delete(hapus_cal)
        db.session.commit()
        return redirect(url_for('tambah_caleg'))

@admin.route('/hasil-pencarian/<string:nama>')
def hasil(nama):
    cari = "%{0}%".format(nama)
    hasilnya = db.session.query(Caleg.id, Caleg.nama, Dapil.nama_dapil, Type.tipe).join(Dapil, Caleg.dapilid == Dapil.id)\
        .join(Type, Caleg.tipeid == Type.id).filter(Caleg.nama.like(cari)).all()
    had_groupby = [{
        'ID' : dt[0],
         'kandidat': dt[1],
         'Dapil': dt[2],
         'Type': dt[3]
     } for dt in hasilnya]
    return jsonify({'hsl':had_groupby})


# userDict={}

# @socketio.on('connect')
# def test_connect(auth):
#     if current_user.is_authenticated:
#         actmember = Profil_tps.query.filter_by(emailName=current_user.email).first()
#         # join_room('active_member')
#         userDict[actmember.id] = {'Nama': actmember.nama_tps, 'lat':actmember.lat, 'lng':actmember.lon}
#         emit('member', userDict, broadcast=True)
#         print(userDict)



# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')   