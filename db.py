from logging import ERROR
import pymysql as psql

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

def set_camisa_diseno(idCamisa, idDiseno):
    try:
        conexion=get_db()
        print("HOLA")
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO mydb.camiseta_has_diseño (Camiseta_idCamiseta, Diseño_idDiseño) VALUES(%s,%s);",(idCamisa,idDiseno))
        
        conexion.commit()
        conexion.close()
        return "Creacion exitosa"
    except ERROR as er:
        return er