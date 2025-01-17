import os
import uuid
import re
from flask import Flask, render_template, redirect, url_for, request, flash, session, make_response, send_from_directory
from werkzeug.utils import secure_filename
from config import Config
from models import db, User, Product, CartItem

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)



# app.secret_key = os.environ.get('FLASK_SECRET_KEY')
app.secret_key = "234234fwfdfvef3fvefv"
app.config['UPLOAD_FOLDER'] = 'pictures'


def validate_email(email: str) -> bool:
    regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(regex, email) is not None


def validate_password(password: str) -> bool:
    return len(password) >= 8





@app.route("/")
def start():
    db.create_all()
    session.clear()
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        print(f"user id: {session['user_id']}")
        return redirect(url_for('products', link_token=user.link_token))

    elif 'user_id' not in session:
        remember_token = request.cookies.get('remember_token')
        if remember_token:
            user = User.query.filter_by(remember_token=remember_token).first()
            if user:
                if user.username == "admin":
                    return redirect(url_for('add_new_product', link_token=user.link_token))
                session['user_id'] = user.id
                print(f"the user is {user.id} with the token {remember_token}")
                return redirect(url_for('products', link_token=user.link_token))

    # return redirect(url_for('register_page'))
    return redirect(url_for('login_page'))





@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/register/process", methods=["POST"])
def register_process():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    repeat_password = request.form.get('repeat_password')

    if not validate_email(email):
        return redirect(url_for("register_page"), code=302)

    if not validate_password(password):
        flash("Password has to be at least 8 characters")
        return redirect(url_for("register_page"), code=302)

    if password != repeat_password:
        flash('Passwords seem to be different!', 'error')
        return redirect(url_for("register_page"))

    user = User.query.filter_by(email=email).first()
    if user:
        flash("Email has already been used!", 'danger')
        return redirect(url_for('register_page'))

    user = User.query.filter_by(username=username).first()
    if user:
        flash("A user with this username already exists", 'danger')
        return redirect(url_for('register_page'))

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("login_page"))


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/login/process", methods=["POST"])
def login_process():
    email = request.form.get("email")
    password = request.form.get("password")
    remember_me = request.form.get("remember_me")

    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User.query.filter_by(username=email).first()
    if user is None:
        flash("No such user", 'danger')
        return redirect(url_for("login_page"))
    elif not user.check_password(password):
        flash("Wrong password", 'danger')
        return redirect(url_for("login_page"))

    token = str(uuid.uuid4())
    user.link_token = token
    print(f"User's new link token: {user.link_token}")

    session['user_id'] = user.id
    session.permanent = False

    if user.username == "admin":
        resp = make_response(redirect(url_for('add_new_product', link_token=user.link_token)))
    else:
        resp = make_response(redirect(url_for('products', link_token=user.link_token)))

    if not remember_me:
        db.session.commit()
    if remember_me:
        token = str(uuid.uuid4())
        user.remember_token = token
        db.session.commit()
        resp.set_cookie('remember_token', token, max_age=60 * 60 * 24 * 30)
    return resp


@app.route("/description/<uuid:link_token>")
def description(link_token):
    return render_template("description.html", link_token=link_token)


@app.route("/products/<uuid:link_token>")
def products(link_token):
    user = User.query.filter_by(link_token=str(link_token)).first()
    products1 = Product.query.all()
    cart_items = CartItem.query.filter_by(user_id=user.id).all()
    sum = 0
    for i in cart_items:
        sum += (i.price * i.quantity)
    sum = round(sum, 2)
    return render_template('product.html', products=products1, link_token=link_token,
                           amount_of_products=len(products1), cart=cart_items, sum=sum)


@app.route('/products/add_to_cart/<uuid:link_token>/<product_id>', methods=["POST"])
def add_to_cart(link_token, product_id):
    user = User.query.filter_by(link_token=str(link_token)).first()
    product = Product.query.filter_by(id=product_id).first()
    cart_item = CartItem.query.filter_by(product_id=product_id, user_id=user.id).first()
    if cart_item is None:
        cart_item = CartItem(filename=product.filename,
                             name=product.name,
                             price=product.price,
                             quantity=int(request.form.get('quantity')),
                             user_id=user.id,
                             product_id=product_id)
        db.session.add(cart_item)
    else:
        cart_item.quantity = cart_item.quantity + int(request.form.get('quantity'))
    db.session.commit()
    print(f"cart_item user_id: {cart_item.user_id}, product_id: {cart_item.product_id}")
    print(f'Product quantity: {cart_item.quantity}')
    return redirect(url_for('products', link_token=link_token))


@app.route("/products/delete/<uuid:link_token>/<id>", methods=["POST"])
def delete_from_cart(id, link_token):
    user = User.query.filter_by(link_token=str(link_token)).first()
    cart_item = CartItem.query.filter_by(user_id=user.id, product_id=id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
    return redirect(url_for("products", link_token=link_token))


@app.route("/checkout/<uuid:link_token>")
def checkout(link_token):
    user = User.query.filter_by(link_token=str(link_token)).first()
    print(f"Add_new_product\nlink token: {link_token}, user: {user}")
    cart_items = CartItem.query.filter_by(user_id=user.id).all()
    sum = 0
    for i in cart_items:
        sum += (i.price * i.quantity)
    sum = round(sum, 2)
    return render_template("checkout_page.html", products=cart_items, link_token=link_token, sum=sum)


@app.route("/final_page/<uuid:link_token>")
def final_page(link_token):
    user = User.query.filter_by(link_token=str(link_token)).first()
    print(f"Final Page\nlink token: {link_token}, user: {user}")
    cart_items = CartItem.query.filter_by(user_id=user.id).all()
    if cart_items:
        for cart_item in cart_items:
            db.session.delete(cart_item)
        db.session.commit()
    return redirect("https://www.youtube.com/watch?v=q-Y0bnx6Ndw")


@app.route("/admin/add/<uuid:link_token>")
def add_new_product(link_token):
    return render_template("add_new_product.html", link_token=link_token)


@app.route("/admin/add/process/<uuid:link_token>", methods=["POST"])
def add_new_product_process(link_token):
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    picture = request.files['picture']
    if picture:
        filename = secure_filename(picture.filename)
        picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    new_product = Product(name=name, description=description, filename=filename, price=price)
    db.session.add(new_product)
    db.session.commit()
    print(f"New product: {new_product.name}")
    print(f"Description: {new_product.description}")
    print(f"Picture: {new_product.filename}")
    return render_template("add_new_product.html", link_token=link_token)


@app.route("/admin/delete/<uuid:link_token>")
def delete_product(link_token):
    products1 = Product.query.all()
    return render_template("delete_product.html", products=products1, link_token=link_token)


@app.route("/admin/delete/process/<uuid:link_token>/<product_id>", methods=["DELETE"])
def delete_product_process(link_token, product_id):
    product = Product.query.filter_by(id=product_id).first()
    cart_items = CartItem.query.filter_by(product_id=product_id).all()
    if cart_items:
        for cart_item in cart_items:
            db.session.delete(cart_item)
    db.session.delete(product)
    db.session.commit()
    return render_template("delete_product.html", link_token=link_token)


@app.route('/products/pictures/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/logout/<uuid:link_token>")
def logout(link_token):
    user = User.query.filter_by(link_token=str(link_token)).first()
    print(f"Logout\nlink token: {link_token}, user: {user}")

    session.pop('user_id', None)
    resp = make_response(redirect(url_for('login_page')))
    resp.delete_cookie('remember_token')
    user.remember_token = None
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)