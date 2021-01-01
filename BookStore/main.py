from __init__ import app
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from admin_models import *
from __init__ import login
from models import User
from flask_login import login_user, logout_user
import hashlib
import utils

@app.route("/")
def index():
    return render_template('base/base.html',  list_book= utils.load_Book(), list_book_image=utils.load_book_image())

@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods = ['get', 'post'])
def login_admin():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = hashlib.md5(password.encode("utf-8")).hexdigest()
        user = User.query.filter(User.username == username, User.password == password).first()

        if user:
            flash('Logged in successfully.')
            login_user(user=user)
        else:
            flash("Login failed !", category='error')

    return redirect('/')

# @app.route('/1')
# def listBook():
#     return render_template('base/banner_bottom.html', list_book= utils.load_Book(), list_book_image=utils.load_book_image())

@app.route('/api/cart', methods=['get' , 'post'])
def add_to_cart():
    # if 'cart' not in session:
    #     session['cart'] = {}

    # cart = session['cart']
    data = request.json
    id_book = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')

    id_cart, list_item = utils.list_item_of_user(1)

    flag = 0
    for item in list_item:
        if (str(item.idBook) == id_book):
            item.quantity += 1
            flag = 1
            db.session.commit()
    if (flag == 0):
        newitem = CartItem(idCart=id_cart, idBook=id_book, quantity=1, price=price, discount=price)
        db.session.add(newitem)
        db.session.commit()

    # if id_book in cart:      #co hang trong gio
    #     cart[id]['quantity'] +=1
    #
    # else:
    #     cart[id] = {
    #         "id": id,
    #         "name": name,
    #         "price": price,
    #         "quantity": 1
    #     }
    # session['cart'] = cart
    #
    #
    # total_quantity, total_amount = utils.cart_stats(cart)

    # return jsonify({
    #     "total_amount": 1,
    #     "total_quantity": 1,
    #     # "cart": cart
    # })


@app.route('/pay')
def payment():
    id_cart, list_item = utils.list_item_of_user_name_book(current_user.id)
    total_quantity, total_amount = utils.cart_stats(current_user.id)
    return render_template('payment.html', id_cart = id_cart, list_item = list_item, total_amount = total_amount, total_quantity=total_quantity)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/index')
def index2():
    return render_template('base/base.html')

@app.route('/api/pay', methods=['post'])
def pay():
    pass

if __name__ == "__main__":
    app.run(port=8999, debug=True)


# dang nhap admin, pass 123
# insert mysql admin, pass 202cb962ac59075b964b07152d234b70