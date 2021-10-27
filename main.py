from flask import Flask, render_template, flash, session
import sqlite3
import os
import hashlib
from flask.helpers import flash
from werkzeug.utils import redirect, escape

from wtforms.compat import with_metaclass

from formularios.formulario import Login, Registro, Productos

app=Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET", "POST"])
def home():
    frmLogin = Login()
    if frmLogin.validate_on_submit():
        usuario = escape(frmLogin.usuario.data)
        contraseña = escape(frmLogin.contraseña.data)
        #ciframos la contraseña para compararla
        enc = hashlib.sha256(contraseña.encode())
        pass_enc = enc.hexdigest()
        with sqlite3.connect("vacunacion.db") as con:
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            cursor.execute("SELECT username, perfil FROM usuario WHERE username = ? AND contraseña = ?", [usuario, pass_enc])
            row = cursor.fetchone()
            if row:
                session["usuario"] = usuario
                session["perfil"] = row["perfil"]
                if session["perfil"] == 1:
                    return redirect("/administrador/dashboard")
                elif session["perfil"] == 2:
                    return redirect("/vendedor/dashboard")
            else:
                return "usuario/contraseña errados"
    return render_template("login.html", frm = frmLogin)

@app.route("/vendedor/dashboard")
def vendedorDashBoard():
    return render_template("dashboard.html")

@app.route("/administrador/dashboard")
def adminDashBoard():
    return render_template("dashboard.html")

#Api Rest de registro de usuario
@app.route("/registrarse", methods=["GET", "POST"]) #Ruta
def registrar(): #Endpoint
    frmRegistro = Registro()
    if "usuario" in session and session["perfil"] == 1:       
        #Valida los datos del formulario
        if frmRegistro.validate_on_submit():
            #captura los datos
            usuario = frmRegistro.usuario.data
            nombre = frmRegistro.nombre.data
            correo = frmRegistro.correo.data
            contraseña = frmRegistro.contraseña.data
            #ciframos la contraseña
            enc = hashlib.sha256(contraseña.encode())
            pass_enc = enc.hexdigest()
            with sqlite3.connect("vacunacion.db") as con:
                # creamos el cursor para manipular la base de datos
                cursor = con.cursor()
                #Prepara la sentencia sql a ejecutar
                cursor.execute("INSERT INTO usuario (nombre, username, correo, contraseña) VALUES (?,?,?,?)", [nombre, usuario, correo, pass_enc])
                #Ejecuta la sentencia sql
                con.commit()
                return "Guardado con exito"
        return render_template("registro.html", frmRegistro = frmRegistro) #Respuesta
    else:
        return "Acceso no permitido"

@app.route("/usuarios/listar")
def listarUsuarios():
    #Nos conectamos a la base de datos
    with sqlite3.connect("vacunacion.db") as con:
        #Convierte la respuesta de la consulta en un diccionario
        con.row_factory = sqlite3.Row
        # creamos el cursor para manipular la base de datos
        cursor = con.cursor()
        #Prepara la sentencia sql a ejecutar
        cursor.execute("SELECT * FROM usuario")
        rows = cursor.fetchall()
        return render_template("listaUsuarios.html", rows = rows)

@app.route("/productos", methods=["GET"])
def prod():
    if "usuario" in session and session["perfil"] == 2:
        frm = Productos()
        return render_template("productos.html", frm = frm)
    else:
        return redirect("/")

@app.route("/productos/save", methods=["POST"])
def guardarProducto():
    if "usuario" in session:
        frm = Productos()
        nombre = escape(frm.nombre.data)
        precio = escape(frm.precio.data)
        stock = escape(frm.stock.data)
        with sqlite3.connect("vacunacion.db") as con:
            cursor = con.cursor()
            cursor.execute("INSERT INTO producto (nombre, precio, stock) VALUES (?,?,?)", [nombre, precio, stock])
            con.commit()
            flash("Guardado con éxito")
        return render_template("productos.html", frm = frm)
    else:
        return redirect("/")

@app.route("/productos/get", methods=["POST"])
def consultarProducto():
    if "usuario" in session:
        frm = Productos()
        codigo = frm.codigo.data
        if len(codigo) > 0:
            with sqlite3.connect("vacunacion.db") as con:
                #Convierte la respuesta de la consulta en un diccionario
                con.row_factory = sqlite3.Row
                cursor = con.cursor()
                cursor.execute("SELECT * FROM producto WHERE codigo = ?", [codigo])
                row = cursor.fetchone()
                if row:
                    frm.nombre.data = row["nombre"]
                    frm.precio.data = row["precio"]
                    frm.stock.data = row["stock"]
                else:
                    frm.nombre.data = ""
                    frm.precio.data = ""
                    frm.stock.data = ""
                    flash("El producto no se ha encontrado")
        else:
            flash("Debe digitar el codigo del producto")
        return render_template("productos.html", frm = frm)
    else:
        return redirect("/")

@app.route("/productos/lista", methods=["GET"])
def listarProductos():
    if "usuario" in session and session["perfil"] == 2:
        frm = Productos()
        codigo = frm.codigo.data
        with sqlite3.connect("vacunacion.db") as con:
            #Convierte la respuesta de la consulta en un diccionario
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            cursor.execute("SELECT * FROM producto")
            rows = cursor.fetchall()
            return render_template("productolistado.html", rows = rows)
    else:
        return redirect("/")

@app.route("/productos/update", methods=["POST"])
def actualizarProducto():
    if "usuario" in session:
        frm = Productos()
        codigo = frm.codigo.data
        nombre = frm.nombre.data
        precio = frm.precio.data
        stock = frm.stock.data
        
        if len(codigo):
            if codigo.isnumeric:
                if len(nombre):
                    if len(precio):
                        if len(stock):
                            with sqlite3.connect("vacunacion.db") as con:
                                cursor = con.cursor()
                                cursor.execute("UPDATE producto SET nombre=?, precio=?, stock=? WHERE codigo=?", [nombre, precio, stock, codigo])
                                con.commit
                                flash("producto actualizado")
                        else:
                            flash("debe digitar el stock")
                    else:
                        flash("debe digitar el precio")
                else:
                    flash("debe digitar el nombre")
            else:
                flash("Codigo debe ser numerico")
        else:
            flash("debe digitar el codigo")
        return render_template("productos.html", frm = frm)
    else:
        return redirect("/")

@app.route("/productos/delete", methods=["POST"])
def eliminarProducto():
    if "usuario" in session:
        frm = Productos()
        codigo = frm.codigo.data
        if len(codigo) > 0:
            with sqlite3.connect("vacunacion.db") as con:
                cursor = con.cursor()
                cursor.execute("DELETE FROM producto WHERE codigo = ?", [codigo])
                con.commit()
                flash("El producto se ha eliminado")
        else:
            flash("Debe digitar el codigo del producto")
        return render_template("productos.html", frm = frm)
    else:
        return redirect("/")

@app.route("/logout")
def logoute():
    session.clear()
    return redirect("/")

app.run(debug=True, host='127.0.0.1', port=8080, ssl_context=('micertificado.pem', 'llaveprivada.pem') )