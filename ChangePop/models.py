import datetime

from sqlalchemy import and_
from sqlalchemy.orm import aliased

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
        if c is None:
            c = Categories(cat_name=cat_name)
            db.session.add(c)
            db.session.commit()

    @staticmethod
    def list():
        # TODO doc and more
        list = Categories.query.all()
        return list

    def __repr__(self):
        return '{}'.format(self.cat_name)


class Users(UserMixin, db.Model):
    # TODO doc
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column(db.String(255), unique=False, nullable=False)
    nick = db.Column(db.String(255), unique=True, index=True, nullable=False)
    first_name = db.Column(db.String(255), unique=False, nullable=False)
    ban_reason = db.Column(db.String(255), unique=False, nullable=True)
    ban_until = db.Column(db.Date, unique=False, nullable=True)
    points = db.Column(db.Float, unique=False, nullable=False)
    point_times = db.Column(db.Integer, unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    mail = db.Column(db.String(255), unique=True, index=True, nullable=False)
    is_mod = db.Column(db.Boolean, unique=False, nullable=False)
    is_validated = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    dni = db.Column(db.String(255), unique=True, index=True, nullable=False)
    avatar = db.Column(db.String(255), unique=False, nullable=False)
    fnac = db.Column(db.Date, unique=False, nullable=False)
    place = db.Column(db.String(255), unique=False, nullable=False)
    pass_hash = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255))
    desc = db.Column(db.String, unique=False, nullable=True)
    time_token = db.Column(db.DateTime(timezone=True))
    ts_create = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow())
    ts_edit = db.Column(db.DateTime(timezone=True), unique=False, nullable=False, default=datetime.datetime.utcnow(),
                        onupdate=datetime.datetime.utcnow())

    products = db.relationship("Products", cascade="all, delete-orphan")
    trades_s = db.relationship("Trades", foreign_keys='[Trades.user_sell]', cascade="all, delete-orphan")
    trades_b = db.relationship("Trades", foreign_keys='[Trades.user_buy]', cascade="all, delete-orphan")
    follows = db.relationship("Follows", cascade="all, delete-orphan")
    interests = db.relationship("Interests", cascade="all, delete-orphan")
    comments_t = db.relationship("Comments", foreign_keys='[Comments.user_to]', cascade="all, delete-orphan")
    comments_f = db.relationship("Comments", foreign_keys='[Comments.user_from]', cascade="all, delete-orphan")
    bids = db.relationship("Bids", cascade="all, delete-orphan")
    messages_f = db.relationship("Messages", foreign_keys='[Messages.user_from]', cascade="all, delete-orphan")
    messages_t = db.relationship("Messages", foreign_keys='[Messages.user_to]', cascade="all, delete-orphan")
    reports = db.relationship("Reports", cascade="all, delete-orphan")
    notifications = db.relationship("Notifications", cascade="all, delete-orphan")

    def get_id(self):
        # TODO doc
        return self.id

    @staticmethod
    def get_nick(id):
        user = Users.query.get(id)
        return user.nick

    @staticmethod
    def new_user(nick, last_name, first_name, phone, dni, place, pass_hash, fnac, mail, token):
        # TODO doc
        u = Users(nick=nick,
                  last_name=last_name,
                  first_name=first_name,
                  phone=phone,
                  place=place,
                  dni=dni,
                  points=0,
                  point_times=0,
                  fnac=fnac,
                  is_mod=False,
                  mail=mail,
                  avatar="./static/images/logo.jpg",
                  is_validated=False,
                  token=token
                  )
        u.set_password(pass_hash)
        db.session.add(u)
        db.session.commit()
        db.session.flush()

        return u.id

    @staticmethod
    def list_users():
        # TODO doc and more
        list = Users.query.all()
        return list

    @staticmethod
    def search(nick):
        list = Users.query.filter(Users.nick.like('%' + nick + '%')).all()
        return list

    def my_follows(self):
        my_id = self.id

        products_list = db.session.query(Products.id,
                                         Products.title,
                                         Products.descript,
                                         Products.price,
                                         Products.main_img,
                                         Products.bid_date).join(Follows,
                                                                 Users).filter(my_id == Follows.user_id,
                                                                               Products.id == Follows.product_id)

        return products_list

    def point_me(self, new_points):
        self.point_times = self.point_times + 1
        self.points = float((self.points + new_points) / self.point_times)

        db.session.commit()

    def update_me(self, nick, first_name, last_name, phone, fnac, dni, place, mail, avatar, desc, is_mod=None,
                  ban_reason=None,
                  token=None, points=None, pass_hash=None):
        # TODO doc
        self.nick = nick
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.fnac = fnac
        self.dni = dni
        self.place = place
        self.mail = mail
        self.avatar = avatar
        self.desc = desc

        if is_mod is not None:
            self.is_mod = is_mod
        if ban_reason is not None:
            self.ban_reason = ban_reason
        if token is not None:
            self.token = token
        if points is not None:
            self.points = points
        if pass_hash is not None:
            self.pass_hash = pass_hash

        db.session.commit()

    def delete_me(self):
        # TODO doc
        db.session.delete(self)
        db.session.commit()

    def set_token(self, token):
        self.token = token
        db.session.commit()

    def validate_me(self):
        self.is_validated = True
        db.session.commit()

    def mod_me(self):
        # TODO doc
        self.is_mod = True
        db.session.commit()

    def ban_me(self, reason, until):
        # TODO doc
        self.ban_reason = str(reason)
        self.ban_until = until
        db.session.commit()

    def follow_prod(self, id):
        f = Follows(user_id=self.id, product_id=id)
        db.session.add(f)
        db.session.commit()

    def unfollow_prod(self, id):
        Follows.query.filter_by(user_id=self.id, product_id=id).delete()
        db.session.commit()

    def set_password(self, password):
        """ This funcion set a password to a user after encrypt it

            :param self: The user itself
            :param password: The password to be encrypted
            :type password: str.
            :returns:  str -- Hashed password

            """
        self.pass_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)

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
    bid_date = db.Column(db.DateTime, unique=False, nullable=True)
    visits = db.Column(db.Integer, unique=False, nullable=False)
    boost_date = db.Column(db.DateTime, unique=False, nullable=True)
    followers = db.Column(db.Integer, unique=False, nullable=False)
    is_removed = db.Column(db.Boolean, unique=False, nullable=False)
    main_img = db.Column(db.String(255), nullable=False)
    place = db.Column(db.String(255), unique=False, nullable=False)
    ts_edit = db.Column(db.DateTime(timezone=True), unique=False, nullable=False, default=datetime.datetime.utcnow(),
                        onupdate=datetime.datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    offers = db.relationship("TradesOffers", cascade="all, delete-orphan")
    trades = db.relationship("Trades", cascade="all, delete-orphan")
    cats = db.relationship("CatProducts", cascade="all, delete-orphan")
    bids = db.relationship("Bids", cascade="all, delete-orphan")
    payments = db.relationship("Payments", cascade="all, delete-orphan")
    images = db.relationship("Images", cascade="all, delete-orphan")
    follows = db.relationship("Follows", cascade="all, delete-orphan")
    reports = db.relationship("Reports", cascade="all, delete-orphan")
    notifications = db.relationship("Notifications", cascade="all, delete-orphan")

    @staticmethod
    def list():
        # TODO doc
        list = Products.query.all()
        return list

    @staticmethod
    def list_by_id(id):
        # TODO doc
        list = Products.query.filter_by(user_id=id)
        return list

    @staticmethod
    def get_title(id):
        # TODO doc
        prod = Products.query.get(id)
        return prod.title

    @staticmethod
    def search(title):
        list = Products.query.filter(Products.title.like('%' + title + '%')).all()
        return list

    @staticmethod
    def search_adv(title, price_min, price_max, place, desc, category):
        list = db.session.query(Products.id.label('id'),
                                Products.title.label('title'),
                                Products.price.label('price'),
                                Products.descript.label('descript'),
                                Products.user_id.label('user_id'),
                                Products.visits.label('visits'),
                                Products.place.label('place'), CatProducts.cat_name).filter(CatProducts.product_id == Products.id)

        if price_min is not None:
            list = list.filter(Products.price >= price_min)
        if price_max is not None:
            list = list.filter(Products.price <= price_max)
        if title is not None:
            list = list.filter(Products.title.like('%' + title + '%'))
        if desc is not None:
            list = list.filter(Products.descript.like('%' + desc + '%'))
        if place is not None:
            list = list.filter(Products.place.like('%' + place + '%'))
        if category is not None:
            list = list.filter(CatProducts.cat_name == category)

        list = list.distinct(Products.id).all()

        return list

    @staticmethod
    def new_product(user_id, title, descript, price, place, main_img):
        p = Products(user_id=user_id,
                     title=title,
                     descript=descript,
                     price=price,
                     place=place,
                     visits=0,
                     followers=0,
                     is_removed=False,
                     main_img=main_img
                     )
        db.session.add(p)
        db.session.commit()
        db.session.flush()

        return p.id

    def update_me(self, title, price, descript, bid, place, main_img):
        # TODO doc
        self.title = title
        self.price = price
        self.descript = descript
        self.main_img = main_img
        self.place = place
        self.bid_date = bid

        db.session.commit()

    def delete_me(self):
        # TODO doc
        db.session.delete(self)
        db.session.commit()

    def ban_me(self, reason):
        # TODO doc
        self.ban_reason = str(reason)
        db.session.commit()

    def bid_set(self, bid):
        # TODO doc
        self.bid_date = bid
        db.session.commit()

    def increment_views(self):
        self.visits = self.visits + 1

    def __repr__(self):
        return '{},{},{},{},{}'.format(self.id, self.title, self.user_id, self.visits, self.user_id)


class Images(db.Model):
    __tablename__ = 'Images'
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'))
    image_url = db.Column(db.String(255), primary_key=True, index=True, nullable=False)

    @staticmethod
    def delete_images_by_prod(product_id):
        Images.query.filter_by(product_id=product_id).delete()

    @staticmethod
    def get_images_by_prod(product_id):
        cats = Images.query.with_entities(Images.image_url).filter_by(product_id=product_id)
        return cats

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

    @staticmethod
    def new_report(user_id, product_id, reason):
        r = Reports(user_id=user_id, product_id=product_id, reason=reason)
        db.session.add(r)
        db.session.commit()
        db.session.flush()

        return r.id

    @staticmethod
    def list():
        # TODO doc
        list = Reports.query.all()
        return list

    def delete_me(self):
        # TODO doc
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def delete_by_id(report_id):
        Reports.query.get(report_id).delete_me()

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

    @staticmethod
    def list():
        # TODO doc
        list = Payments.query.all()
        return list

    def delete_me(self):
        # TODO doc
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def add(amount, iban, product_id, boost_date):
        pays = Payments(product_id=product_id,
                        amount=amount,
                        iban=iban,
                        boost_date=boost_date)

        db.session.add(pays)
        db.session.commit()
        db.session.flush()

        return pays.id


class Comments(db.Model):
    __tablename__ = 'Coments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, index=True, nullable=False)
    publish_date = db.Column(db.DateTime(timezone=True), index=True, unique=False, nullable=False,
                             default=datetime.datetime.utcnow())
    body = db.Column(db.String(255), unique=False, nullable=False)
    user_to = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user_from = db.Column(db.Integer, db.ForeignKey('Users.id'))

    @staticmethod
    def add_comment(user_to, user_from, body):
        c = Comments(user_to=user_to, user_from=user_from, body=body)

        db.session.add(c)
        db.session.commit()

    @staticmethod
    def list_by_user(id):
        # TODO doc
        list = Comments.query.filter_by(user_to=id)
        return list

    def __repr__(self):
        return '{},{},{},{}'.format(self.id, self.body, self.user_to, self.user_from)


class CatProducts(db.Model):
    __tablename__ = 'CatProducts'
    cat_name = db.Column(db.String, db.ForeignKey('Categories.cat_name'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), primary_key=True)

    @staticmethod
    def delete_cats_by_prod(product_id):
        CatProducts.query.filter_by(product_id=product_id).delete()

    @staticmethod
    def get_cat_names_by_prod(product_id):
        cats = CatProducts.query.with_entities(CatProducts.cat_name).filter_by(product_id=product_id)
        return cats

    @staticmethod
    def add_prod(cat_name, product_id):
        cp = CatProducts(cat_name=cat_name, product_id=product_id)
        db.session.add(cp)
        db.session.commit()

    def __repr__(self):
        return '{},{}'.format(self.cat_name, self.product_id)


class Interests(db.Model):
    __tablename__ = 'Interest'
    cat_name = db.Column(db.String, db.ForeignKey('Categories.cat_name'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)

    def __repr__(self):
        return '{},{}'.format(self.cat_name, self.user_id)

    @staticmethod
    def add_interest(cat_name, user_id):
        c = Interests.query.get(cat_name, user_id)
        if c is None:
            c = Interests(cat_name=cat_name, user_id=user_id)
            db.session.add(c)
            db.session.commit()

    @staticmethod
    def interest_byUser(id):
        list = Interests.query.filter_by(user_id=id)
        return list

    @staticmethod
    def delete_all(user_id):
        Interests.query.filter_by(user_id=user_id).delete()

    @staticmethod
    def delete_interest(cat, user_id):
        Interests.query.filter_by(user_id=user_id, cat_name=cat).delete()


class Follows(db.Model):
    __tablename__ = 'Follows'
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)

    @staticmethod
    def get_users_follow_prod(product_id):
        list = Follows.query.with_entities(Follows.user_id).filter_by(product_id=product_id)
        return list

    def __repr__(self):
        return '{},{}'.format(self.product_id, self.user_id)


class Bids(db.Model):
    __tablename__ = 'Bids'
    bid = db.Column(db.Float, unique=False, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True)
    ts_create = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow())

    @staticmethod
    def get_max(product_id):
        return db.session.query(Bids.bid, Bids.user_id, ).filter(Bids.product_id == product_id).order_by(
            db.desc(Bids.bid)).first()

    @staticmethod
    def add_bid(product_id, user_id, money):
        b = Bids(bid=float(money), product_id=product_id, user_id=user_id)
        db.session.add(b)
        db.session.commit()

    def __repr__(self):
        return '{},{},{}'.format(self.product_id, self.user_id, self.bid)


