from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from webpython import admin, db, session
from flask import redirect
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user, logout_user
from flask_admin import BaseView, expose
from datetime import datetime
from sqlalchemy.sql import func


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class Rules(db.Model):
    __tablename__ = "rules"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    max_airfield = Column(Integer, default=10)
    min_time_duration = Column(Integer, default=30)


class Flight(db.Model):
    __tablename__ = "flight"
    id = Column(Integer, primary_key=True, autoincrement=True)
    airfield = Column(String(30), nullable=False)
    airfield_land_off = Column(String(30), nullable=False)
    datetime = Column(DateTime, default=datetime.now().date())
    time_duration = Column(Integer, nullable=False)
    available_chair = Column(Integer, default=0)
    unavailable_chair = Column(Integer, default=0)
    price = Column(Float, default=0)
    flight_schedule = relationship('FlightSchedule', backref='flight', lazy=True)

    def __str__(self):
        return "Chuyến bay số " + str(self.id) + " : " + self.airfield \
               + " - " + self.airfield_land_off \
               + " - Khởi hành: " + str(self.datetime.date()) \
               + " - Thời gian: " + str(self.time_duration) + " phút " \
               + " - Ghế trống: " + str(self.available_chair) \
               + " - Ghế đã đặt: " + str(self.unavailable_chair)


class FlightSchedule(db.Model):
    __tablename__ = "flightschedule"
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False, primary_key=True)
    chair_type_1 = Column(Integer, default=0, nullable=False)
    chair_type_2 = Column(Integer, default=0, nullable=False)
    mid_airfield = Column(String(30))
    mid_airfield_time = Column(Integer)
    mid_airfield_note = Column(String(50))
    mid_airfield_2 = Column(String(30))
    mid_airfield_time_2 = Column(Integer)
    mid_airfield_note_2 = Column(String(50))
    orders = relationship('Order', backref='flightschedule', lazy=True)

    def __str__(self):
        return 'Mã chuyến bay: ' + str(self.flight_id)


class Order(db.Model):
    __tablename__ = "order"
    flight_id = Column(Integer, ForeignKey(FlightSchedule.flight_id), nullable=False)
    bill = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    identity_number = Column(String(20), nullable=False)
    ticket_type = Column(Integer, default=1, nullable=False)
    passengers = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(30), nullable=False)
    price = Column(Float, default=0)

    def __str__(self):
        return "Mã hoá đơn: " + str(self.bill) \
               + " - CMND: " + self.identity_number \
               + " - Loại vé: " + str(self.ticket_type) \
               + " - Hành khách: " + str(self.passengers) \
               + " - SĐT: " + self.phone \
               + " - Giá: " + str(self.price) + " VNĐ"


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    count_flight = session.query(Flight.id).count()
    count_order = session.query(Order.bill).count()
    count_ticket = session.query(Order.bill).count()
    flight_table = session.query(Flight)
    order_table = session.query(Order)
    revenue = session.query(func.sum(Order.price).label("revenue")).group_by(Order.price).all()
    ticket_1 = session.query(Order.ticket_type).filter(Order.ticket_type.like(1)).count()
    ticket_2 = session.query(Order.ticket_type).filter(Order.ticket_type.like(2)).count()

    def __str__(self):
        return self.name


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class FlightModelView(AuthenticatedView):
    column_labels = dict(airfield='Sân bay đi', airfield_land_off='Sân bay đến', datetime='Khởi hành',
                         time_duration='Thời gian (phút)', available_chair='Ghế trống', unavailable_chair='Ghế đã đặt',
                         flight_schedule='Lịch chuyến bay', price='Giá tiền')


class FlightScheduleModelView(AuthenticatedView):
    column_labels = dict(flight='Thông tin chuyến bay', chair_type_1='Ghế loại 1', chair_type_2='Ghế loại 2',
                         mid_airfield='Sân trung gian 1', mid_airfield_time='Thời gian dừng 1 (phút)',
                         mid_airfield_note='Ghi chú 1',
                         mid_airfield_2='Sân trung gian 2', mid_airfield_time_2='Thời gian dừng 2 (phút)',
                         mid_airfield_note_2='Ghi chú 2', orders='Phiếu đặt chỗ')


class OrderModelView(AuthenticatedView):
    column_labels = dict(bill='Hoá đơn', identity_number='CMND', ticket_type='Loại vé',
                         passengers='Hành khách', phone='SĐT', email='Email', price='Giá',
                         flightschedule='Chuyến bay', tickets='Vé')


class RulesModelView(AuthenticatedView):
    column_labels = dict(max_airfield='Chuyến bay tối đa', min_time_duration='Thời gian bay tối thiểu')
    can_create = False
    can_delete = False


class UserModelView(AuthenticatedView):
    column_labels = dict(name='Họ và tên', username='Tên người dùng', password='Mật khẩu', active='Trạng thái')


admin.add_view(FlightModelView(Flight, db.session, name="Chuyến bay"))
admin.add_view(FlightScheduleModelView(FlightSchedule, db.session, name='Lịch bay'))
admin.add_view(OrderModelView(Order, db.session, name='Đơn đặt hàng'))
admin.add_view(RulesModelView(Rules, db.session, name='Quy định'))
admin.add_view(UserModelView(User, db.session, name='Tài khoản'))
admin.add_view(LogoutView(name="Đăng xuất"))

if __name__ == "__main__":
    db.create_all()
