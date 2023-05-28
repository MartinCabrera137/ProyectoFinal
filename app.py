from flask import Flask,request,jsonify,render_template,redirect,session,url_for
from flask_cors import CORS
from database import db
from encriptador import bcrypt
from flask_migrate import Migrate
from config import BaseConfig
from sqlalchemy import exc
from models import Usuario,Venta,Proveedor,Producto,Imagen_Producto
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import date
from flask_session import Session
from flask_bootstrap import Bootstrap
from routes.usuario.usuario import appusuario
from routes.imagen.imagen import imageProducto
from routes.producto.producto import appproducto
from routes.proveedor.proveedor import appproveedor
from routes.venta.venta import appventa


app = Flask(__name__)
app.secret_key = "SK1234"
app.register_blueprint(appusuario)
app.register_blueprint(imageProducto)
app.register_blueprint(appproducto)
app.register_blueprint(appproveedor)
app.register_blueprint(appventa)
app.config.from_object(BaseConfig)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
CORS(app)
Session(app)
bootstrap = Bootstrap(app)
bcrypt.init_app(app)
db.init_app(app)
migrate = Migrate()
migrate.init_app(app,db)

admin = Admin(app)
admin.add_view(ModelView(Usuario,db.session))
admin.add_view(ModelView(Venta,db.session))
admin.add_view(ModelView(Producto,db.session))
admin.add_view(ModelView(Proveedor,db.session))


@app.route('/')
@app.route('/inicio')
@app.route('/index')
def inicio():
    return render_template('index.html')



@app.route('/auth/registro',methods=['POST'])
def registro():
    user= request.get_json()
    userExist=Usuario.query.filter_by(correo=user['correo']).first()
    if not userExist:
        usuario=Usuario(nombreUsuario=user["nombreUsuario"],correo=user["correo"],contraseña=user["contraseña"],edad=user["edad"],admin=user["admin"])
        try:
            db.session.add(usuario)
            db.session.commit()
            mensaje="Usuario creado"
        except exc.SQLAlchemyError as e:
            mensaje="Error"
    else:
        mensaje="El usuario ya existe"
    return jsonify({"mensaje":mensaje})

@app.errorhandler(404)
def paginaEncontrada(error):
  return render_template('404.html',error=error),404

@app.errorhandler(500)
def paginaNoEncontrada(error):
  return render_template('500.html',error=error) ,500