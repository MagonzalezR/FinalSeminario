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

#def close_db(e=None):







#def sql_read(query,arreglo):



#def sql_update(query,arreglo):



#def sql_delete(query,arreglo):
