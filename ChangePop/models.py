import datetime

from ChangePop import db
from ChangePop import login
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


# A ver, esto es un poco una locura, las funciones que tengan que ver con cada clase
# hay que ponerlas dentro de esa clase, es decir, la api, pero bueno, esto se va rellenando
# poco a poco
# dejo de ejemplo la del hash de la contraseña


class Categories(db.Model):
    __tablename__ = 'Categories'
    cat_name = db.Column(db.String(255), primary_key=True, index=True, nullable=False)

    @staticmethod
    def add_cat(cat_name):
        c = Categories.query.get(cat_name)
        if not (c is not None):
            c = Categories(cat_name=cat_name)
            db.session.add(c)
            db.session.commit()

    def __repr__(self):
        return '{}'.format(self.cat_name)


# noinspection PyArgumentList
class Users(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column(db.String(255), unique=False, nullable=False)
    nick = db.Column(db.String(255), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(255), unique=False, nullable=False)
    ban_reason = db.Column(db.String(255), unique=False, nullable=True)
    ban_until = db.Column(db.Date, unique=False, nullable=True)
    points = db.Column(db.Float, unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    mail = db.Column(db.String(255), index=True, unique=True, nullable=False)
    is_mod = db.Column(db.Boolean, unique=False, nullable=False)
    dni = db.Column(db.String(255), index=True, unique=True, nullable=False)
    avatar = db.Column(db.String(255), unique=False, nullable=False)
    fnac = db.Column(db.Date, unique=False, nullable=False)
    place = db.Column(db.String(255), unique=False, nullable=False)
    pass_hash = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255))
    time_token = db.Column(db.DateTime(timezone=True))
    ts_create = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow())
    ts_edit = db.Column(db.DateTime(timezone=True), onupdate=datetime.datetime.utcnow())

    def get_id(self):
        return self.id

    @staticmethod
    def new_user(nick, last_name, first_name, phone, dni, place, pass_hash, fnac, mail):
        u = Users(nick=nick,
                  last_name=last_name,
                  first_name=first_name,
                  phone=phone,
                  place=place,
                  dni=dni,
                  points=0,
                  fnac=fnac,
                  is_mod=False,
                  mail=mail,
                  avatar="http://127.0.0.1:5000/static/images/logo.jpg"
                  )
        u.set_password(pass_hash)
        db.session.add(u)
        db.session.commit()
        db.session.flush()

        return u.id

    @staticmethod
    def delete_user(id):
        u = Users.query.get(id)
        db.session.delete(u)
        db.session.commit()

    def set_password(self, password):
        """ This funcion set a password to a user after encrypt it

            :param self: The user itself
            :param password: The password to be encrypted
            :type password: str.
            :returns:  str -- Hashed password

            """
        self.pass_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)

    # esto es si no le dices nada, muestra esto de salida al hacer una consulta a esta clase
    def __repr__(self):
        return '{}, {}, {}, {}'.format(self.id, self.nick, self.mail, self.first_name)


