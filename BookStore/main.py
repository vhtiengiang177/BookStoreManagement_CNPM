from __init__ import app
from flask import Flask, render_template, request, redirect
from admin_models import *
from __init__ import login, db
from models import User
from sqlalchemy.sql import func
from flask_login import login_user

@app.route("/")
def index():
    return render_template('base/base.html')

@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=['get', 'post'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('tentao')
        password = request.form.get('password')
        print(username, password)

        user = User.query.filter(User.username == username,
                                 User.password == password).first()

        if user:
            login_user(user=user)
    return redirect('/admin')
'''hihi thay doi ne'''
if __name__ == "__main__":
    app.run(port=8999, debug=True) 