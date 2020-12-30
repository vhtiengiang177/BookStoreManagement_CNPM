# from BookStore import db
from models import Book, Image, BookCategory, User
# from flask import session, sessions
# from BookStore.models import User

def load_Book():
    return Book.query.all()

def load_book_image():
    return Book.query.join(Image, Image.id_book == Book.id).add_column(Image.img)


def chek_login(username, password):
    print(username, password)
    return User.query.filter(User.username == username, User.password == password).first()

def get_user_by_id(user_id):
    return User.query.filter(User.id == user_id).all()


def cart_stats(cart):
    count = 0
    price = 0
    for i in cart.values():
        count = count + i['quantity']
        price = price + i['quantity'] * i['price']
    return count, price