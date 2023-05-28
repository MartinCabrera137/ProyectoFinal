from flask import Blueprint, request, Flask, request, url_for, render_template, redirect, jsonify, make_response
from sqlalchemy import exc
from models import Usuario
from app import session, db, bcrypt
from auth import tokenCheck
from forms import FormLogin,FormRegistro,FormObtenerUsuario

appusuario = Blueprint('appusuario',__name__,template_folder="templates")

@appusuario.route('/login',methods={'POST','GET'})
def login():
    mensaje = "Iniciar Sesion"
    pop = ""
    Login = FormLogin()
    if request.method == "POST":
        if Login.validate_on_submit():
            log = {"correo": Login.correo.data,"contraseña": Login.contraseña.data}
            usuario = Usuario(correo=log['correo'], contraseña=log["contraseña"])
            BusquedaCo = Usuario.query.filter_by(correo=usuario.correo).first()
            if BusquedaCo:
                validar = bcrypt.check_password_hash(BusquedaCo.contraseña,log["contraseña"])
                if validar:
                    auth_token = usuario.encode_auth_token(user_id=BusquedaCo.idUsuario)
                    
                    responseObj = {
                        "status": "exitoso",
                        "mensaje": "Login",
                        "auth_token": auth_token
                    }
                    print(responseObj)
                    session['token'] = auth_token
                    print("Entro aqui")
                    return render_template('index.html')
                pop = "Contraseña incorrecta. Por favor intentelo de nuevo"
                return render_template('login.html', forma=Login, mensaje=mensaje, pop=pop)
            pop = "Usuario Inexistente. Por favor verifique los datos ingresados sean los correctos"
    return render_template('login.html', forma=Login, mensaje=mensaje, pop=pop)

@appusuario.route('/registro', methods={'POST','GET'})
def registro():
    mensaje = "Registro de Nuevo Usuario"
    Registro = FormRegistro()
    if request.method == "POST":
        if Registro.validate_on_submit():
            user = {"nombreUsuario":Registro.nombreUsuario.data,"correo": Registro.correo.data,"contraseña": Registro.contraseña.data,"edad":Registro.edad.data,"admin":0} #PARA ADMIN
            userExist = Usuario.query.filter_by(correo=user['correo']).first()
            if not userExist:
                usuario = Usuario(nombreUsuario=user['nombreUsuario'], correo=user['correo'], contraseña=user["contraseña"], edad=user["edad"], admin=user["admin"])
                try:
                    db.session.add(usuario)
                    db.session.commit()
                    mensaje = "Usuario Registrado"
                    return render_template('index.html')
                except exc.SQLAlchemyError as e:
                    mensaje = print(e)
            else:
                mensaje="El usuario ya existe"
            return render_template('registro.html', forma=Registro, mensaje=mensaje)
    return render_template('registro.html', forma=Registro, mensaje=mensaje)


@appusuario.route('/usuario', methods=["GET"])
@tokenCheck
def getUsuarios(usuario):
    mensaje =  "Lista de todos los usuarios registrados"
    if usuario['admin']:
            output=[]
            usuarios = Usuario.query.all()
            return render_template('usuario/usuario.html', usuarios = usuarios, mensaje=mensaje)
    else:
        return render_template('admin.html')

@appusuario.route('/usuario/editar/<int:idUsuario>', methods=['GET', 'POST'])
@tokenCheck
def editarUsuario(usuario, idUsuario):
    mensaje = "Editar usuario"
    if usuario['admin']:
        usuario = Usuario.query.get_or_404(idUsuario)
        Consultar = FormObtenerUsuario(obj=usuario)
        if request.method == "POST":
            if Consultar.validate_on_submit():
                Consultar.populate_obj(usuario)
                db.session.commit()
                return redirect(url_for('appusuario.getUsuarios'))
        return render_template('usuario/editarusuario.html', forma=Consultar,mensaje=mensaje)
    else:
        return render_template('admin.html')


@appusuario.route('/usuario/eliminar/<int:idUsuario>', methods=['GET', 'POST'])
@tokenCheck
def eliminar(usuario, idUsuario):
    if usuario['admin']:
        usuario = Usuario.query.get_or_404(idUsuario)
        db.session.delete(usuario)
        db.session.commit()
        return redirect(url_for('appusuario.getUsuarios'))
    return render_template('admin.html')