from __init__ import admin, db
from models import Category, Book, Voucher, Customer, Bill, User
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Book, db.session))
admin.add_view(ModelView(Voucher, db.session))
admin.add_view(ModelView(Customer, db.session))
admin.add_view(ModelView(Bill, db.session))
# admin.add_view(ModelView(Account, db.session))


