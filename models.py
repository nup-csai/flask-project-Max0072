from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    # Определяем столбцы таблицы
    id = db.Column(db.Integer, primary_key=True)  # primary_key=True - это уникальный идентификатор
    username = db.Column(db.String(120), unique=True, nullable=False)  # уникальное имя пользователя
    email = db.Column(db.String(120), unique=True, nullable=False)  # уникальный email
    password_hash = db.Column(db.String(128), nullable=False)  # хеш пароля
    remember_token = db.Column(db.String(128), nullable=True, default=None)
    link_token = db.Column(db.String(128), unique=True, nullable=True, default=None)

    # Конструктор для удобства
    def __repr__(self):
        return f'<User {self.username}>'

    # Методы для работы с паролем (хеширование и проверка)
    def set_password(self, password):
        """Метод для хеширования пароля перед его сохранением"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Метод для проверки пароля при авторизации"""
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=True)  # Путь к картинке
    price = db.Column(db.Float, nullable=False)
    cart = db.Column(db.Boolean, nullable=False, default=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    def __repr__(self):
        return f'<Product {self.name}>'


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(255), nullable=True)  # Путь к картинке
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    # связи с моделями
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))
