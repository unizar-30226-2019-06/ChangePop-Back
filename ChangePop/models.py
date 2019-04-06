from sqlalchemy import func

from ChangePop import db
from ChangePop import login
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

# A ver, esto es un poco una locura, las funciones que tengan que ver con cada clase
# hay que ponerlas dentro de esa clase, es decir, la api, pero bueno, esto se va rellenando
# poco a poco
# dejo de ejemplo la del hash de la contraseña


class Categories(db.Model):
    cat_name = db.Column(db.String(255), primary_key=True, index=True, nullable=False)

    def __repr__(self):
        return '{}'.format(self.cat_name)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column(db.String(255), unique=False, nullable=False)
    nick = db.Column(db.String(255), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(255), unique=False, nullable=False)
    ban_reason = db.Column(db.String(255), unique=False, nullable=True)
    points = db.Column(db.Float, unique=False, nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    is_mod = db.Column(db.Boolean, unique=False, nullable=False)
    dni = db.Column(db.String(255), index=True, unique=True, nullable=False)
    avatar = db.Column(db.String(255), unique=False, nullable=False)
    fnac = db.Column(db.Date, unique=False, nullable=False)
    place = db.Column(db.String(255), unique=False, nullable=False)
    pass_hash = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255))
    time_token = db.Column(db.DateTime(timezone=True))
    ts_create = db.Column(db.DateTime(timezone=True), default=func.now())
    ts_edit = db.Column(db.DateTime(timezone=True), onupdate=func.now())

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

    def new_user(self, nick, last_name, first_name, phone, dni, place, pass_hash):
        u = Users(nick=nick, last_name=last_name, first_name=first_name, phone=phone,
                         dni=dni, place=place);
        u.set_password(pass_hash)
        db.session.add(u)
        db.session.commit()

# esto es si no le dices nada, muestra esto de salida al hacer una consulta a esta clase
    def __repr__(self):
        return '{}, {}, {}, {}'.format(self.id, self.nick, self.email, self.first_name)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True, nullable=False, autoincrement=True)
    tittle = db.Column(db.String(255), unique=False, index=True, nullable=False)
    descript = db.Column(db.String(255), unique=False, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    publish_date = db.Column(db.Date, unique=False, nullable=False, default=func.now())
    ban_reason = db.Column(db.String(255), unique=False, nullable=False)
    bid_dat = db.Column(db.Date, unique=False, nullable=True)
    num_visits = db.Column(db.Integer, unique=False, nullable=False)
    boost_date = db.Column(db.Date, unique=False, nullable=True)
    followers = db.Column(db.Integer, unique=False, nullable=False)
    is_removed = db.Column(db.Boolean, unique=False, nullable=False)
    place = db.Column(db.String(255), unique=False, nullable=False)
    ts_edit = db.Column(db.DateTime(timezone=True), unique=False, nullable=False, onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __repr__(self):
        return '{},{},{},{}'.format(self.id, self.tittle, self.user_id)


class Images(db.Model):
    products_id = db.Column(db.Integer, db.ForeignKey('Products.id'))
    image_url = db.Column(db.String(255), primary_key=True, index=True, nullable=False)

    def __repr__(self):
        return '{},{}'.format(self.products_id, self.image_url)


class Reports(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, index=True, nullable=False)
    reason = db.Column(db.String(255), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'))
    report_date = db.Column(db.DateTime(timezone=True), index=True, unique=False, nullable=True, default=func.now())

    def __repr__(self):
        return '{},{},{},{}'.format(self.id, self.reason, self.user_id, self.product_id)


class Payments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, index=True, nullable=False)
    pay_date = db.Column(db.DateTime(timezone=True), index=True, unique=False, nullable=False, default=func.now())
    amount = db.Column(db.Float, unique=False, nullable=False)
    iban = db.Column(db.String(255), unique=False, nullable=False)
    boost_date = db.Column(db.DateTime(timezone=True), unique=False, nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'))

    def __repr__(self):
        return '{},{},{}'.format(self.id, self.amount, self.product_id)


class Coments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, index=True, nullable=False)
    publish_date = db.Column(db.DateTime(timezone=True), index=True, unique=False, nullable=False, default=func.now())
    body = db.Column(db.String(255), unique=False, nullable=False)
    user_to = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user_from = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __repr__(self):
        return '{},{},{},{}'.format(self.id, self.body, self.user_to, self.user_from)


class CatProducts(db.Model):
    cat_name = db.Column(db.Integer, db.ForeignKey('Categories.cat_name'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), primary_key=True)

    def __repr__(self):
        return '{},{}'.format(self.cat_name, self.product_id)


class Interest(db.Model):
    cat_name = db.Column(db.Integer, db.ForeignKey('Categories.cat_name'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)

    def __repr__(self):
        return '{},{}'.format(self.cat_name, self.user_id)


class Follows(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)

    def __repr__(self):
        return '{},{}'.format(self.product_id, self.user_id)


class Bids(db.Model):
    bid = db.Column(db.Float, unique=False, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    ts_create = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return '{},{},{}'.format(self.product_id, self.user_id, self.bid)


class Trades(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, index=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'))
    user_sell = db.Column(db.Integer, db.ForeignKey('User.id'))
    user_buy = db.Column(db.Integer, db.ForeignKey('User.id'))
    closed = db.Column(db.Boolean, unique=False, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    ts_create = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return '{},{},{},{},{}'.format(self.id, self.user_sell, self.user_buy, self.product_id, self.price)


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, index=True, nullable=False)
    trade_id = db.Column(db.Integer, db.ForeignKey('Trades.id'))
    user_to = db.Column(db.Integer, db.ForeignKey('User.id'))
    user_from = db.Column(db.Integer, db.ForeignKey('User.id'))
    body = db.Column(db.String(255), unique=False, nullable=False)
    msg_date = db.Column(db.DateTime(timezone=True), unique=False, nullable=True, default=func.now())

    def __repr__(self):
        return '{},{},{},{},{}'.format(self.id, self.user_to, self.user_from, self.trade_id, self.body)


class TradesOffers(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), primary_key=True)
    trade_id = db.Column(db.Integer, db.ForeignKey('Trades.id'), primary_key=True)

    def __repr__(self):
        return '{},{}'.format(self.product_id, self.trade_id)


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))




