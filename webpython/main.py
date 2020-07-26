from webpython import app
from flask import render_template


@app.route('/')
def admin():
    return render_template("admin/base.html")


if __name__ == '__main__':
    app.run()
