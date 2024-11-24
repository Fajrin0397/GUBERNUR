from project import socketio, db
from project.models import suara_caleg, Profil_tps, Caleg, Dapil
from flask import render_template, Blueprint, redirect, url_for, jsonify
from flask_login import current_user
from flask_socketio import emit, send, join_room, leave_room
client = Blueprint('client',__name__)

@client.route('/')
def index():
    dapil = Dapil.query.all()
    if current_user.is_authenticated:
        daftar = Profil_tps.query.filter_by(emailName=current_user.email).first()
        if daftar:
            return render_template('index.html', title='home')
        else:
           return redirect(url_for('member.profiltps')) 
    else:
        return render_template('index.html', title='DPRD', dapil=dapil)
        
     
@client.route('/DPR-RI/Pusat')
def pusat():
    if current_user.is_authenticated:
        daftar = Profil_tps.query.filter_by(emailName=current_user.email).first()
        if daftar:
            return render_template('index.html', title='home')
        else:
            return redirect(url_for('member.profiltps')) 
    else:
        return render_template('dpr-pusat.html', title='DPR pusat')


@client.route('/Halaman-DPR-Provinsi')
def dprri():
    if current_user.is_authenticated:
        daftar = Profil_tps.query.filter_by(emailName=current_user.email).first()
        if daftar:
            return render_template('index.html', title='home')
        else:
            return redirect(url_for('member.profiltps')) 
    else:    
        return render_template('dprprov.html', title='DPR Povinsi')
 
@client.route('/DPRD/<int:tipe>')
def pilihlegis(tipe):
    legis = db.session.query(suara_caleg.total_s, Caleg.nama ).join(suara_caleg, Caleg.id == suara_caleg.calgid).\
            filter(suara_caleg.tpsid == tipe).filter(Caleg.tipeid == 1).all() #and Caleg.tipeid==3 ).all()
    leg =[{
        'suara': dt[0],
        'nama': dt[1],
    } for dt in legis]
    return jsonify(leg)
    
@client.route('/tojson')
def tojson():
  prfl = Profil_tps.query.all()
  mylist = []
  for pr in prfl:
        kms = {}
        kms['Idtps'] = pr.id
        kms['nama_tps'] = pr.nama_tps
        kms['lat'] = pr.lat
        kms['lon'] = pr.lon
        #kms['per'] = cektps(pr.id)
        mylist.append(kms)
  return jsonify({'users':mylist})

  
@client.route('/cektps/<id>')
def cektps(id):
  hit = suara_caleg.query.filter_by(tpsid=id).all()
  hitArray = []
  for h in hit:
      hitObj = {}
   # if h.no_tps == cekId:
      hitObj['nama'] = h.suara_calegT.nama
      hitObj['suara'] = h.total_s
      hitObj['id_tps'] = h.id
      hitObj['nama_tps'] = h.srcaleg.nama_tps
      hitArray.append(hitObj)
  return jsonify(hitArray)
  
 
@client.route('/pusat/<int:tipe>')
def Ri_pusat(tipe):
    legis_pusat = db.session.query(suara_caleg.total_s, Caleg.nama ).join(suara_caleg, Caleg.id == suara_caleg.calgid).\
            filter(suara_caleg.tpsid == tipe).filter(Caleg.tipeid == 3 ).all()
    leg =[{
        'suara': dt[0],
        'nama': dt[1],
    } for dt in legis_pusat]
    return jsonify(leg)


@client.route('/jsonprov/<int:tipe>')
def jsondprri(tipe):
    legis = db.session.query(suara_caleg.total_s, Caleg.nama ).join(suara_caleg, Caleg.id == suara_caleg.calgid).\
            filter(suara_caleg.tpsid == tipe).filter(Caleg.tipeid == 2 ).all()
    leg =[{
        'suara': dt[0],
        'nama': dt[1],
    } for dt in legis]
    return jsonify(leg)

 
 
 
@socketio.on('kirimdata')
def kirim(data):
    filterDapil = db.session.query(Caleg.nama, db.func.sum(suara_caleg.total_s)).\
        join(Caleg, suara_caleg.calgid == Caleg.id).join(Dapil, suara_caleg.dapilid==Dapil.id)\
        .group_by(Caleg.nama).filter_by(id = data).all()
    #print(dapil)

    fltDpJson = [{'Nama_Caleg': cg[0], 'Total_suara': int(cg[1])} for cg in filterDapil]
    emit('hasJson', fltDpJson)

@socketio.on('datadprprov')
def kirim(data):
    filterDapil = db.session.query(Caleg.nama, db.func.sum(suara_caleg.total_s)).\
        join(Caleg, suara_caleg.calgid == Caleg.id).join(Dapil, suara_caleg.dapilid==Dapil.id)\
        .group_by(Caleg.nama).filter(Dapil.id == data).all()

    fltDpJsonprov = [{'Nama_Caleg': cg[0], 'Total_suara': int(cg[1])} for cg in filterDapil]
    emit('hasJsonprov', fltDpJsonprov)

@socketio.on('datapusat')
def rimpusat(data):
    filterPusat = db.session.query(Caleg.nama, db.func.sum(suara_caleg.total_s)).\
        join(Caleg, suara_caleg.calgid == Caleg.id).join(Dapil, suara_caleg.dapilid==Dapil.id)\
        .group_by(Caleg.nama).filter(Dapil.id == data).all()
    
    fltDpJsonpus = [{'Nama_Caleg': cg_pus[0], 'Total_suara': int(cg_pus[1])} for cg_pus in filterPusat]
    emit('hasJsonpus', fltDpJsonpus)
