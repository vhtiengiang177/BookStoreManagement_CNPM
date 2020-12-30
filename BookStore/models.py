from sqlalchemy import Column, Integer, Float, Boolean, Date, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from __init__ import db
from datetime import datetime, date
from flask_login import UserMixin

class BookCategory(db.Model):
    __tablename__ = 'BookCategory'
    # __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    book_category = relationship('Book', backref='BookCategory', lazy=True)

    def __str__(self):
        return self.name


class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    quantity = Column(Integer, default=0)
    author = Column(String(50))
    decription = Column(String(255))
    sold = Column(Integer, default=0)
    pulisher = Column(String(50))
    price = Column(Integer, nullable=False, default=0)
    discount = Column(Float, default=0)

    idCategory = Column(Integer, ForeignKey(BookCategory.id))

    bill_detail = relationship("BillDetail", backref="book", lazy=True)
    cart_item = relationship("CartItem", backref="book", lazy=True)
    id_imageBook = relationship("Image", backref="book", lazy=True)

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

    # def __str__(self):
    #     return self.name

class CartItem(db.Model):
    __tablename__ = "CartItem"
    id = Column(Integer, primary_key=True, autoincrement=True)
    idCart = Column(Integer, ForeignKey(Cart.id))
    idBook = Column(Integer, ForeignKey(Book.id))
    quantity = Column(Integer, default=1)
    price = Column(Integer)
    discount = Column(Float)

    # def __str__(self):
    #     return self.name



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


class Image(db.Model):
    __tablename__ = "Image"

    id = Column(Integer, primary_key=True, autoincrement=True)
    img= Column(String(255))

    id_book = Column(Integer, ForeignKey(Book.id))


if __name__ == '__main__':
    pass
    # db.drop_all()
    # db.create_all()
    #
    # cat1 = BookCategory(name='Tiểu thuyết')
    # cat2 = BookCategory(name='Truyện ngắn')
    # cat3 = BookCategory(name='Ngôn tình')
    # cat4 = BookCategory(name = '12 cung hoàng đạo')
    # cat5 = BookCategory(name='Trinh thám')
    # cat6 = BookCategory(name = 'Quản trị- Lãnh đạo')
    # cat7 = BookCategory(name = 'Marketing')
    # cat8 = BookCategory(name = 'Phân tích kinh tế')
    # cat9 = BookCategory(name = 'Truyện thiếu nhi')
    # cat10 = BookCategory(name = 'Tô màu, luyện chữ')
    # cat11 = BookCategory(name = 'Sách kiến thức- kĩ năng sống cho trẻ')
    #
    # b1 = Book(name = 'Con chim xanh biếc bay về', quantity=10, author='Nguyễn Nhật Ánh', decription='Truyện ngắn', sold=0, pulisher='Nhà xuất bản Trẻ', price = 112000, discount = 0.2, idCategory=2)
    #
    # b2 = Book(name = 'Vui vẻ không quạu nha', quantity=10, author='Ở Đây Vui Nè', decription='Sách kiến thức- kĩ năng sống cho trẻ', sold=0, pulisher='Nhà xuất bản Phụ nữ Việt Nam', price = 41000, discount = 0.2, idCategory=11)
    #
    # b3 = Book(name = 'Hôm nay em có ổn không', quantity=10, author='Hall of Dreamers', decription='Truyện Ngắn', sold=0, pulisher='Nhà xuất bản Hà Nội', price = 59000, discount = 0.1, idCategory=2)
    #
    # img1 = Image(img='images/3.jpg', id_book=1)
    # img2 = Image(img='images/4.jpg', id_book=1)
    # img3 = Image(img='images/5.jpg', id_book=2)
    # img4 = Image(img='images/6.jpg', id_book=3)
    # img5 = Image(img='images/7.jpg', id_book=3)
    # img6 = Image(img='images/8.jpg', id_book=3)
    # db.session.add(cat1)
    # db.session.add(cat2)
    # db.session.add(cat3)
    # db.session.add(cat4)
    # db.session.add(cat5)
    # db.session.add(cat6)
    # db.session.add(cat7)
    # db.session.add(cat8)
    # db.session.add(cat9)
    # db.session.add(cat10)
    # db.session.add(cat11)
    # db.session.add(b1)
    # db.session.add(b2)
    # db.session.add(b3)
    # db.session.add(img1)
    # db.session.add(img2)
    # db.session.add(img3)
    # db.session.add(img4)
    # db.session.add(img5)
    # db.session.add(img6)
    # db.session.add(img1)
    # db.session.add(img2)
    # db.session.add(img3)
    # db.session.add(img4)
    # db.session.add(img5)
    # db.session.add(img6)
    # db.session.commit()
