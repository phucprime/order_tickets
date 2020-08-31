from webpython.models import *


def read_flights(airfield=None, airfield_land_off=None, keyword=None):
    flights = Flight.query

    if airfield and airfield_land_off:
        flights = flights.filter(Flight.airfield.contains(airfield),
                                 Flight.airfield_land_off.contains(airfield_land_off))

    if keyword:
        flights = flights.filter(Flight.airfield.contains(keyword) |
                                 Flight.airfield_land_off.contains(keyword))

    return flights.all()


def flight_details(flight_id):
    details = FlightSchedule.query
    if flight_id:
        details = details.filter(FlightSchedule.flight_id.like(flight_id))
    return details.all()


def cancel(bill):
    Order.query.filter(Order.bill == bill).delete()
    return db.session.commit()


def option_flights():
    option = Flight.query
    return option.all()


if __name__ == "__main__":
    print(read_flights())