class Trades(db.Model):
    __tablename__ = 'Trades'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, index=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    user_sell = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    user_buy = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    closed_s = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    closed_b = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    ts_create = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow())
    ts_edit = db.Column(db.DateTime(timezone=True), unique=False, nullable=False, default=datetime.datetime.utcnow(),
                        onupdate=datetime.datetime.utcnow())

    offers = db.relationship("TradesOffers", cascade="all, delete-orphan")
    messages = db.relationship("Messages", cascade="all, delete-orphan")

    @staticmethod
    def add(product_id, seller_id, buyer_id):
        p = Products.query.get(product_id)

        t = Trades(product_id=product_id,
                   user_sell=seller_id,
                   user_buy=buyer_id,
                   price=p.price,
                   closed_b=False,
                   closed_s=False)

        db.session.add(t)
        db.session.commit()
        db.session.flush()

        return t.id

    @staticmethod
    def get_trades(user_id):
        items = Trades.query.filter((Trades.user_sell == str(user_id)) | (Trades.user_buy == str(user_id)))
        return items

    def set_price(self, price):
        self.price = price

        db.session.commit()

    def switch(self, who):
        if who == 's':
            self.closed_s = not self.closed_s
        elif who == 'b':
            self.closed_b = not self.closed_b

        db.session.commit()

    def __repr__(self):
        return '{},{},{},{},{}'.format(self.id, self.user_sell, self.user_buy, self.product_id, self.price)


