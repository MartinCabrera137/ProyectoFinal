from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField,IntegerField,DateField,FileField,SelectField,PasswordField
from wtforms.validators import DataRequired
from flask import Flask, render_template, redirect, url_for

class FormLogin(FlaskForm):
    correo = StringField('Correo:', validators=[DataRequired()])
    contraseña = PasswordField('Contraseña:', validators=[DataRequired()])
    enviar = SubmitField('Enviar')

class FormRegistro(FlaskForm):
    nombreUsuario = StringField('Nombre del usuario:', validators=[DataRequired()])
    correo = StringField('Correo:', validators=[DataRequired()])
    contraseña = StringField('Contraseña:', validators=[DataRequired()])
    edad = IntegerField('Edad:', validators=[DataRequired()])
    enviar = SubmitField('Enviar')

class FormProveedor(FlaskForm):
    nombreProveedor = StringField('Nombre del Proveedor:', validators=[DataRequired()])
    direccion = StringField('Direccion:', validators=[DataRequired()])
    enviar = SubmitField('Enviar')


class FormProducto(FlaskForm):
    nombreProducto = StringField('Perfume:', validators=[DataRequired()])
    desProducto = StringField('Descripcion:', validators=[DataRequired()])
    enviar = SubmitField('Enviar')

class FormVenta(FlaskForm):
    fecha = DateField('Fecha:', validators=[DataRequired()])
    total = IntegerField('Total:', validators=[DataRequired()])
    enviar = SubmitField('Enviar')

        
class FormObtenerUsuario(FlaskForm):
    nombreUsuario = StringField('Nombre del Usuario:', validators=[DataRequired()])
    correo = StringField('Correo:', validators=[DataRequired()])
    contraseña = StringField('Contraseña:', validators=[DataRequired()])
    edad = IntegerField('Edad:', validators=[DataRequired()])
    admin = BooleanField('Admin')
    enviar = SubmitField('Enviar')


class ImageForm(FlaskForm):
    type = StringField('Nombre:', validators=[DataRequired()])
    imagen = FileField('Imagen:', validators=[DataRequired()])
    idProducto = SelectField('Perfume:',choices=[],coerce=int,validators=[DataRequired()])
    enviar = SubmitField('Enviar')