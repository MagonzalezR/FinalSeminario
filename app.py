from flask import Flask, render_template, request, redirect, session, g
import utils as ut
import db as mod
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config['UPLOAD_FOLDER'] = "./static/imagesD"

@app.route("/")
def index():
    print(g.user)
    if g.user !=None:

        camisas = mod.get_camisas()
        return render_template("loged.html", imagenes=camisas)
    return render_template("index.html")

@app.route("/registro", methods = ["GET", "POST"])
def registro():
    if g.user !=None:
        return redirect("/")
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
    if g.user != None:
        return redirect("/")
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
    if g.user==None:
        return redirect("/")
    try:
        print(idDiseno)
        print(idCamisa)
        print(g.carrito[0])
        creado=mod.get_camisa_diseño(g.carrito[0],idDiseno,idCamisa)
        print(creado)
        if creado =="F":
            creacion=mod.set_camisa_diseno(g.carrito[0],idCamisa,idDiseno)
        else:
            creacion=mod.actualizar_camisa_diseño(creado[4]+1, creado[3])
        camisa=mod.get_valor_camisa(idCamisa)
        actualizado=mod.actualizar_valor_carrito(g.carrito[0], g.carrito[1]+camisa[0])
        print(creacion)
        print(actualizado)

        if actualizado== "Carrito actualizado" and creacion=="Creacion exitosa" :
            return redirect("/carro")
        else:
            return redirect("/detalle")
    except:
        return redirect("/")

@app.route("/carro")
def carro():
    if g.user==None:
        return redirect("/")
    try:
        if(g.carrito!=None):
            camisas=mod.get_camisas_carrito(g.carrito[0])
            designes=mod.get_designe_carrito(g.carrito[0])
            return render_template("carro.html", camisas=camisas, designes=designes, total=g.carrito[1])
        else:
            return redirect("/")
    except:
        return redirect("/")

@app.route("/pagar")
def pagar():
    if  g.user==None:
        return redirect("/")
    try:
        disponibles=mod.get_hay_disponibles(g.carrito[0])
        if disponibles!=None:
            camisas=ut.sumarCamisas(disponibles)
            for i in camisas:
                
                if i[0]>i[1]:
                    print("error 1")
                    return redirect("/")
                else:
                    nuevo=i[1]-i[0]
                    actualizacion=mod.update_camiseta(i[2], nuevo)
                    
            mod.actualizar_valor_carrito(g.carrito[0], 0)
            print("error 2")
            mod.delete_referencias(g.carrito[0])
            print("error 3")
            if( actualizacion=="actualizacion exitosa"):
                return redirect("/perfil")
            else:
                return redirect("/")
        else:
            return redirect("/carro")
    except:
        return redirect("/")

@app.route("/diseño")
def diseño():
    if g.user==None:
        return redirect("/")
    return render_template("diseño.html")

@app.route("/guardar_dis", methods = ["POST"])
def guardar_dis():
    try:
        if g.user!=None:
            print("hola")
            nombre= request.form["titulo"]
            print("hay titulo")
            if "imagen" in request.files:
                print("hay imagen")
                imagen_file = request.files['imagen']
            if nombre!="" and imagen_file!="":
                print("hay titulo e imagen")
                if imagen_file.filename:
                    print("es archivo")
                    imagen_file.save(os.path.join(app.config['UPLOAD_FOLDER'],str(imagen_file.filename)))
                    print("se guardo el archivo")
                    img_data_to_db = mod.set_diseño(nombre, str(imagen_file.filename), g.user[0])
                    if img_data_to_db=="Creacion exitosa":
                            return redirect("/perfil")
            return redirect("/diseño")
        return redirect("/diseño")
    except:
        return redirect("/")
@app.route("/perfil")
def perfil():
    if g.user==None:
        return redirect("/")
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
        g.carrito= mod.get_carrito(id_usuario)

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)
