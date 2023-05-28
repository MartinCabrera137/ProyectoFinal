from flask import Blueprint, request, Flask, request, url_for, render_template, redirect, jsonify, make_response
from sqlalchemy import exc
from models import Usuario,Venta
from app import db, bcrypt
from auth import tokenCheck
from forms import FormVenta

appventa = Blueprint('appventa',__name__,template_folder="templates")

@appventa.route('/agregarventa', methods=['POST','GET'])
@tokenCheck
def registroven(usuario):
    mensaje = "Registro de Venta"
    ven = FormVenta()
    if request.method == "POST":
        if ven.validate_on_submit():
            venta = {"fecha":ven.fecha.data, "total":ven.total.data}
            userExist = Venta.query.filter_by(fecha=venta['fecha']).first()
            if not userExist:
                agregar = Venta(fecha=venta['fecha'], total=venta['total'])
                try:
                    db.session.add(agregar)
                    db.session.commit()
                    mensaje = "Venta del dia agregada"
                    
                except exc.SQLAlchemyError as e:
                    mensaje = print(e)
            else:
                mensaje="La venta del dia ya fue registrada"
            return render_template('Venta/agregarventa.html', forma=ven, mensaje=mensaje)
    return render_template('Venta/agregarventa.html', forma=ven, mensaje=mensaje)

@appventa.route('/venta', methods=["GET"])
@tokenCheck
def getVenta(usuario):
    if usuario['admin']:
        output=[]
        ventas = Venta.query.all()
        return render_template('Venta/venta.html', ventas=ventas)
    else:
        return render_template('admin.html')


@appventa.route('/ventas/editar/<int:idVenta>', methods=['GET', 'POST'])
@tokenCheck
def editarVenta(usuario, idVenta):
    mensaje = "Editar proveedor"
    if usuario['admin']:
        proveedor = Venta.query.get_or_404(idVenta)
        pro = FormVenta(obj=proveedor)
        if request.method == "POST":
            if pro.validate_on_submit():
                pro.populate_obj(proveedor)
                db.session.commit()
                return redirect(url_for('appventa.getVenta'))
        return render_template('Venta/editarventa.html', forma=pro,mensaje=mensaje)
    else:
        return render_template('admin.html')

@appventa.route('/ventas/eliminar/<int:idVenta>', methods=['GET', 'POST'])
@tokenCheck
def eliminarproveedor(usuario, idVenta):
    if usuario['admin']:
        pro = Venta.query.get_or_404(idVenta)
        db.session.delete(pro)
        db.session.commit()
        return redirect(url_for('appventa.getVenta'))
    return render_template('admin.html')