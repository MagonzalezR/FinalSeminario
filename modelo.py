from db import *

def ingresar_usuario(user,correo,password):
    try:
        arreglo=(user,correo,password)
        query='"INSERT INTO usuario(usuarioNick,usuarioCorreo,usuarioPass) VALUES (%s, %s, %s)"'
        sql_create(query,arreglo)
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