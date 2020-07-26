from webpython import app
from flask import render_template


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/admin')
def admin():
    return render_template("admin/base.html")


if __name__ == '__main__':
    app.run()
