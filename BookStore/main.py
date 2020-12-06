from __init__ import app
from flask import Flask, render_template, request, redirect, flash
from admin_models import *
from __init__ import login
from models import User
from flask_login import login_user
import hashlib

@app.route("/")
def index():
    return render_template('base/base.html')

@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods = ['get', 'post'])
def login_admin():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = hashlib.md5(password.strip().encode("utf-8")).hexdigest()
        user = User.query.filter(User.username == username.strip(), User.password==password.strip()).first()

        if user:
            flash('Logged in successfully.')
            login_user(user=user)
            # admin.add_view(LogoutView(name="Logout"))
        else:
            flash("Login failed !", category='error')

    return redirect('/admin')


if __name__ == "__main__":
    app.run(port=8999, debug=True)


# dang nhap admin, pass 123
# insert mysql admin, pass 202cb962ac59075b964b07152d234b70