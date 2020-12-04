from __init__ import admin, db
from models import Category, Book, Voucher, Customer, Bill, User
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user
from flask import redirect


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Book, db.session))
admin.add_view(ModelView(Voucher, db.session))
admin.add_view(ModelView(Customer, db.session))
admin.add_view(ModelView(Bill, db.session))
# admin.add_view(ModelView(Account, db.session))
admin.add_view(LogoutView(name="Logout"))
