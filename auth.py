from models import Usuario
from functools import wraps
from flask import request,jsonify,redirect,url_for,render_template
from app import session

def obtenerInfo(token):
    if token:
        resp = Usuario.decode_auth_token(token)
        usuario = Usuario.query.filter_by(idUsuario=resp).first()
        if  usuario:
            usu = {
                    'status': 'success',
                    'data': {
                        'idUsuario': usuario.idUsuario,
                        'correo': usuario.correo,
                        'admin': usuario.admin,
                        'registered_on': usuario.registered_on
                    }
                }
            return usu
        else:
            error = {
                'status': 'fail',
                #'message': resp
            }
            return error


def tokenCheck(f):
    @wraps(f)
    def verificar(*args,**kwargs):
        token = None
        if 'token' in request.headers:
            token = request.headers['token']
        elif 'token' in session:
            token = session['token']
        if not token:
            return redirect(url_for('appusuario.login'))
        try:
            info = obtenerInfo(token)
            print(info)
            if info['status']=="Fallido":
                return redirect(url_for('appusuario.login'))
        except:
            return redirect(url_for('appusuario.login'))
        return f(info['data'],*args,**kwargs)
    return verificar