from api.api_inventario import api_datos_usuario

def obtener_datos_usuario(usuario):
    try:
        datos_usuario = api_datos_usuario(usuario)
        dni = datos_usuario[0][0]
        nombre =  datos_usuario[0][1]
        apellido_paterno = datos_usuario[0][2]
        apellido_materno = datos_usuario[0][3]
        fecha_nacimiento = datos_usuario[0][4]
        rol = datos_usuario[0][5]
        fecha_registro = datos_usuario[0][6]
        fecha_modificacion = datos_usuario[0][7]
        estado = datos_usuario[0][8]
        id_usuarios = datos_usuario[0][9]
        return dni, nombre, apellido_paterno, apellido_materno, fecha_nacimiento, rol, fecha_registro, fecha_modificacion, estado, id_usuarios
    except Exception as e:
        print("Error en obtener datos del usuario: ",e)
        return False, False, False, False, False, False, False, False, False