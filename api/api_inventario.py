import requests, json

def server_json():
    try:
        ruta = f"config/config.json"
        with open(ruta, "r", encoding="UTF-8") as archivo:
            datos_server = json.load(archivo)
        return datos_server
    except Exception as e:
        print(e)
        return False

def api_login(usuario, contrasena):
    try:
        datos_server = server_json()
        apiServ = 'inventario_login'
        config = datos_server["url_api"]
        url = f"{config}/{apiServ}"
        data = {
            "usuario":usuario,
            "contrasena":contrasena
        }
        respuesta = requests.post(url, json=data)
        return respuesta.json()
    except Exception as e:
        print(e)

def api_registrar_prod(nombre, categoria, stock, id_usuarios):
    try:
        datos_server = server_json()
        apiServ = 'inventario_registro_prod'
        config = datos_server["url_api"]
        url = f"{config}/{apiServ}"
        data = {
            "nombre": nombre,
            "categoria": categoria,
            "stock": stock,
            "usuario": id_usuarios
        }
        respuesta = requests.post(url, json=data)
        return respuesta.json()
    except Exception as e:
        print(e)

def api_datos_usuario(usuario):
    try:
        data_server = server_json()
        apiServ = 'datos_usuario'
        config = data_server["url_api"]
        url = f"{config}/{apiServ}"
        data = {
            "usuario": usuario
        }
        respuesta = requests.post(url, json=data)
        return respuesta.json()
    except Exception as e:
        print(e)

def api_consulta_categorias():
    try:
        data_server = server_json()
        apiServ = 'inventario_consulta_categorias'
        config = data_server["url_api"]
        url = f"{config}/{apiServ}"
        respuesta = requests.get(url)
        return respuesta.json()
    except Exception as e:
        print(e)

def api_consultar_tipo_movimientos():
    try:
        data_server = server_json()
        apiServ = 'inventario_consulta_tipo_movimientos'
        config = data_server["url_api"]
        url = f"{config}/{apiServ}"
        respuesta = requests.get(url)
        return respuesta.json()
    except Exception as e:
        print(e)

def api_consulta_roles():
    try:
        data_server = server_json()
        apiServ = 'inventario_consulta_roles'
        config = data_server["url_api"]
        url = f"{config}/{apiServ}"
        respuesta = requests.get(url)
        return respuesta.json()
    except Exception as e:
        print(e)

def api_listar_productos():
    try:
        data_server = server_json()
        apiServ = 'inventario_listar_productos'
        config = data_server["url_api"]
        url = f"{config}/{apiServ}"
        respuesta = requests.get(url)
        return respuesta.json()
    except Exception as e:
        print(e)

def api_listar_usuarios(dni):
    try:
        data_server = server_json()
        apiServ = 'inventario_listar_usuarios'
        config = data_server["url_api"]
        url = f"{config}/{apiServ}"
        data = {
            "dni": dni
        }
        respuesta = requests.post(url, json=data)
        return respuesta.json()
    except Exception as e:
        print(e)

def api_eliminar_producto(codigo):
    try:
        datos_server = server_json()
        apiServ = 'inventario_eliminar_productos'
        config = datos_server["url_api"]
        url = f"{config}/{apiServ}"
        data = {
            "codigo": codigo
        }
        respuesta = requests.post(url, json=data)
        return respuesta.json()
    except Exception as e:
        print(e)

def api_modificar_producto(codigo, nombre, categoria, stock):
    try:
        datos_server = server_json()
        apiServ = 'inventario_modificar_productos'
        config = datos_server["url_api"]
        url = f"{config}/{apiServ}"
        data = {
            "codigo": codigo,
            "nombre": nombre,
            "categoria" : categoria,
            "stock" : stock
        }
        respuesta = requests.post(url, json=data)
        return respuesta.json()
    except Exception as e:
        print(e)

