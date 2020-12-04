from __init__ import admin, db
from models import Category, Book, Voucher, Customer, Bill, User
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from sqlalchemy.sql import func
from flask_login import logout_user
from flask import redirect

admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Book, db.session))
admin.add_view(ModelView(Voucher, db.session))
admin.add_view(ModelView(Customer, db.session))
admin.add_view(ModelView(Bill, db.session))
# admin.add_view(ModelView(Account, db.session))

class AnalyticsView(BaseView):
    @expose('/')
    def index(self):
        lst = []
        SumDoanhSoTheoNgay = db.session.query(func.sum(Bill.totalCost).label('sum'), Bill.dateConfirm).group_by(Bill.dateConfirm).all()
        for i in SumDoanhSoTheoNgay:
            lst.append([i[1].day, i[0]])
        return self.render('admin/analytics.html', lst = lst)

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

admin.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))
admin.add_view(LogoutView(name="Logout"))


