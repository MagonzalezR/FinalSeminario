from flask import Flask, render_template, request, redirect, session, g, flash
import utils as ut
import db as mod
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route("/")
def inde():
    return render_template("index.html")

@app.route("/registro", methods = ["GET", "POST"])
def registro():
    if request.method == "POST":
        username=request.form["user"]
        correo=request.form["email"]
        password=request.form["password"]
        error=None
        if not ut.isUsernameValid(username):
            error="El usuario es invalido"
            flash(error)
            render_template("/registro.html")

        if not ut.isEmailValid(correo):
            error="el correo no es valido"
            flash(error)
            render_template("/registro.html")

        if not ut.isPasswordValid(password):
            error="La contraseña debe tener por lo menos una minuscula, una mayuscula, un numero y 8 caracteres"
            flash(error)
            render_template("/registro.html")

        Result=mod.ingresar_usuario(username,correo,password)
        print(Result)
        if Result != "Creacion exitosa":
            flash(Result)
            return render_template("/registro.html")
        else:
            return redirect("/")

    return render_template("registro.html")

@app.route("/iniciar_sesion")
def iniciar_sesion():
    return render_template("inicioSesion.html")

@app.route("/detalle")
def detalles():
    return render_template("detalles.html")

@app.route("/carro")
def carro():
    return render_template("carro.html")

@app.route("/diseño")
def diseño():
    return render_template("diseño.html")

if __name__ == '__main__':
    app.run(debug=True)