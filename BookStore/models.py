from __init__ import db
from sqlalchemy import Column, Integer, Float, Boolean, Date, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime, date


class UserType(db.Model):
    __tablename__ = "UserType"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_type = Column(String(50), nullable=False)

    id_user = relationship("User", backref="UserType", lazy=True)

    def __str__(self):
        return self.name_type

class User(db.Model, UserMixin):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True)
    password = Column(String(50))
    phone = Column(String(50), unique=True)
    active_phone = Column(Boolean, default=False)
    mail = Column(String(50), unique=True)
    active_mail = Column(Boolean, default=False)
    state_block = Column(Boolean, default=False)
    avatar = Column(String(50), default='images/user.jpg')
    name = Column(String(50), default='')
    birthday = Column(Date, default=date.today())
    address = Column(String(50), default='')
    district = Column(String(50), default='')
    city = Column(String(50), default='')
    gender = Column(Integer, default=0) #0 nu 1 nam

    id_UserType = Column(Integer, ForeignKey(UserType.id))  ##
    id_bill = relationship("Bill", backref = "User", lazy = True)
    id_cart = relationship("Cart", backref = "User", lazy = True)

    def __str__(self):
        return self.name

class BookCategory(db.Model):
    __tablename__ = 'BookCategory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    book_category = relationship('Book', backref='BookCategory', lazy=True)

    def __str__(self):
        return self.name

class Book(db.Model):
    __tablename__ = 'Book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    author = Column(String(50), default='')
    description = Column(String(255), default='')
    publisher = Column(String(50), default='')
    sold = Column(Integer, default=0)
    import_number = Column(Integer, default=0)
    price = Column(Integer, nullable=False, default=0)
    discount = Column(Float, default=0)

    id_category = Column(Integer, ForeignKey(BookCategory.id))  ##
    id_ImportBook = relationship('ImportBook', backref = 'Book', lazy=True)
    id_billDetail = relationship("BillDetail", backref = "Book", lazy=True)
    id_cartItem = relationship("CartItem", backref = "Book", lazy = True)
    id_image = relationship("Image", backref = "Book", lazy = True)

    def __str__(self):
        return self.name

class Supplier(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), default='')

    id_importbook = relationship("ImportBook", backref='Supplier', lazy=True)

    def __str__(self):
        return self.name

class ImportBook(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_book = Column(Integer, ForeignKey(Book.id))  #
    amount = Column(Integer, default=0)
    price_import = Column(Integer)
    date_import = Column(Date, default=date.today())
    id_supplier = Column(Integer, ForeignKey(Supplier.id))  #

class Bill(db.Model):
    __tablename__ = "Bill"

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_price = Column(Integer)
    order_time = Column(DateTime, default=datetime.now())
    intend_time = Column(DateTime, default=datetime(int(datetime.now().strftime("%Y")), int(datetime.now().strftime("%m")), int(datetime.now().strftime("%d"))+3))
    confirm_time = Column(DateTime)
    phone = Column(String(50), default='')
    address_delivery = Column(String(50), nullable=False)
    name_delivery = Column(String(50), nullable=False)
    status = Column(Integer, default=1)

    id_user = Column(Integer, ForeignKey(User.id))      #
    id_billDetail = relationship("BillDetail", backref = "Bill", lazy = True)

    def __str__(self):
        return str(self.id)

class BillDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_bill = Column(Integer, ForeignKey(Bill.id))      #
    id_book = Column(Integer, ForeignKey(Book.id))      #
    price = Column(Integer)
    quantity = Column(Integer, default=0)

    def __str__(self):
        return self.id

class Cart(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey(User.id)) #
    total_amount = Column(Integer, default=0)
    total_price = Column(Integer, default=0)

    id_cart_item = relationship("CartItem", backref="Cart", lazy=True)

class CartItem(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cart = Column(Integer, ForeignKey(Cart.id))      #
    id_book = Column(Integer, ForeignKey(Book.id))      #
    quantity = Column(Integer, default=1)
    price = Column(Integer, default= 0)
    discount = Column(Float, default=0)
    would_buy = Column(Integer, default=1)

class Image(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    image = Column(String(255), default='images/user.jpg')

    id_book = Column(Integer, ForeignKey(Book.id))  #


if __name__ == '__main__':
    pass
    #db.create_all()

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
    # b1 = Book(name = 'Con chim xanh biếc bay về',  author='Nguyễn Nhật Ánh', description='Truyện ngắn', publisher='Nhà xuất bản Trẻ', price = 112000, discount = 0.2, id_category=2)
    #
    # b2 = Book(name = 'Vui vẻ không quạu nha', author='Ở Đây Vui Nè', description='Sách kiến thức- kĩ năng sống cho trẻ', publisher='Nhà xuất bản Phụ nữ Việt Nam', price = 41000, discount = 0.2, id_category=11)
    #
    # b3 = Book(name = 'Hôm nay em có ổn không', author='Hall of Dreamers', description='Truyện Ngắn', publisher='Nhà xuất bản Hà Nội', price = 59000, discount = 0.1, id_category=2)
    #
    # typeAdmin = UserType(name_type = 'admin')
    # typeUser = UserType(name_type = 'user')
    # db.session.add(typeAdmin)
    # db.session.add(typeUser)
    #
    #
    #
    # admin = User(username = 'admin@gmail.com', password = '202cb962ac59075b964b07152d234b70', phone='0563406033', active_phone=True, mail= 'admin@gmail.com', active_mail=True, name='Lê Nguyễn Gia Bảo', avatar='images/avt.jpg', id_UserType=1, gender=1)
    # db.session.add(admin)
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
    #
    # db.session.commit()
    #






