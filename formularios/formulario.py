from flask_wtf import FlaskForm
import flask_wtf
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class Login(FlaskForm):
    usuario = StringField("Usuario", validators=[DataRequired("Debe ingresar un usuario")])
    contraseña = PasswordField("Contraseña", validators=[DataRequired("Debe ingresar una contraseña")])
    enviar = SubmitField("Enviar")
    

class Mensaje(FlaskForm):
    remitente = StringField("Id de quien remite")
    para = StringField("Id de para quien es el mensaje")
    asunto = StringField("asunto del mensaje")
    mensaje = StringField("Mensaje")

class Registro(FlaskForm):
    usuario = StringField("Usuario")
    nombre = StringField("Nombre")
    correo = StringField("Correo",)
    contraseña = PasswordField("Contraseña")
    registrar = SubmitField("Registrar")
    
class Productos(FlaskForm):
    codigo = StringField("Código")
    nombre = StringField("Nombre")
    precio = StringField("Precio")
    stock = StringField("Stock")
    guardar = SubmitField("Guardar", render_kw=({"onfocus":"cambiaRuta('productos/save')"}))
    consultar = SubmitField("Consultar", render_kw=({"onfocus":"cambiaRuta('productos/get')"}) )
    eliminar = SubmitField("Eliminar", render_kw=({"onfocus":"cambiaRuta('productos/delete')"}))
    editar = SubmitField("Editar", render_kw=({"onfocus":"cambiaRuta('productos/update')"}))
