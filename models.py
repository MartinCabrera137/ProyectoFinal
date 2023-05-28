import jwt
import datetime
from config import BaseConfig
from app import db, bcrypt

class Usuario(db.Model):
        __tablename__="usuarios"
        idUsuario = db.Column(db.Integer,primary_key=True,autoincrement=True)
        nombreUsuario = db.Column(db.String(250))
        correo = db.Column(db.String(250),unique=True,nullable=False)
        contraseña = db.Column(db.String(250),nullable=False)
        edad = db.Column(db.Integer)
        registered_on = db.Column(db.DateTime, nullable=False)
        admin = db.Column(db.Boolean, nullable=False, default=False)
        
        def __init__(self, nombreUsuario=None,correo=None, contraseña=None, edad=None,admin=None) -> None:
                
                self.nombreUsuario = nombreUsuario
                self.correo = correo
                self.contraseña = bcrypt.generate_password_hash(
                        contraseña,BaseConfig.BCRYPT_LOG_ROUNDS
                ).decode()
                self.edad=edad
                self.registered_on = datetime.datetime.now()
                self.admin = admin
        
        def encode_auth_token(self, user_id):
                try:
                        payload = {
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                                'iat': datetime.datetime.utcnow(),
                                'sub': user_id
                        }
                        return jwt.encode(payload,BaseConfig.SECRET_KEY,algorithm='HS256')
                except Exception as e:
                        return e

        @staticmethod
        def decode_auth_token(auth_token):
                try:
                        payload = jwt.decode(auth_token, BaseConfig.SECRET_KEY,algorithms=['HS256'])
                        return payload['sub']
                except jwt.ExpiredSignatureError as e:
                        print(e)
                        return 'Signature expired. Please log in again.'
                except jwt.InvalidTokenError as e:
                        print(e)
                        return 'Invalid token. Please log in again.'


class Venta(db.Model):
    __tablename__="ventas"
    idVenta = db.Column(db.Integer,primary_key=True,autoincrement=True)
    fecha = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Integer)

    def __init__(self,fecha,total) -> None:
          self.fecha = fecha
          self.total = total

class Proveedor(db.Model):
    __tablename__="proveedor"
    idProveedor = db.Column(db.Integer,primary_key=True,autoincrement=True)
    nombreProveedor = db.Column(db.String(250))
    direccion = db.Column(db.String(250))

    def __init__(self,nombreProveedor,direccion) -> None:
          self.nombreProveedor = nombreProveedor
          self.direccion = direccion

class Producto(db.Model):
    __tablename__="producto"
    idProducto = db.Column(db.Integer,primary_key=True,autoincrement=True)
    nombreProducto = db.Column(db.String(250))
    desProducto = db.Column(db.Text)

    def __init__(self,nombreProducto,desProducto) -> None:
          self.nombreProducto = nombreProducto
          self.desProducto = desProducto

class Imagen_Producto(db.Model):
    __tablename__ = "imagen_producto"
    id_imagen = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    renderate_date = db.Column(db.Text, nullable=False)
    idProducto = db.Column(db.Integer, db.ForeignKey('producto.idProducto'),nullable = False)
    relacion_producto = db.relationship('Producto', backref="producto")