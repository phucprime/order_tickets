from flask_admin import Admin

from webpython import app, login
from flask import render_template, redirect, request, url_for
from flask_login import login_user
from sqlalchemy import func, select
from webpython.models import *
import hashlib


@app.route("/")
def home_index():
    return render_template("home/index.html")


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


@app.route("/login_admin", methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        password = str(hashlib.md5(password.strip().encode('utf8')).hexdigest())

        user = User.query.filter(User.username == username.strip(),
                                 User.password == password.strip()).first()

        if user:
            login_user(user=user)
            
    return redirect("/admin")


if __name__ == '__main__':
    app.run()
