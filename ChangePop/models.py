import datetime

from app import db
from app import login
from flask_login import UserMixin
from sqlalchemy import func


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
    time_token = db.Column(db.DateTime)
    ts_create = db.Column(db.DateTime)
    ts_edit = db.Column(db.DateTime)

    def set_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)

# esto es si no le dices nada, muestra esto de salida al hacer una consulta a esta clase
    def __repr__(self):
        return '{}, {}, {}, {}'.format(self.id, self.nick, self.email, self.first_name)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True, nullable=False)
    tittle = db.Column(db.String(255), unique=False, index=True, nullable=False)
    descript = db.Column(db.String(255), unique=False, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    publish_date = db.Column(db.Date, unique=False, nullable=False)
    ban_reason = db.Column(db.String(255), unique=False, nullable=False)
    bid_dat = db.Column(db.Date, unique=False, nullable=True)
    num_visits = db.Column(db.Integer, unique=False, nullable=False)
    boost_date
    followers
    is_removed
    place
    user_id
    ts_edit
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __repr__(self):
        return '{},{},{}'.format(self.nia, self.carrera, self.privilegiado)


class Images(db.Model):
    products_id = db.Column(db.Integer, db.ForeignKey('Products.id'))
    image_url = db.Column(db.String(255), primary_key=True, index=True, nullable=False)

    def __repr__(self):
        return '{},{}'.format(self.products_id, self.image_url)

class Reto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(10000), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    pregunta = db.Column(db.String(500), nullable=False)
    activo = db.Column(db.Boolean, nullable=False)
    fecha_inicio = db.Column(db.DateTime, index=True, nullable=True)
    fecha_fin = db.Column(db.DateTime, index=True, nullable=True)

    def __repr__(self):
        return '{}, {}, {}, {}, {}'.format(self.titulo, self.descripcion, self.pregunta, self.fecha_inicio, self.fecha_fin)

    def activate(self):
        self.activo=True

    def desactivate(self):
        self.activo=False

    def calcularStats(reto_ident):
        aciertos = 0
        fallos = 0
        blanco = 0
        total = 0
        lista = Respuesta.obtenerrespuestas(reto_ident)
        for elemento in lista:
            resp = [elemento.respuesta1, elemento.respuesta2, elemento.respuesta3, elemento.respuesta4]
            i = 0
            while i < 4:
                total = total + 1
                if resp[i] == 0:
                    blanco = blanco+1
                elif resp[i] == 1:
                    aciertos = aciertos+1
                else:
                    fallos = fallos+1
                i = i+1
        if total == 0:
            aciertos = 0
            fallos = 0
            blanco = 0
        else:
            aciertos = int((aciertos * 100) / total)
            fallos = int((fallos * 100) / total)
            blanco = int((blanco * 100) / total)
        return [aciertos, fallos, blanco, total]



class Opciones(db.Model):
    reto_id = db.Column(db.Integer, db.ForeignKey('reto.id'), primary_key=True)
    cuerpo = db.Column(db.String(500), nullable=False, primary_key=True)
    verdadero = db.Column(db.Boolean, index=True, nullable=False)

    def __repr__(self):
        return '{}'.format(self.cuerpo)

class Responde(db.Model):
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    respuesta_id = db.Column(db.Integer, db.ForeignKey('respuesta.id'), primary_key=True)

    def __repr__(self):
        return '{}'.format(self.respuesta)

class Publica(db.Model):
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.email'), primary_key=True)
    reto_id = db.Column(db.Integer, db.ForeignKey('reto.id'), primary_key=True)
    ganador = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '{}'.format(self.ganador)

class Respuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reto_id = db.Column(db.Integer, db.ForeignKey('reto.id'))
    respuesta1 = db.Column(db.Integer)# No contestado=0, Acierto=1, Fallo=2
    respuesta2 = db.Column(db.Integer)
    respuesta3 = db.Column(db.Integer)
    respuesta4 = db.Column(db.Integer)
    def __repr__(self):
        return '{}''{}''{}''{}'.format(self.respuesta1, self.respuesta2, self.respuesta3, self.respuesta4)
        #return [str(self.respuesta1), str(self.respuesta2), str(self.respuesta3), str(self.respuesta4)]

    def obtenerrespuestas(iden):
        # SELECT cuerpo,verdadero FROM Opciones WHERE Opciones.reto_id=id
        return Respuesta.query.filter_by(reto_id=iden).all()

class Admin(db.Model):
    email = db.Column(db.String(120), primary_key=True, index=True, unique=True, nullable=False)
    activado= db.Column(db.Boolean)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def activate(self):
        self.activado=True

    def is_activated(self):
        return (self.activado==True)

    def __repr__(self):
        return '{},{}'.format(self.email,self.activado)

@login.user_loader
def load_user(id):
    return Usuario.query.get(int(id))




