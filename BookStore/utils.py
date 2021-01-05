# from BookStore import db
from models import Book, Image, BookCategory, User, Cart, CartItem, BillDetail, Bill
from __init__ import db
from sqlalchemy import desc,  asc
# from flask import session, sessions
# from BookStore.models import User

def loadImageByListIdBook(listBook):
    list_image = []
    for book in listBook:
        image = Image.query.filter(Image.id_book == book.id).all()
        image = image *8
        image = image[0:8]
        list_image.append(image)
    return list_image


def loadImageByIdBook(id_book):
    return Image.query.filter(Image.id_book == id_book).all()

def infoUser(id_user):
    return User.query.filter(User.id_user == id_user).first()

def load_Book():
    return Book.query.all()

def load_book_image():
    list_book = load_Book()
    list_image =[]
    list_temp=[]
    for item in list_book:
        image = Image.query.filter(Image.id_book == item.id).all()
        list_temp.append(image)
    for i in list_temp:
        item2 = i*8
        item2 = item2[0:8]
        list_image.append(item2)
    return list_image

    # return Book.query.join(Image, Image.id_book == Book.id).add_column(Image.img)
#load_book_image()


def chek_login(username, password):
    print(username, password)
    return User.query.filter(User.username == username, User.password == password).first()

def get_user_by_id(user_id):
    return User.query.filter(User.id == user_id).all()


def cart_stats(id_user):
    count = 0
    price = 0

    id_cart , list_item = list_item_of_user(id_user)


    for i in list_item:
        count = count + i.quantity
        price = price + i.quantity * i.discount
    return count, price

def list_item_of_user(id_user):
    cart = Cart.query.filter(Cart.id_user == id_user).all()
    if(cart!=[]):
        id_cart = cart[0].id
    else:
        newcart = Cart(id_user=id_user)
        db.session.add(newcart)
        db.session.commit()
        id_cart = Cart.query.filter(Cart.id_user == id_user).first().id

    list_item = CartItem.query.filter(CartItem.idCart == id_cart).all()

    return id_cart, list_item

def list_item_of_user_name_book(id_user):
    cart = Cart.query.filter(Cart.id_user == id_user).all()
    if (cart != []):
        id_cart = cart[0].id
    else:
        newcart = Cart(id_user=id_user)
        db.session.add(newcart)
        db.session.commit()
        id_cart = Cart.query.filter(Cart.id_user == id_user).first().id

    list_item = CartItem.query.filter(CartItem.idCart == id_cart).join(Book, Book.id == CartItem.idBook).add_column(Book.name).all()

    return id_cart, list_item


def add_receipt(id_user):
    bill = Bill(id_user = id_user)
    db.session.add(bill)

    id_cart, list_item = list_item_of_user(id_user)

def get_item_by_id_cart(id_cart):
    return CartItem.query.filter(CartItem.idCart == id_cart).all()


def get_book_category():
    return BookCategory.query.all()

def get_book_by_id(id_book):
    return Book.query.filter(Book.id == id_book).first()

def get_image_by_id_book(id_book):
    return Image.query.filter(Image.id_book ==id_book).all()

def get_item_cart_by_id(id_item):
    return CartItem.query.filter(CartItem.id == id_item).first()

def best_sale_book():
    return Book.query.order_by(desc(Book.sold)).all()[0:3]

def recommend_book():
    return Book.query.all()[::-1][0:3]

def recommend_bookNew():
    return Book.query.all()[::-1][0:4]


