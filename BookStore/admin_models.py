from __init__ import admin, db
from models import Book, BookCategory, User, UserType, Cart, CartItem, Bill, BillDetail,Supplier,ImportBook
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect





class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id_UserType == 1

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/')

    def is_accessible(self):
        return current_user.is_authenticated

class GoToHome(BaseView):
    @expose('/')
    def index(self):
        return redirect('/')

admin.add_view(AuthenticatedView(BookCategory, db.session, category="Book"))
admin.add_view(AuthenticatedView(Book, db.session, category="Book"))
admin.add_view(AuthenticatedView(User, db.session, category="User"))
admin.add_view(AuthenticatedView(UserType, db.session, category="User"))
admin.add_view(AuthenticatedView(Cart, db.session))
admin.add_view(AuthenticatedView(CartItem, db.session))
admin.add_view(AuthenticatedView(Bill, db.session))
admin.add_view(AuthenticatedView(BillDetail, db.session))
admin.add_view(AuthenticatedView(Supplier, db.session))
admin.add_view(AuthenticatedView(ImportBook, db.session))


admin.add_view(LogoutView(name="Logout"))
admin.add_view((GoToHome(name="Go To Home ")))
#
