from flask import Flask, render_template, request, redirect, session, g
import utils as ut
import db as mod
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route("/")
def index():
    print(g.user)
    if g.user !=None:

        camisas = mod.get_camisas()
        return render_template("loged.html", imagenes=camisas)
    return render_template("index.html")

@app.route("/registro", methods = ["GET", "POST"])
def registro():
    try:
        if request.method == "POST":
            username=request.form["user"]
            correo=request.form["email"]
            password=request.form["password"]
            error=None
            if not ut.isEmailValid(correo):
                error=["el correo no es valido"]
                return render_template("registro.html", errores =error)

            if not ut.isPasswordValid(password):
                error=["La contraseña debe tener por lo menos una minuscula, una mayuscula, un numero y 8 caracteres"]
                return render_template("registro.html", errores =error)

            Result=mod.ingresar_usuario(username,correo,password)
            print(Result)
            if Result != "Creacion exitosa":
                return render_template("registro.html")
            else:
                return redirect("/")
        return render_template("registro.html")
    except:
        error=["Algo salió mal"]
        return render_template("registro.html", errores =error)

@app.route("/iniciar_sesion", methods = ["GET", "POST"])
def iniciar_sesion():
    try:
        if request.method=="POST":
            correo=request.form["email"]
            password=request.form["password"]
            user = mod.comprobar_usuario(correo,password)
            if user!=[]:
                mod.creaCarrito(user[0])
                session['id_usuario']=user[0]
                print(session.get('id_usuario'))
                return redirect("/")
            else:
                err=["correo o contraseña incorrectos, intentelo de nuevo"]
                print(err)
                return render_template("inicioSesion.html", errores=err)

        return render_template("inicioSesion.html")
    except:   
        err=["correo o contraseña incorrectos, intentelo de nuevo"]
        print(err)
        return render_template("inicioSesion.html", errores=err) 
        

@app.route("/detalle/<int:idCamisa>")
def detalles(idCamisa=None):
    if g.user==None:
        return redirect("/")
    try:
        camisa =mod.get_camisa_id(idCamisa)
        disenos= mod.get_disenos()
        return render_template("detalles.html", camiseta=camisa, diseños=disenos)
    except: 
        return redirect("/")

@app.route("/agregar_a_carrito/")
@app.route("/agregar_a_carrito/<int:idCamisa>")
@app.route("/agregar_a_carrito/<int:idCamisa>/<int:idDiseno>")
def agregar_a_carrito(idCamisa=None, idDiseno=None):
    try:
        print(idDiseno)
        print(idCamisa)
        creacion=mod.set_camisa_diseno(idCamisa,idDiseno)
        print(creacion)
        if creacion== "Creacion exitosa":
            return redirect("/carro")
        else:
            return redirect("/detalle")
    except:
        return redirect("/")

@app.route("/carro")
def carro():
    try:
        if(g.carro!=None):
            return render_template("carro.html")
        else:
            return redirect("/")
    except:
        return redirect("/")

@app.route("/diseño",methods = ["GET", "POST"])
def diseño():
    try:
        if request.method=="POST":
            img=request.form["imagen"]

        else:
            return render_template("diseño.html")
    except: 
        return render_template("diseño.html")

@app.route("/perfil/")
def perfil():
    return render_template("perfil.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.before_request
def load_logged_in_user():
    id_usuario = session.get('id_usuario')
    
    if id_usuario is None:
        g.user = None
    else:
        g.user = mod.get_usuario_id(id_usuario)
        g.carro= mod.get_carrito(id_usuario)

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)
