from __init__ import app
from flask import Flask, render_template, request, redirect
from admin_models import *
from __init__ import login
from models import User
from flask_login import login_user

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
        password = request.form.get("password")
        user = User.query.filter(username == username, password=password).first()

        if user:
            login_user(user=user)
        else:
            err_msg = "Login failed !"

    return redirect('/admin')
'''hihi thay doi ne'''
if __name__ == "__main__":
    app.run(port=8999, debug=True) 