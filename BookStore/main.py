from __init__ import app
from flask import Flask, render_template, request, redirect, flash, session, jsonify,Response
from admin_models import *
from __init__ import login
from models import User
from flask_login import login_user, logout_user, login_required
import hashlib
import random
import math
import os
import urllib.request
from flask import flash, url_for
from werkzeug.utils import secure_filename
from authy.api import AuthyApiClient
import utils
import smtplib
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
s = URLSafeTimedSerializer('thisissecret!')


app.config['CSRF_ENABLED'] = True
app.config['USER_ENABLE_EMAIL'] = True
app.config.from_pyfile('config.cfg')
mail = Mail(app)
mail.init_app(app)
app.config.from_object('config')
app.secret_key = 'super-secret'
api = AuthyApiClient(app.config['AUTHY_API_KEY'])


@app.route('/about')
def about():
    return render_template('about.html',  list_book_category=utils.get_book_category())


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
    return render_template('base/base.html',list_recommend_book_new = utils.recommend_bookNew(), list_recommend_book = utils.recommend_book(), list_best_sale_book= utils.best_sale_book(), list_book_image=utils.load_book_image(), list_book_category=utils.get_book_category())

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


#Thao
@app.route('/login', methods = ['get', 'post'])
def login_admin():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = hashlib.md5(password.encode("utf-8")).hexdigest()
        user = User.query.filter(User.username == username, User.password == password).first()
        if user:
            if (user.active_mail==1):
                flash('Logged in successfully.')
                login_user(user=user)
            elif(user.active_mail==0):
                return '<h1>Please Confirm your email to active account</h1>'
        else:
            flash("Login failed !", category='error')
            return render_template('base/base.html', list_recommend_book_new=utils.recommend_bookNew(),
                                   list_recommend_book=utils.recommend_book(),
                                   list_best_sale_book=utils.best_sale_book(),
                                   list_book_image=utils.load_book_image(),
                                   list_book_category=utils.get_book_category(), err='sai tai khoan hoac mat khau')
    return redirect('/')

#Thao