def api_filtrar_producto(codigo, nombre, categoria, fecha_inicio, fecha_fin):
    try:
        datos_server = server_json()
        apiServ = 'inventario_filtrar_productos'
        config = datos_server["url_api"]
        url = f"{config}/{apiServ}"
        data = {
            "codigo": codigo,
            "nombre": nombre,
            "categoria" : categoria,
            "fecha_inicio" : fecha_inicio,
            "fecha_fin" : fecha_fin
        }
        respuesta = requests.post(url, json=data)
        return respuesta.json()
    except Exception as e:
        print(e)

def api_registrar_usuario(dni, nombre, apellido_paterno, apellido_materno, fecha_nacimiento, rol):
    try:
        print("a")
        dato_server = server_json()
        apiServ = 'inventario_registro_usuario'
        config = dato_server["url_api"]
        url = f"{config}/{apiServ}"
        data = {
            "dni": dni,
            "nombre": nombre,
            "apellido_paterno": apellido_paterno,
            "apellido_materno": apellido_materno,
            "fecha_nacimiento": fecha_nacimiento,   
            "rol": rol
        }
        print("b")
        respuesta = requests.post(url, json=data)
        print("c")
        return respuesta.json()
    except Exception as e:
        print(e)

def api_modificar_usuarios(dni, nombre, apellido_paterno, apellido_materno, fecha_nacimiento, rol):
    try:
        dato_server = server_json()
        apiServ = 'inventario_modificar_usuarios'
        config = dato_server["url_api"]
        url = f"{config}/{apiServ}"
        data = {
            "dni": dni,
            "nombre": nombre,
            "apellido_paterno": apellido_paterno,
            "apellido_materno": apellido_materno,
            "fecha_nacimiento": fecha_nacimiento,   
            "rol": rol
        }
        respuesta = requests.post(url, json=data)
        return respuesta.json()
    except Exception as e:
        print(e)

def api_eliminar_usuarios(dni):
    try:
        datos_server = server_json()
        apiServ = 'inventario_eliminar_usuarios'
        config = datos_server["url_api"]
        url = f"{config}/{apiServ}"
        data = {
            "dni": dni
        }
        respuesta = requests.post(url, json=data)
        return respuesta.json()
    except Exception as e:
        print(e)

def api_filtrar_usuarios(dni, nombre, rol):
    try:
        datos_server = server_json()
        apiServ = 'inventario_filtrar_usuarios'
        config = datos_server["url_api"]
        url = f"{config}/{apiServ}"
        data = {
            "dni": dni,
            "nombre": nombre,
            "rol": rol
        }
        respuesta = requests.post(url, json=data)
        return respuesta.json()
    except Exception as e:
        print(e)

def api_insertar_movimientos(tipo_movimiento, cantidad, codigo, usuario, detalles):
    try:
        print("a")
        dato_server = server_json()
        apiServ = 'inventario_insertar_movimientos'
        config = dato_server["url_api"]
        url = f"{config}/{apiServ}"
        data = {
        "motivo": tipo_movimiento,
        "cantidad": cantidad,
        "codigo": codigo,
        "usuario": usuario,
        "detalles": detalles
        }
        print("b")
        respuesta = requests.post(url, json=data)
        print("c")
        return respuesta.json()
    except Exception as e:
        print(e)

def api_obtener_ultimo_id_producto():
    try:
        data_server = server_json()
        apiServ = 'obtener_ultimo_id_producto'
        config = data_server["url_api"]
        url = f"{config}/{apiServ}"
        respuesta = requests.get(url)
        return respuesta.json()
    except Exception as e:
        print(e)

def api_listar_movimientos(fecha_inicio, fecha_fin):
    try:
        data_server = server_json()
        apiServ = 'inventario_listar_movimientos'
        config = data_server["url_api"]
        url = f"{config}/{apiServ}"
        data = {
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin
        }
        respuesta = requests.post(url, json=data)
        return respuesta.json()
    except Exception as e:
        print(e)


    