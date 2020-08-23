from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, sessionmaker, session
from webpython import admin, db
from flask import redirect
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user, logout_user
from flask_admin import BaseView, expose


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class Flight(db.Model):
    __tablename__ = "flight"
    id = Column(Integer, primary_key=True, autoincrement=True)
    airfield = Column(String(30), nullable=False)
    airfield_land_off = Column(String(30), nullable=False)
    datetime = Column(String(20), nullable=False)
    time_duration = Column(String(20), nullable=False)
    available_chair = Column(Integer, default=0)
    unavailable_chair = Column(Integer, default=0)
    flight_schedule = relationship('FlightSchedule', backref='flight', lazy=True)

    def __str__(self):
        return "Chuyến bay số " + str(self.id) \
               + ": " + self.airfield \
               + " - " + self.airfield_land_off \
               + " - Khởi hành: " + self.datetime \
               + " - Thời gian: " + self.time_duration \
               + " - Ghế trống: " + str(self.available_chair) \
               + " - Ghế đã đặt: " + str(self.unavailable_chair)


class FlightSchedule(db.Model):
    __tablename__ = "flightschedule"
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False, primary_key=True)
    chair_type_1 = Column(Integer, default=0, nullable=False)
    chair_type_2 = Column(Integer, default=0, nullable=False)
    mid_airfield = Column(String(30))
    mid_airfield_time = Column(String(20))
    mid_airfield_note = Column(String(50))
    mid_airfield_2 = Column(String(30))
    mid_airfield_time_2 = Column(String(20))
    mid_airfield_note_2 = Column(String(50))
    orders = relationship('Order', backref='flightschedule', lazy=True)

    def __str__(self):
        return 'Mã chuyến bay: ' + str(self.flight_id)


class Order(db.Model):
    __tablename__ = "order"
    flight_id = Column(Integer, ForeignKey(FlightSchedule.flight_id), nullable=False, primary_key=True)
    bill = Column(String(10), nullable=False)
    identity_number = Column(String(20), nullable=False)
    ticket_type = Column(Integer, default=1, nullable=False)
    passengers = Column(Integer, nullable=False)
    phone = Column(String(20), nullable=False)
    price = Column(Float(20), default=0)
    tickets = relationship('Ticket', backref='order', lazy=True)

    def __str__(self):
        return "Mã hoá đơn: " + self.bill \
                    + " - CMND: " + self.identity_number \
                    + " - Loại vé: " + str(self.ticket_type) \
                    + " - Hành khách: " + str(self.passengers) \
                    + " - SĐT: " + self.phone \
                    + " - Giá: " + str(self.price) + " VNĐ"


class Ticket(db.Model):
    __tablename__ = "ticket"
    flight_id = Column(Integer, ForeignKey(Order.flight_id), primary_key=True)


class MonthReport(db.Model):
    __tablename__ = 'monthreport'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    flight = Column(String(10), nullable=False)
    ticket_count = Column(Integer, default=0)
    ratio = Column(Float, default=0)
    revenue = Column(Float, default=0)


class YearReport(db.Model):
    __tablename__ = 'yearreport'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    month = Column(Integer, default=1)
    flight_count = Column(Integer, default=0)
    revenue = Column(Float, default=0)
    ratio = Column(Float, default=0)


Session = sessionmaker(bind=db.engine)
session = Session()


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    count_flight = session.query(Flight.id).count()
    count_order = session.query(Order.bill).count()
    count_ticket = session.query(Ticket.flight_id).count()
    flight_table = session.query(Flight)
    order_table = session.query(Order)

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
                         time_duration='Thời gian', available_chair='Ghế trống', unavailable_chair='Ghế đã đặt',
                         flight_schedule='Lịch chuyến bay')


class FlightScheduleModelView(AuthenticatedView):
    column_labels = dict(flight='Thông tin chuyến bay', chair_type_1='Ghế loại 1', chair_type_2='Ghế loại 2',
                         mid_airfield='Sân trung gian 1', mid_airfield_time='Thời gian dừng 1',
                         mid_airfield_note='Ghi chú 1',
                         mid_airfield_2='Sân trung gian 2', mid_airfield_time_2='Thời gian dừng 2',
                         mid_airfield_note_2='Ghi chú 2', orders='Phiếu đặt chỗ')


class OrderModelView(AuthenticatedView):
    column_labels = dict(bill='Hoá đơn', identity_number='CMND', ticket_type='Loại vé',
                         passengers='Hành khách', phone='SĐT', price='Giá', flightschedule='Chuyến bay',
                         tickets='Vé')


class TicketModelView(AuthenticatedView):
    column_labels = dict(order='Thông tin vé đã được đặt')


class YearReportModelView(AuthenticatedView):
    pass


class MonthReportModelView(AuthenticatedView):
    pass


class UserModelView(AuthenticatedView):
    column_labels = dict(name='Họ và tên', username='Tên người dùng', password='Mật khẩu', active='Trạng thái')


admin.add_view(FlightModelView(Flight, db.session, name="Chuyến bay"))
admin.add_view(FlightScheduleModelView(FlightSchedule, db.session, name='Lịch bay'))
admin.add_view(OrderModelView(Order, db.session, name='Đơn đặt hàng'))
admin.add_view(TicketModelView(Ticket, db.session, name='Vé'))
admin.add_view(MonthReportModelView(MonthReport, db.session, name='Báo cáo tháng'))
admin.add_view(YearReportModelView(YearReport, db.session, name='Báo cáo năm'))
admin.add_view(UserModelView(User, db.session, name='Tài khoản'))
admin.add_view(LogoutView(name="Đăng xuất"))

if __name__ == "__main__":
    db.create_all()
