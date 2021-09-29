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
            print(user)
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
            print(camisas)
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
            print(camisa)
        conexion.close()
        return camisa
    except(Exception) as error:
        return error

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
            print(carro)
        conexion.close()
        return carro
    except(Exception) as error:
        return error



#def sql_delete(query,arreglo):
