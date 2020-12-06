from __init__ import admin, db
from models import BookCategory, Book, Voucher, User, UserType, Cart, CartItem, Bill, BillDetail
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user
from flask import redirect


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(ModelView(BookCategory, db.session))
admin.add_view(ModelView(Book, db.session))
admin.add_view(ModelView(Voucher, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(UserType, db.session))
admin.add_view(ModelView(Cart, db.session))
admin.add_view(ModelView(CartItem, db.session))
admin.add_view(ModelView(Bill, db.session))
admin.add_view(ModelView(BillDetail, db.session))
admin.add_view(LogoutView(name="Logout"))
