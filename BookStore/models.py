from sqlalchemy import Column, Integer, Float, Boolean, Date, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from __init__ import db
from datetime import datetime, date
from flask_login import UserMixin

class BookCategory(db.Model):
    __tablename__ = 'BookCategory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    book_category = relationship('Book', backref='BookCategory', lazy=True)

    def __str__(self):
        return self.name


class Book(db.Model):
    __tablename__ = 'Book'

    id=Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String(50), nullable=False)
    quantity = Column(Integer, default=0)
    author = Column(String(50))
    decription = Column(String(255))
    sold = Column(Integer, default=0)
    pulisher = Column(String(50))
    price = Column(Integer, nullable=False, default=0)

    idCategory = Column(Integer, ForeignKey(BookCategory.id))

    bill_detail = relationship("BillDetail", backref="Book", lazy=True)
    cart_item = relationship("CartItem", backref = "Book", lazy = True)

    def __str__(self):
        return self.name


class Voucher(db.Model):
    __tablename__ = 'Voucher'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    startDate = Column(Date, nullable=False, default=date.today())
    endDate = Column(Date, nullable=False, default=date.today())
    description = Column(String(255))
    discount = Column(Float, default=0)

    bill_detail = relationship('BillDetail', backref = 'Voucher', lazy=True)

    def __str__(self):
        return self.name

# class Customer(db.Model):
#     __tablename__ = 'Customer'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)
#     birthday = Column(Date, default=date.today())
#     address = Column(String(50))
#     phone =  Column(String(50))
#     gender = Column(Boolean, default=True)  #True = 1= Nam, False = 0= Nữ
#     bill = relationship('Bill', backref='Customer', lazy=True)
#
#     def __str__(self):
#         return self.name

class UserType(db.Model):
    __tablename__ = "UserType"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_type = Column(String(50), nullable=False)

    idUser = relationship("User", backref = "UserType", lazy=True)

    def __str__(self):
        return self.name_type

class User(db.Model, UserMixin):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, autoincrement=True)
    lname = Column(String(50))
    fname = Column(String(50))
    username = Column(String(50), unique=True)
    password = Column(String(50))
    avatar = Column(String(50))
    birthday = Column(Date, default=date.today())
    address = Column(String(50))
    gender = Column(Integer, default=0) #0 nu 1 nam
    phone = Column(String(50))

    idUserType = Column(Integer, ForeignKey(UserType.id))
    idBill = relationship("Bill", backref = "User", lazy = True)
    idCart = relationship("Cart", backref = "User", lazy = True)

    def __str__(self):
        return self.lname + self.fname




class Cart(db.Model):
    __tablename__ = "Cart"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey(User.id))
    total_quantity = Column(Integer)

    idCartItem = relationship("CartItem", backref = "Cart", lazy = True)

    def __str__(self):
        return self.name

class CartItem(db.Model):
    __tablename__ = "CartItem"
    id = Column(Integer, primary_key=True, autoincrement=True)
    idCart = Column(Integer, ForeignKey(Cart.id))
    idBook = Column(Integer, ForeignKey(Book.id))
    quantity = Column(Integer, default=1)
    price = Column(Integer)
    discount = Column(Float)

    def __str__(self):
        return self.name



class Bill(db.Model):
    __tablename__ = "Bill"

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_price = Column(Float)
    order_time = Column(DateTime, default=datetime.now())
    address_delivery = Column(String(50), nullable=False)
    phone_delivery = Column(String(50), nullable=False)
    name_delivery = Column(String(50), nullable=False)

    idVoucher = Column(Integer, ForeignKey(Voucher.id))
    idUser = Column(Integer, ForeignKey(User.id))
    idBillDetail = relationship("BillDetail", backref = "Bill", lazy = True)

    def __str__(self):
        return self.name


class BillDetail(db.Model):
    __tablename__ = "BillDetail"

    id = Column(Integer, primary_key=True, autoincrement=True)
    idBill = Column(Integer, ForeignKey(Bill.id))
    idBook = Column(Integer, ForeignKey(Book.id))
    price = Column(Integer)
    quantity =Column(Integer)

    idVoucher = Column(Integer, ForeignKey(Voucher.id))

    def __str__(self):
        return self.name

if __name__ == '__main__':
    db.create_all()