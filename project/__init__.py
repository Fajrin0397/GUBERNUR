from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
from flask_socketio import SocketIO
import pymysql 
from datetime import timedelta

dbuser = 'root'
dbpass ='dh1yaL_D' 
dbhost = 'localhost'
dbname = 'ttotalcount'
conn = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(dbuser, dbpass, dbhost, dbname)

app = Flask('__name__', template_folder='project/templates', static_folder='project/static')
app.config['SECRET_KEY'] = "dh1yaldinxx4"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///totalcount.db'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=240)

db = SQLAlchemy(app)
socketio = SocketIO(app)
loginmanager = LoginManager(app)
loginmanager.login_view = "member.login_adm"

bcrypt = Bcrypt(app)

from project.admin.routes import admin
from project.client.routes import client
from project.member.routes import member

app.register_blueprint(member)
app.register_blueprint(admin)
app.register_blueprint(client)