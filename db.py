from logging import ERROR, error
from os import truncate
import pymysql as psql
from pymysql.connections import Connection

def get_db():
    return psql.connect(host="localhost",
                        user="root",
                        passwd="root",
                        database="mydb")

def ingresar_usuario(user,correo,password):
    try:
        conexion=get_db()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO usuario(usuarioNick,usuarioCorreo,usuarioPass) VALUES (%s, %s, %s)",
                            (user,correo,password))
        conexion.commit()
        conexion.close()
        return "Creacion exitosa"
    except(Exception) as e:
        error=None
        if(str(e)=="UNIQUE constraint failed: Usuario.username"):
            error = 'El usuario ya existe, intente nuevamente con un usuario diferente'
        elif(str(e)=="UNIQUE constraint failed: Usuario.email"):
            error = u'Esta dirección de correo ya está registrada'
        else:
            error = e
        return error 

def comprobar_usuario(correo,password):
    try:
        conexion=get_db()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM mydb.usuario where usuarioCorreo = %s and usuarioPass = %s ",(correo,password))
            user=cursor.fetchone()
        conexion.close()
        return user
    except(Exception) as error:
        return error

def get_usuario_id(id):
    try:
        conexion=get_db()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM mydb.usuario where idUsuario= %s ",(id))
            user=cursor.fetchone()
        conexion.close()
        return user
    except(Exception) as error:
        return error

def get_camisas():
    try:
        conexion=get_db()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM mydb.camiseta")
            camisas=cursor.fetchall()
        conexion.close()
        return camisas
    except(Exception) as error:
        return error

def get_camisa_id(id):
    try:
        conexion=get_db()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM mydb.camiseta where idCamiseta= %s ",(id))
            camisa=cursor.fetchone()
        conexion.close()
        return camisa
    except:
        return None

def creaCarrito(idUser):
    try:
        conexion=get_db()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO carrito(Valor,Usuario_idUsuario) VALUES (%s, %s)",
                            (0,idUser))
        conexion.commit()
        conexion.close()
        return "Creacion exitosa"
    except(Exception) as error:
        return error 

def get_carrito(idUser):
    try:
        conexion=get_db()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM mydb.carrito where Usuario_idUsuario= %s ",(idUser))
            carro=cursor.fetchone()
        conexion.close()
        return carro
    except(Exception) as error:
        return error

def get_disenos():
    try:
        conexion=get_db()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM mydb.diseño")
            disenos=cursor.fetchall()
            print(disenos)
        conexion.close()
        return disenos
    except(Exception) as error:
        return error

def get_diseno_id(id):
    try:
        conexion=get_db()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM mydb.diseño where idDiseño= %s ",(id))
            diseno=cursor.fetchone()
        conexion.close()
        return diseno
    except:
        return None

def get_camisa_diseño(idCarrito, idDiseño, idCamisa):
    try:
        conexion=get_db()
        with conexion.cursor() as cursor:
            cursor.execute("select * from mydb.carrito_camisa_diseño where carrito_camisa_diseño.carrito_idCarrito=%s and carrito_camisa_diseño.diseño_idDiseño= %s and carrito_camisa_diseño.camiseta_idCamiseta=%s",(idCarrito, idDiseño, idCamisa))
            camisa_diseño=cursor.fetchone()
        conexion.close()
        return camisa_diseño
    except :
        return "F"

def set_camisa_diseno(idCarrito, idCamisa, idDiseno):
    try:
        conexion=get_db()
        
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO mydb.carrito_camisa_diseño (carrito_idCarrito, diseño_idDiseño, camiseta_idCamiseta) VALUES(%s,%s,%s);",(idCarrito, idDiseno, idCamisa))
        
        conexion.commit()
        conexion.close()
        return "Creacion exitosa"
    except ERROR as er:
        return er
def actualizar_camisa_diseño(cantidad, id):
    try:
        conexion=get_db()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE mydb.carrito_camisa_diseño SET cantidad = %s WHERE (id = %s);",(cantidad, id))
        conexion.commit()
        conexion.close()
        return "Creacion exitosa"
    except(Exception) as error:
        return error 
def get_valor_camisa(id):
    try:
        conexion=get_db()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT mydb.camiseta.Costo FROM mydb.camiseta where idCamiseta= %s ",(id))
            camisa=cursor.fetchone()
        conexion.close()
        print(camisa[0])
        return camisa
    except:
        return None

def actualizar_valor_carrito(id, valor):
    try:
        conexion=get_db()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE mydb.carrito SET Valor = %s WHERE (idCarrito = %s);",(valor, id))
        conexion.commit()
        conexion.close()
        return "Carrito actualizado"
    except(Exception) as error:
        return error 

def get_camisas_carrito(id):
    try:
        conexion=get_db()
        with conexion.cursor() as cursor:
            cursor.execute("""SELECT mydb.camiseta.* FROM mydb.carrito, mydb.camiseta, mydb.carrito_camisa_diseño
                        where carrito.idCarrito=%s and carrito_camisa_diseño.carrito_idCarrito=carrito.idCarrito 
                        and camiseta.idCamiseta=carrito_camisa_diseño.camiseta_idCamiseta; """,(id))
            camisas=cursor.fetchall()
        conexion.close()
        print(camisas)
        return camisas
    except:
        return None

def get_designe_carrito(id):
    try:
        conexion=get_db()
        with conexion.cursor() as cursor:
            cursor.execute("""SELECT mydb.diseño.* FROM mydb.carrito, mydb.diseño, mydb.carrito_camisa_diseño
                        where carrito.idCarrito=%s and carrito_camisa_diseño.carrito_idCarrito=carrito.idCarrito 
                        and diseño.idDiseño=carrito_camisa_diseño.diseño_idDiseño; """,(id))
            diseños=cursor.fetchall()
        conexion.close()
        print(diseños)
        return diseños
    except:
        return None

def get_hay_disponibles(idCarrito):
    try:
        conexion=get_db()
        with conexion.cursor() as cursor:
            cursor.execute("""SELECT mydb.carrito_camisa_diseño.cantidad, mydb.camiseta.Disponibilidad, mydb.camiseta.idCamiseta FROM mydb.carrito_camisa_diseño, mydb.camiseta
                    where carrito_camisa_diseño.carrito_idCarrito=%s
                    and camiseta.idCamiseta=carrito_camisa_diseño.camiseta_idCamiseta """,(idCarrito))
            disponibles=cursor.fetchall()
        conexion.close()
        print(disponibles)
        return disponibles
    except:
        return None

def update_camiseta(idCamiseta, Disponibles):
    print(idCamiseta)
    print(Disponibles)
    try:
        conexion=get_db()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE mydb.camiseta SET Disponibilidad = %s WHERE (idCamiseta = %s);",(Disponibles, idCamiseta))
        conexion.commit()
        conexion.close()
        print("actualizo")
        return "actualizacion exitosa"
    except:
        print("error aqui")
        return "F"
def delete_referencias(idCarrito):
    try:
        conexion=get_db()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM mydb.carrito_camisa_diseño WHERE (carrito_idCarrito = %s);",(idCarrito))
        conexion.commit()
        conexion.close()
        return "borrado exitoso"
    except:
        return "F"