from __init__ import app
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from admin_models import *
from __init__ import login
from models import User
from flask_login import login_user, logout_user
import hashlib
import utils


@app.route('/pay')
def payment():
    return render_template('payment.html')


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
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')

    if id in cart:      #co hang trong gio
        cart[id]['quantity'] +=1

    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }
    session['cart'] = cart


    total_quantity, total_amount = utils.cart_stats(cart)

    return jsonify({
        "total_amount": total_amount,
        "total_quantity": total_quantity,
        "cart": cart
    })

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/index')
def index2():
    return render_template('base/base.html')


if __name__ == "__main__":
    app.run(port=8999, debug=True)


# dang nhap admin, pass 123
# insert mysql admin, pass 202cb962ac59075b964b07152d234b70