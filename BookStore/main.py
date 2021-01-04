from __init__ import app
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from admin_models import *
from __init__ import login
from models import User
from flask_login import login_user, logout_user, login_required
import hashlib
import utils



import os
import urllib.request
from flask import flash, url_for
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/infoImage', methods=['get', 'post'])
def upload_image():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # print('upload_image filename: ' + filename)
    id = request.form.get("idUser")
    user = User.query.get(id)
    user.avatar = 'images/' + filename
    db.session.commit()
    return render_template('info.html',  list_book_category=utils.get_book_category())


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='images/' + filename), code=301)


@app.route('/info')
def info():
    return render_template('info.html',  list_book_category=utils.get_book_category())



@app.route("/")
def index():
    return render_template('base/base.html', list_recommend_book = utils.recommend_book(), list_best_sale_book= utils.best_sale_book(), list_book_image=utils.load_book_image(), list_book_category=utils.get_book_category())

@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)


@app.route('/info', methods = ['get', 'post'])
def updateInfoUser():
    err_msg = ""
    if request.method == 'POST':
        id = request.form.get("idUser")
        user = User.query.get(id)
        user.lname = request.form.get("lname")
        user.fname = request.form.get("fname")
        user.birthday = request.form.get("birthday")
        user.phone = request.form.get("phone")
        user.address = request.form.get("address")

        db.session.commit()
        return render_template('info.html', list_book_category=utils.get_book_category())


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

@app.route('/register', methods=['post'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        password2 = request.form.get("password2", "")
        if(password == password2):
            password = hashlib.md5(password.encode("utf-8")).hexdigest()
            user = User(username = username, password= password, idUserType=2)
            db.session.add(user)
            db.session.commit()
            return  redirect('/login')
    return redirect('/')





@app.route('/api/cart', methods=['get' , 'post'])
def add_to_cart():
    data = request.json
    id_book = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')
    quantity = data.get('quantity')

    id_cart, list_item = utils.list_item_of_user(current_user.id)

    flag = 0
    for item in list_item:
        if (str(item.idBook) == id_book):
            item.quantity += quantity
            flag = 1
            db.session.commit()
    if (flag == 0):
        newitem = CartItem(idCart=id_cart, idBook=id_book, quantity=quantity, price=price, discount=price)
        db.session.add(newitem)
        db.session.commit()

    return jsonify({
        "message": "Them thanh cong"
    })


@app.route('/pay')
@login_required
def payment():
    id_cart, list_item = utils.list_item_of_user(current_user.id)
    total_quantity, total_amount = utils.cart_stats(current_user.id)
    return render_template('payment.html', id_cart = id_cart, list_item = list_item, total_amount = total_amount, total_quantity=total_quantity,list_book_category=utils.get_book_category())

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/index')
def index2():
    return render_template('base/base.html',list_book_category=utils.get_book_category())

@app.route('/api/pay', methods=['post'])
def pay():
    try:
        data = request.json
        id_user = data.get('id_user')
        id_cart = data.get('cart')
        bill = Bill(idUser = id_user, address_delivery='1', phone_delivery='1', name_delivery='1')
        db.session.add(bill)
        cart = utils.get_item_by_id_cart(id_cart)
        for p in cart:
            if(p.would_buy ==1):
                bill_detail = BillDetail(Bill=bill, idBook=p.idBook, price=p.discount, quantity=p.quantity)
                db.session.add(bill_detail)
                db.session.delete(p)

        db.session.commit()
        return jsonify({
            'message':'success'
        })
    except:
        return jsonify({
            'message': 'failed'
                       })

@app.route('/api/delete/<item_id>', methods=['delete'])
def delete_item(item_id):
    print(item_id)
    id_cart, list_item =utils.list_item_of_user(current_user.id)
    for item in list_item:
        if(str(item.id) == item_id):
            print(item.id == item_id)
            db.session.delete(item)
            db.session.commit()
            return jsonify({
                'message': 'Xóa thành công'
            })
    return jsonify({
        'message': 'Xóa thất bại'
    })


@app.route('/search', methods=['GET', 'POST'])
def search():
    # if request.method == "POST":
    #     name=request.form.get('Search')
    #     found_book=next(name for name in Book if Book.name==name)
    #     cursor.executemany('''select * from Book where name = %s''', )
    #     return render_template("search.html", records=cursor.fetchall())

    name=request.form.get('Search')
    #filters = [dict(name='name', op='like', val='%y%')]
    listBook = Book.query.filter(Book.name.like('%' + name + '%')).all()

    n = len(listBook)
    return render_template('search.html', listBook = listBook , list_book_category=utils.get_book_category(),len = n,  listImage = utils.loadImageByListIdBook(listBook))


# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     if request.method == "POST":
#         name=request.form.get('Search')
#     #     found_book=next(name for name in Book if Book.name==name)
#     #     cursor.executemany('''select * from Book where name = %s''', )
#     #     return render_template("search.html", records=cursor.fetchall())
#     return render_template('search.html',list_book_category=utils.get_book_category())


@app.route('/search/<id_category>', methods=['GET', 'POST'])
def searchCategory(id_category):
    listcate = Book.query.filter(Book.idCategory == id_category).all()
    n = len(listcate)
    return render_template('search.html', listBook=listcate, len = n, listImage = utils.loadImageByListIdBook(listcate), list_book_category=utils.get_book_category(),list_book= utils.load_Book(), list_book_image=utils.load_book_image())

@app.route('/book')
def book():
    products = Book.query.all()
    # if request.method == "POST":
    #     name=request.form.get('Search')
    #     found_book=next(name for name in Book if Book.name==name)
    #     cursor.executemany('''select * from Book where name = %s''', )
    #     return render_template("search.html", records=cursor.fetchall())
    return render_template('list'
                           'book.html', products=products, list_book_category=utils.get_book_category())

@app.route('/single/<int:id_book>', methods=['GET'])
def load_detail_book_by_id(id_book):
    book=utils.get_book_by_id(id_book)
    return render_template('single.html', book = book, list_image = utils.get_image_by_id_book(id_book),list_book_category=utils.get_book_category())


@app.route('/api/check_would_buy', methods=['POST'])
def check_would_buy():
    data = request.json
    id_cart_item = data.get('id')
    check = data.get('checked')
    cart_item = utils.get_item_cart_by_id(id_cart_item)
    if(check):
        cart_item.would_buy = 1
    else:
        cart_item.would_buy = 0
    db.session.commit()
    return jsonify({
        'message': 'success'
    })




if __name__ == "__main__":
    app.run(port=8999, debug=True)


# dang nhap admin, pass 123
# insert mysql admin, pass 202cb962ac59075b964b07152d234b70