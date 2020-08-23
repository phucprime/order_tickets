from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "7p\x1d\xf6\xb4\xcb\xde\xd2\x92\x0en\x9b\x8b\xdf\xfe\xbc"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Arkadas0p@localhost/data1?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

admin = Admin(app=app, name="Trang quản lý", template_mode="bootstrap3")

login = LoginManager(app=app)
