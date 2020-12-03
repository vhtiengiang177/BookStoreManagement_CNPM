from sqlalchemy import Column, Integer, Float, Boolean, Date, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from __init__ import db
from datetime import date
from flask_login import UserMixin

class Category(db.Model):
    __tablename__ = 'Category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    books = relationship('Book', backref='Category', lazy=True)


class Book(db.Model):
    __tablename__ = 'Book'

    id=Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String(50), nullable=False)
    quantity = Column(Integer, default=0)
    author = Column(String(50))
    decription = Column(String(255))
    sold = Column(Integer, default=0)
    pulisher = Column(String(50))
    idCategory = Column(Integer, ForeignKey(Category.id))


class Voucher(db.Model):
    __tablename__ = 'Voucher'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    startDate = Column(Date, nullable=False, default=date.today())
    endDate = Column(Date, nullable=False, default=date.today())
    detail = Column(String(255))
    discount = Column(Float, default=0)
    bills = relationship('Bill', backref = 'Voucher', lazy=True)

class Customer(db.Model):
    __tablename__ = 'Customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    birthday = Column(Date, default=date.today())
    address = Column(String(50))
    phone =  Column(String(50))
    gender = Column(Boolean, default=True)  #True = 1= Nam, False = 0= Nữ
    bill = relationship('Bill', backref='Customer', lazy=True)

class Bill(db.Model):
    __tablename__ = "Bill"
    id = Column(Integer, primary_key=True, autoincrement=True)
    idCustomer = Column(Integer, nullable=False)
    address = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    dateConfirm = Column(Date, default=date.today())
    idVoucher = Column(Integer, ForeignKey(Voucher.id))
    totalCost = Column(Float)
    idCustomer = Column(Integer, ForeignKey(Customer.id))

class User(db.Model, UserMixin):
    __tablename__ = 'User'

    id=Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avater =Column(String(100))
    active = Column(Boolean, default=True)

if __name__ == '__main__':
    db.create_all()