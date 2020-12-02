from __init__ import app
from flask import Flask, render_template
from admin_models import *
from __init__ import login
from models import User

@app.route("/")
def index():
    return render_template('base/base.html')

@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)

'''hihi thay doi ne'''
if __name__ == "__main__":
    app.run(port=8999, debug=True) 