@app.route('/register', methods=['post'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        password2 = request.form.get("password2", "")
        phone = request.form.get("phonenumber")
        if(password == password2 ):
            password = hashlib.md5(password.encode("utf-8")).hexdigest()
            user = User(username=username, password=password, id_UserType=2,phone=phone)
            db.session.add(user)
            token = s.dumps(username, salt='email-confirm')
            TEXT = 'Thannks for sign up! Please enter this link to active your account: http://127.0.0.1:8999/confirm_email/'+token+'/'+username
            SUBJECT='BOOKSTORE: Verify Account'
            message = 'Subject: {}\n\n{}'.format( SUBJECT, TEXT)

            server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
            server.login('thaonguyen.201.9b@gmail.com', 'kimdong20012000')
            server.sendmail('thaonguyen.201.9b@gmail.com',username , msg=message)
            db.session.commit()
            return '<h1>Please Confirm your email to active account</h1>'
    return redirect('/')

#Thao
@app.route('/confirm_email/<token>/<userid>')
def confirm_email(token, userid):
    try:
        email = s.loads(token,salt='email-confirm')
    except SignatureExpired:
        return '<h1>Mã confirm đã hết hạn, bạn vui lòng đăng kí lại . </h1>'
    user_id = userid
    user = User.query.filter(User.username==user_id).first()
    user.active_mail=1
    db.session.commit()

    login_user(user=user)
    return redirect('/')

#Thao
@app.route("/phone_verification", methods=["GET", "POST"])
def phone_verification():
    if request.method == "POST":
        country_code = request.form.get("country_code")
        phone_number = request.form.get("phone_number")
        method = request.form.get("method")

        session['country_code'] = country_code
        session['phone_number'] = phone_number

        api.phones.verification_start(phone_number, country_code, via=method)
        return redirect(url_for("verify"))
    return render_template("phone_verification.html")


#Thao
@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        token = request.form.get("token")

        phone_number = session.get("phone_number")
        country_code = session.get("country_code")

        verification = api.phones.verification_check(phone_number,
                                                     country_code,
                                                     token)
        if verification.ok():
            user = User.query.filter(User.phone == phone_number).first()

            #tạo mã code 6 số random
            digits = [i for i in range(0, 10)]
            random_str = ""
            for i in range(6):
                index = math.floor(random.random() * 10)
                random_str += str(digits[index])

            user.password = hashlib.md5(random_str.encode("utf-8")).hexdigest()
            db.session.commit()
            return Response("<h1>Xác thực thành công, bạn vui lòng đăng nhập lại với email đã đăng kí và mật khẩu: " + random_str +"</h1>")
    return render_template("verify.html")



#Thao
@app.route('/email_verification', methods=['post'])
def verifyemail():
    if request.method == 'POST':
        email = request.form.get("username")
        # tạo mã code 6 số random
        digits = [i for i in range(0, 10)]
        random_str = ""
        for i in range(6):
            index = math.floor(random.random() * 10)
            random_str += str(digits[index])

        user = User.query.filter(User.username == email).all()
        if user!=[]:
            user = user[0]
            password = hashlib.md5(random_str.encode("utf-8")).hexdigest()
            user.password = hashlib.md5(random_str.encode("utf-8")).hexdigest()
            db.session.commit()
            TEXT = "Verify Success. Reset your password after SIGN IN with THIS EMAIL and PASS: " + str(random_str)
            SUBJECT = 'BOOKSTORE: Verify Reset Password Account'
            message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

            server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
            server.login('thaonguyen.201.9b@gmail.com', 'kimdong20012000')
            server.sendmail('thaonguyen.201.9b@gmail.com', email, msg=message)
            return '<h1>Please Confirm your email to Reset Password.'+'Back to web: http://127.0.0.1:8999'+'</h1>'
        else:
            return '<h1>Dont found your email in my list cutomer'  + ' Back to web: http://127.0.0.1:8999' + '</h1>'
    return redirect('/')


#Thao
@app.route('/api/cart', methods=['get' , 'post'])
def add_to_cart():
    data = request.json
    id_book = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')
    discount = data.get('discount')
    quantity = data.get('quantity')

    id_cart, list_item = utils.list_item_of_user(current_user.id)

    flag = 0
    for item in list_item:
        if (str(item.id_book) == id_book):
            item.quantity += quantity
            flag = 1
            db.session.commit()
    if (flag == 0):
        newitem = CartItem(id_cart=id_cart, id_book=id_book, quantity=quantity, price=price, discount=price * (1 - discount))
        db.session.add(newitem)
        db.session.commit()

    return jsonify({
        "message": "Them thanh cong"
    })


#Thao
@app.route('/pay')
@login_required
def payment():
    id_cart, list_item = utils.list_item_of_user(current_user.id)
    total_quantity, total_amount = utils.cart_stats(current_user.id)
    return render_template('payment.html', id_cart = id_cart, list_item = list_item, total_amount = total_amount, total_quantity=total_quantity, list_book = utils.load_Book(),list_book_category=utils.get_book_category(), list_image = utils.get_all_image())

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
        name_receiver = data.get('name_receiver')
        phone_number_receiver = data.get('phone_number_receiver')
        address_receiver = data.get('address_receiver')
        print(address_receiver, name_receiver, phone_number_receiver, current_user.id)
        bill = Bill(id_user = current_user.id, address_delivery=address_receiver, phone=phone_number_receiver, name_delivery=name_receiver)
        db.session.add(bill)
        print(bill.id)

        id_cart, list_item = utils.list_item_of_user(current_user.id)

        cart = utils.get_item_by_id_cart(id_cart)
        for p in cart:
            if(p.would_buy==1):
                bill_detail = BillDetail(Bill=bill, id_book=p.id_book, price=p.discount, quantity=p.quantity)
                print(2)
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

@app.route('/confirmpay', methods=['post'])
def confirm_pay():
    id_cart, list_item = utils.list_item_of_user(current_user.id)
    total_quantity, total_amount = utils.cart_stats(current_user.id)
    return render_template('confirm_pay.html', id_cart = id_cart, list_item = list_item, total_amount = total_amount, total_quantity=total_quantity, list_book = utils.load_Book(),list_book_category=utils.get_book_category(), list_image = utils.get_all_image())


@app.route('/api/delete/<item_id>', methods=['delete'])
def delete_item(item_id):
    id_cart, list_item =utils.list_item_of_user(current_user.id)
    for item in list_item:
        if(str(item.id) == item_id):
            db.session.delete(item)
            db.session.commit()
            return jsonify({
                'message': 'Xóa thành công'
            })
    return jsonify({
        'message': 'Xóa thất bại'
    })



@app.route('/api/cart/<item_id>', methods=['post'])
def update_item(item_id):
    id_cart, list_item = utils.list_item_of_user(current_user.id)
    data = request.json
    for item in list_item:
        if (str(item.id) == item_id):
            if('quantity' in data):
                item.quantity = int(data['quantity'])
                db.session.commit()
                total_quantity, total_amount = utils.cart_stats(current_user.id)
                return jsonify(({
                    'code': 200,
                    'total_quantity': total_quantity,
                    'total_amount': total_amount
                }))
    return  jsonify(({
        'code': 500
    }))

#Thao
@app.route('/search', methods=['GET', 'POST'])
def search():
    name=request.form.get('Search')
    listBook = Book.query.filter(Book.name.like('%' + name + '%')).all()

    n = len(listBook)
    return render_template('search.html', listBook = listBook , list_book_category=utils.get_book_category(),len = n,  listImage = utils.loadImageByListIdBook(listBook))


#Thao
@app.route('/search/<id_category>', methods=['GET', 'POST'])
def searchCategory(id_category):
    listcate = Book.query.filter(Book.id_category == id_category).all()
    n = len(listcate)
    return render_template('search.html', listBook=listcate, len = n, listImage = utils.loadImageByListIdBook(listcate), list_book_category=utils.get_book_category(),list_book= utils.load_Book(), list_book_image=utils.load_book_image())



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