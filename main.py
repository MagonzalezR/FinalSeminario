from flask import Flask, render_template, request, redirect, session, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:root@localhost/mydb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config['UPLOAD_FOLDER'] = "./static/uploads"
db=SQLAlchemy(app)
g.db=db
g.db.session.begin()
g.db.session.connection()
g.db.session.close()

@app.route("/")
def inde():
    return render_template("index.html")

@app.route("/registro")
def registro():
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