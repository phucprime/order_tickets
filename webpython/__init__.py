from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = "7p\x1d\xf6\xb4\xcb\xde\xd2\x92\x0en\x9b\x8b\xdf\xfe\xbc"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Arkadas0p@localhost/data1?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_DEBUG"] = True
app.config["MAIL_USERNAME"] = 'servertestmvc@gmail.com'
app.config["MAIL_PASSWORD"] = 'd11m03y99'
app.config["MAIL_DEFAULT_SENDER"] = 'servertestmvc@gmail.com'
app.config["MAIL_MAX_EMAILS"] = None
app.config["MAIL_SUPPRESS_SEND"] = False
app.config["MAIL_ASCII_ATTACHMENTS"] = False

mail = Mail(app)

db = SQLAlchemy(app)

admin = Admin(app=app, name="Trang quản lý", template_mode="bootstrap3")

login = LoginManager(app=app)

Session = sessionmaker(bind=db.engine, autocommit=False, autoflush=False)
session = Session()
