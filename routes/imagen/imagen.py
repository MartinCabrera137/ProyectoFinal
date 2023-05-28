from flask import Blueprint, request,Flask,url_for,render_template,redirect,jsonify
from sqlalchemy import exc
from models import Imagen_Producto, Producto
from app import db,bcrypt
from auth import tokenCheck
import base64
from forms import ImageForm
from app import session

imageProducto = Blueprint('imageProducto',__name__,template_folder="templates")


def render_image(data):
    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic

@imageProducto.route("/producto/imagen/<int:idProducto>", methods=["POST","GET"])
@tokenCheck
def upload(usuario,idProducto):
    if usuario['admin']:
        if 'registered_on' in usuario:
            pop=""
            mensaje="Ingresar imagen"
            imageForm = ImageForm()
            imageForm.type.data = "Foto"
            elegido = idProducto
            imageForm.idProducto.choices = [(producto.idProducto,producto.nombreProducto) for producto in Producto.query.filter_by(idProducto=elegido).all()]

            if request.method == "POST":
                if imageForm.validate_on_submit():
                    try:
                        elegido = imageForm.idProducto.data
                        searchImage = Imagen_Producto.query.filter_by(idProducto=elegido).first()
                        if searchImage:
                            file = imageForm.imagen.data
                            data = file.read()
                            render_file = render_image(data)
                            searchImage.data = data
                            searchImage.renderate_date = render_file
                            db.session.commit()
                            pop = "Imagen agregada correctamente"
                            return (render_template('Producto/añadirimagen.html',forma=imageForm,mensaje=mensaje,pop=pop))
                        else:
                            file = imageForm.imagen.data
                            data = file.read()
                            render_file = render_image(data)
                            newFile = Imagen_Producto()
                            newFile.type = imageForm.type.data
                            newFile.renderate_date = render_file
                            newFile.idProducto = imageForm.idProducto.data
                            newFile.data=data
                            db.session.add(newFile)
                            db.session.commit()
                            pop="Imagen agregada correctamente"
                            return (render_template('Producto/añadirimagen.html',forma=imageForm,mensaje=mensaje,pop=pop))
                    except exc.SQLAlchemyError as e:
                        print(e)
                        pop = f'Error: {e}'
                        return render_template ('Producto/añadirimagen.html',forma=imageForm,mensaje=mensaje,pop=pop)
            return render_template ('Producto/añadirimagen.html',forma=imageForm,mensaje=mensaje,pop=pop)
        else:
            return jsonify({"mensaje":"Sesion erronea"})
    else:
        return render_template('admin.html')