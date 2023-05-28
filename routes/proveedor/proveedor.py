from flask import Blueprint, request, Flask, request, url_for, render_template, redirect, jsonify, make_response
from sqlalchemy import exc
from models import Usuario,Proveedor
from app import db, bcrypt
from auth import tokenCheck
from forms import FormProveedor

appproveedor = Blueprint('appproveedor',__name__,template_folder="templates")

@appproveedor.route('/agregarproveedor', methods=['POST','GET'])
@tokenCheck
def registropro(usuario):
    mensaje = "Registro de proveedor"
    pro = FormProveedor()
    if request.method == "POST":
        if pro.validate_on_submit():
            proveedor = {"nombreProveedor":pro.nombreProveedor.data, "direccion":pro.direccion.data}
            userExist = Usuario.query.filter_by(correo=proveedor['nombreProveedor']).first()
            if not userExist:
                agregar = Proveedor(nombreProveedor=proveedor['nombreProveedor'], direccion=proveedor['direccion'])
                try:
                    db.session.add(agregar)
                    db.session.commit()
                    mensaje = "Proveedor agregado"
                except exc.SQLAlchemyError as e:
                    mensaje = print(e)
            else:
                mensaje="El proveedor ya existe"
            return render_template('proveedor/agregarproveedor.html', forma=pro, mensaje=mensaje)
    return render_template('proveedor/agregarproveedor.html', forma=pro, mensaje=mensaje)

@appproveedor.route('/proveedores', methods=["GET"])
@tokenCheck
def getProveedor(usuario):
    if usuario['admin']:
        output=[]
        proveedores = Proveedor.query.all()
        return render_template('proveedor/proveedor.html', proveedores=proveedores)
    else:
        return render_template('admin.html')


@appproveedor.route('/proveedores/editar/<int:idProveedor>', methods=['GET', 'POST'])
@tokenCheck
def editarProveedor(usuario, idProveedor):
    mensaje = "Editar proveedor"
    if usuario['admin']:
        proveedor = Proveedor.query.get_or_404(idProveedor)
        pro = FormProveedor(obj=proveedor)
        if request.method == "POST":
            if pro.validate_on_submit():
                pro.populate_obj(proveedor)
                db.session.commit()
                return redirect(url_for('appproveedor.getProveedor'))
        return render_template('Proveedor/editarproveedor.html', forma=pro,mensaje=mensaje)
    else:
        return render_template('admin.html')

@appproveedor.route('/proveedores/eliminar/<int:idProveedor>', methods=['GET', 'POST'])
@tokenCheck
def eliminarproveedor(usuario, idProveedor):
    if usuario['admin']:
        pro = Proveedor.query.get_or_404(idProveedor)
        db.session.delete(pro)
        db.session.commit()
        return redirect(url_for('appproveedor.getProveedor'))
    return render_template('admin.html')
