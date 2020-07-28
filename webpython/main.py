from webpython import app
from flask import render_template


@app.route('/admin')
def admin_index():
    return render_template("admin/index.html")


@app.route('/admin/internal-flight')
def flight_index_internal():
    return render_template("admin/flight-internal.html")


@app.route('/admin/external-flight')
def flight_index_external():
    return render_template("admin/flight-external.html")


@app.route("/admin/order")
def order_index():
    return render_template("admin/order.html")


@app.route("/admin/report")
def report_index():
    return render_template("admin/report.html")


if __name__ == '__main__':
    app.run()
