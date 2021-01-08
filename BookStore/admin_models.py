from __init__ import admin, db
from models import Book, BookCategory, User, UserType, Cart, CartItem, Bill, BillDetail,Supplier,ImportBook
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect
from sqlalchemy.sql import func
import datetime




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

def myFunc(e):
  return e[0]

class AnalyticsView(BaseView):
    @expose('/')
    def index(self):
        lst = []
        SumDoanhSoTheoNgay = db.session.query(func.sum(Bill.total_price).label('sum'), Bill.order_time).filter(func.month(Bill.order_time) == datetime.datetime.today().month).group_by(
            func.date(Bill.order_time)).all()

        # #co check status
        # SumDoanhSoTheoNgay = db.session.query(func.sum(Bill.total_price).label('sum'), Bill.order_time).filter(
        #     Bill.status == 4).filter(func.month(Bill.order_time) == datetime.datetime.today().month).group_by(
        #     func.date(Bill.order_time)).all()

        for i in SumDoanhSoTheoNgay:
            lst.append([i[1].day, int(i[0])])
        lst.sort(key=myFunc)
        return self.render('admin/analytics.html', lst = lst)

class ExportFile(BaseView):
    @expose('/')
    def index(self):
        pass



admin.add_view(AuthenticatedView(BookCategory, db.session, category="Book"))
admin.add_view(AuthenticatedView(Book, db.session, category="Book"))
admin.add_view(AuthenticatedView(User, db.session, category="User"))
admin.add_view(AuthenticatedView(UserType, db.session, category="User"))
# admin.add_view(AuthenticatedView(Cart, db.session))
# admin.add_view(AuthenticatedView(CartItem, db.session))
admin.add_view(AuthenticatedView(Bill, db.session))
admin.add_view(AuthenticatedView(BillDetail, db.session))
admin.add_view(AuthenticatedView(Supplier, db.session))
admin.add_view(AuthenticatedView(ImportBook, db.session))

admin.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))

admin.add_view(LogoutView(name="Logout"))
admin.add_view((GoToHome(name="Go To Home ")))
#
