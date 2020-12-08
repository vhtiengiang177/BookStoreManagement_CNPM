from __init__ import admin, db
from models import BookCategory, Book, Voucher, User, UserType, Cart, CartItem, Bill, BillDetail
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect





class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.idUserType == 1

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.idUserType == 1

# class InfoAccount(AuthenticatedView):
#     can_edit = True
#     can_create = False
#
#     @expose('/')
#     def index(self):
#         self = current_user
#         return


admin.add_view(AuthenticatedView(BookCategory, db.session, category="Book"))
admin.add_view(AuthenticatedView(Book, db.session, category="Book"))
admin.add_view(AuthenticatedView(Voucher, db.session))
admin.add_view(AuthenticatedView(User, db.session, category="User"))
admin.add_view(AuthenticatedView(UserType, db.session, category="User"))
admin.add_view(AuthenticatedView(Cart, db.session))
admin.add_view(AuthenticatedView(CartItem, db.session))
admin.add_view(AuthenticatedView(Bill, db.session))
admin.add_view(AuthenticatedView(BillDetail, db.session))
admin.add_view(LogoutView(name="Logout"))

