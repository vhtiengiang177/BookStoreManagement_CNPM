from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
app = Flask(__name__)

app.secret_key='ansfhkashfk11111shfnmsagashfska1111'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:18110402@localhost/bookstore?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)
admin = Admin(app=app, name="Book Store",
              template_mode='bootstrap3')

login = LoginManager(app=app)