class Messages(db.Model):
    __tablename__ = 'Messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, index=True, nullable=False)
    trade_id = db.Column(db.Integer, db.ForeignKey('Trades.id'), nullable=False)
    user_to = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    user_from = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    body = db.Column(db.String(255), unique=False, nullable=False)
    msg_date = db.Column(db.DateTime(timezone=True), unique=False, nullable=True, default=datetime.datetime.utcnow())

    @staticmethod
    def new_msg(trade_id, user_to, user_from, body):
        m = Messages(trade_id=trade_id, user_to=user_to, user_from=user_from, body=body)

        db.session.add(m)
        db.session.commit()

    @staticmethod
    def get_msgs(trade_id):
        items = Messages.query.filter((Messages.trade_id == str(trade_id)))
        return items

    def __repr__(self):
        return '{},{},{},{},{}'.format(self.id, self.user_to, self.user_from, self.trade_id, self.body)


class TradesOffers(db.Model):
    __tablename__ = 'TradesOffers'
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), primary_key=True)
    trade_id = db.Column(db.Integer, db.ForeignKey('Trades.id'), primary_key=True)

    @staticmethod
    def add_product(trade_id, product_id):
        to = TradesOffers(product_id=product_id, trade_id=trade_id)

        db.session.add(to)
        db.session.commit()

    @staticmethod
    def delete_all(trade_id):
        TradesOffers.query.filter_by(trade_id=trade_id).delete()

    @staticmethod
    def get_prods_by_id(trade_id):
        items = TradesOffers.query.with_entities(TradesOffers.product_id).filter_by(trade_id=trade_id)
        return items

    def __repr__(self):
        return '{},{}'.format(self.product_id, self.trade_id)


class Notifications(db.Model):
    __tablename__ = 'Notifications'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'))
    category = db.Column(db.String(255), db.ForeignKey('Categories.cat_name'))
    date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow())
    text = db.Column(db.String(255), unique=False, nullable=False)

    @staticmethod
    def push(user, text, product=None, category=None):
        n = Notifications(user_id=user, product_id=product, category=category, text=text)

        db.session.add(n)
        db.session.commit()

    @staticmethod
    def delete_id(id):
        Notifications.query.filter_by(id=id).delete()
        db.session.commit()

    @staticmethod
    def delete_all(user):
        Notifications.query.filter_by(user_id=user).delete()
        db.session.commit()

    @staticmethod
    def list_by_user(user_id):
        items = Notifications.query.filter_by(user_id=user_id)
        return items

    def __repr__(self):
        return '{},{},{},{},{},{}'.format(self.id, self.user_id, self.product_id, self.category, self.date, self.text)


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))
