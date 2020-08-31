from flask_mail import Message
from webpython import app, login, dao, mail
from flask import render_template, request
from flask_login import login_user
from webpython.models import *
import hashlib
from twilio.rest import Client

account_sid = "ACd5107eb430c675476c846de4b5c102d2"
auth_token = "3a25e1a430fabde4c97b274efe24b535"
client = Client(account_sid, auth_token)


@app.route("/mail-sender", methods=["get", "post"])
def mail_sender():
    email = request.form['email']
    flight = request.form['flight']
    identity_number = request.form['identity_number']
    ticket_type = request.form['ticket_type']
    passengers = request.form['passengers']
    phone = request.form['phone']
    price = request.form['price']

    msg = Message("VE MAY BAY TRUC TUYEN", recipients=[email])

    msg.body = '\nKHACH HANG: ' + passengers + \
               '\nCHUYEN BAY: ' + flight + \
               '\nHANG VE: ' + ticket_type + \
               '\nGIA VE: ' + price + ' VND' + \
               '\nSDT: ' + phone + \
               '\nEMAIL: ' + email + \
               '\nCMND: ' + identity_number + \
               '\nCAM ON BAN DA SU DUNG DICH VU CUA CHUNG TOI!\n'

    mail.send(msg)

    client.messages.create(
        from_='+14158734759',

        body='\n\nVE MAY BAY TRUC TUYEN\n' +
             '\nKHACH HANG: ' + passengers +
             '\nCHUYEN BAY: ' + flight +
             '\nHANG VE: ' + ticket_type +
             '\nGIA VE: ' + price + ' VND' +
             '\nSDT: ' + phone +
             '\nEMAIL: ' + email +
             '\nCMND: ' + identity_number +
             '\n\nCAM ON BAN DA SU DUNG DICH VU CUA CHUNG TOI!\n',

        to='+84' + phone,
    )

    return render_template("home/done-success.html")


@app.route("/")
def home_index():
    airfield = request.args["airfield"] if request.args.get("airfield") else None
    airfield_land_off = request.args["airfield_land_off"] if request.args.get("airfield_land_off") else None
    keyword = request.args["keyword"] if request.args.get("keyword") else None
    return render_template("home/index.html",
                           option=dao.option_flights(),
                           flights=dao.read_flights(airfield=airfield,
                                                    airfield_land_off=airfield_land_off,
                                                    keyword=keyword))


@app.route("/schedule/<int:flight_id>")
def details_flight(flight_id):
    return render_template("home/flight_schedule.html",
                           schedule=dao.flight_details(flight_id))


@app.route("/done-cancel/<string:passengers>")
def done_cancel(passengers):
    return render_template("home/done-delete.html", passengers=dao.cancel(passengers))


@app.route("/about")
def about():
    return render_template("home/about.html")


@app.route("/schedule/order/<int:schedule_id>")
def order_form(schedule_id):
    return render_template("home/order.html",
                           schedule=dao.flight_details(schedule_id))


@app.route("/order-flight", methods=["get", "post"])
def order_flight():
    if request.method.lower() == "post":
        phone = request.form['phone']
        if len(phone) < 10:
            return render_template("home/confirm.html")
        else:
            bill = Order(flight_id=request.form['flight_id'],
                         identity_number=request.form['identity_number'],
                         ticket_type=request.form['ticket_type'],
                         passengers=request.form['passengers'],
                         phone=phone,
                         email=request.form['email'],
                         price=request.form['price'])
            db.session.add(bill)
            flight = request.form['flight']
        db.session.commit()
    return render_template("home/confirm.html", bill=bill, flight=flight)


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
    db.create_all()
    app.run()