# noinspection PyArgumentList
class Products(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(255), unique=False, index=True, nullable=False)
    descript = db.Column(db.String(255), unique=False, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    publish_date = db.Column(db.Date, unique=False, nullable=False, default=datetime.datetime.utcnow())
    ban_reason = db.Column(db.String(255), unique=False, nullable=True)
    bid_date = db.Column(db.Date, unique=False, nullable=True)
    visits = db.Column(db.Integer, unique=False, nullable=False)
    boost_date = db.Column(db.Date, unique=False, nullable=True)
    followers = db.Column(db.Integer, unique=False, nullable=False)
    is_removed = db.Column(db.Boolean, unique=False, nullable=False)
    place = db.Column(db.String(255), unique=False, nullable=False)
    ts_edit = db.Column(db.DateTime(timezone=True), unique=False, nullable=False, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    @staticmethod
    def new_product(user_id, title, descript, price, place):
        p = Products(user_id=user_id,
                     title=title,
                     descript=descript,
                     price=price,
                     place=place,
                     visits=0,
                     followers=0,
                     is_removed=False
                     )
        db.session.add(p)
        db.session.commit()
        db.session.flush()

        return p.id

    def __repr__(self):
        return '{},{},{},{}'.format(self.id, self.tittle, self.user_id)


class Images(db.Model):
    __tablename__ = 'Images'
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'))
    image_url = db.Column(db.String(255), primary_key=True, index=True, nullable=False)

    @staticmethod
    def add_photo(image_url, product_id):
        pp = Images(image_url=image_url, product_id=product_id)
        db.session.add(pp)
        db.session.commit()

    def __repr__(self):
        return '{},{}'.format(self.products_id, self.image_url)


class Reports(db.Model):
    __tablename__ = 'Reports'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, index=True, nullable=False)
    reason = db.Column(db.String(255), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'))
    report_date = db.Column(db.DateTime(timezone=True), index=True, unique=False, nullable=True,
                            default=datetime.datetime.utcnow())

    def __repr__(self):
        return '{},{},{},{}'.format(self.id, self.reason, self.user_id, self.product_id)


class Payments(db.Model):
    __tablename__ = 'Payments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, index=True, nullable=False)
    pay_date = db.Column(db.DateTime(timezone=True), index=True, unique=False, nullable=False,
                         default=datetime.datetime.utcnow())
    amount = db.Column(db.Float, unique=False, nullable=False)
    iban = db.Column(db.String(255), unique=False, nullable=False)
    boost_date = db.Column(db.DateTime(timezone=True), unique=False, nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'))

    def __repr__(self):
        return '{},{},{}'.format(self.id, self.amount, self.product_id)


class Coments(db.Model):
    __tablename__ = 'Coments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, index=True, nullable=False)
    publish_date = db.Column(db.DateTime(timezone=True), index=True, unique=False, nullable=False,
                             default=datetime.datetime.utcnow())
    body = db.Column(db.String(255), unique=False, nullable=False)
    user_to = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user_from = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __repr__(self):
        return '{},{},{},{}'.format(self.id, self.body, self.user_to, self.user_from)


class CatProducts(db.Model):
    __tablename__ = 'CatProducts'
    cat_name = db.Column(db.Integer, db.ForeignKey('Categories.cat_name'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), primary_key=True)

    @staticmethod
    def add_prod(cat_name, product_id):
        cp = CatProducts(cat_name=cat_name, product_id=product_id)
        db.session.add(cp)
        db.session.commit()


    def __repr__(self):
        return '{},{}'.format(self.cat_name, self.product_id)


class Interest(db.Model):
    __tablename__ = 'Interest'
    cat_name = db.Column(db.Integer, db.ForeignKey('Categories.cat_name'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)

    def __repr__(self):
        return '{},{}'.format(self.cat_name, self.user_id)


class Follows(db.Model):
    __tablename__ = 'Follows'
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)

    def __repr__(self):
        return '{},{}'.format(self.product_id, self.user_id)


class Bids(db.Model):
    __tablename__ = 'Bids'
    bid = db.Column(db.Float, unique=False, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    ts_create = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow())

    def __repr__(self):
        return '{},{},{}'.format(self.product_id, self.user_id, self.bid)


class Trades(db.Model):
    __tablename__ = 'Trades'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, index=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'))
    user_sell = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user_buy = db.Column(db.Integer, db.ForeignKey('Users.id'))
    closed = db.Column(db.Boolean, unique=False, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    ts_create = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow())

    def __repr__(self):
        return '{},{},{},{},{}'.format(self.id, self.user_sell, self.user_buy, self.product_id, self.price)


class Messages(db.Model):
    __tablename__ = 'Messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, index=True, nullable=False)
    trade_id = db.Column(db.Integer, db.ForeignKey('Trades.id'))
    user_to = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user_from = db.Column(db.Integer, db.ForeignKey('Users.id'))
    body = db.Column(db.String(255), unique=False, nullable=False)
    msg_date = db.Column(db.DateTime(timezone=True), unique=False, nullable=True, default=datetime.datetime.utcnow())

    def __repr__(self):
        return '{},{},{},{},{}'.format(self.id, self.user_to, self.user_from, self.trade_id, self.body)


class TradesOffers(db.Model):
    __tablename__ = 'TradesOffers'
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), primary_key=True)
    trade_id = db.Column(db.Integer, db.ForeignKey('Trades.id'), primary_key=True)

    def __repr__(self):
        return '{},{}'.format(self.product_id, self.trade_id)


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))
