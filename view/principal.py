from customtkinter import *
from PIL import Image
from tkcalendar import Calendar
import tkinter as tk
from tkinter import messagebox, Canvas
from view.login import *
from api.api_inventario import api_consulta_categorias, api_listar_productos, api_eliminar_producto, api_filtrar_producto
from utils.utils import obtener_datos_usuario

def mostrar_calendario(entry):
    top = tk.Toplevel(entry.master)
    cal = Calendar(top, selectmode='day',
                        firstweekday='monday',
                        showweeknumbers=False,
                        date_pattern='yyyy-mm-dd')
    cal.pack(padx=10, pady=10)

    def seleccionar_y_cerrar():
        fecha_seleccionada = cal.get_date()
        entry.delete(0, END)
        entry.insert(0, fecha_seleccionada)
        top.destroy()

    boton_seleccionar = CTkButton(top, text="Seleccionar", command=seleccionar_y_cerrar)
    boton_seleccionar.pack(pady=5)

def principal(permiso, usuario):
    ventana = CTk()
    ventana.geometry("1485x600")
    ventana.title("INVENTARIO")
    ventana.resizable(width=False, height=False)
    # Marco lateral izquierdo
    panel = CTkFrame(ventana, width=800, height=600)
    panel.pack(side="left", fill="y")

    try:
        dni, nombre, apellido_paterno, apellido_materno, fecha_nacimiento, rol, fecha_registro, fecha_modificacion, estado, id_usuarios = obtener_datos_usuario(usuario)
        print(nombre)
        print(apellido_paterno)
        print(id_usuarios)
    except Exception as e:
        print(e)

    try:
        image = Image.open("img/perfil.png")
        image = Image.open(image)
        rezized_image = image.resize((350, 350))
        photo = CTkImage(rezized_image, size=(50, 50))
        ventana.photo = photo
        imageLabel = CTkLabel(panel, image=photo, text=" ")
        imageLabel.pack(pady=10, padx=60)
    except Exception as e:
        print(f"Error al cargar imagen: {e}")
        imageLabel = CTkLabel(panel, text="👤", font=("Arial", 60))
        imageLabel.pack(pady=10, padx=60)

    # Botones del panel lateral
    label_perfil = CTkLabel(panel, text=f"{usuario}")
    label_perfil.pack()

    def gestion_usuario():
        try:
            if permiso == "ADMINISTRADOR" or permiso == "MASTER":
                from view.v_gestion_usua.gestion_usuario import gestion_usuario
                gestion_usuario(dni)
            else:
                messagebox.showinfo("ALERTA", "NO CUENTA CON PERMISOS DE ADMINISTRADOR")
        except Exception as e:
            print(e)
            return False

    boton_panel = CTkButton(panel, text="GESTION DE USUARIOS", width=140, command=gestion_usuario)
    boton_panel.pack(pady = 15)
    
    def cerrar_sesion():
        try:
            from view.login import login
            if messagebox.askyesno("Cerrar sesión", "¿Está seguro que desea cerrar la sesión?"):
                ventana.destroy()
                login()
        except Exception as e:
            print(f"Error al cerrar sesión: {e}")
            messagebox.showerror("Error", "No se pudo cerrar la sesión")

    boton_cerrar_sesion = CTkButton(panel, text="CERRAR SESION", width=150, command=cerrar_sesion)
    boton_cerrar_sesion.pack(pady = 0)
    
    labelVersion = CTkLabel(panel, text="V 1.1.1")
    labelVersion.pack(side = "bottom", pady = 5)
    boton_ayuda = CTkButton(panel, text="AYUDA", width=150)
    boton_ayuda.pack(side = "bottom", pady = 5)
    
    # Marco principal derecho

    marco_principal = CTkFrame(ventana, fg_color="#343434")
    marco_principal.pack(side = "right", fill = "both", expand = True)
    

    # Etiquetas de encabezado
    lista_categorias = api_consulta_categorias()
    etiqueta_codigo = CTkLabel(marco_principal, text="CODIGO:")
    etiqueta_codigo.grid(row=0, column=0, padx=10, pady=10)
    entrada_codigo = CTkEntry(marco_principal)
    entrada_codigo.grid(row=0, column=1, padx=10, pady=10)
    etiqueta_nombre = CTkLabel(marco_principal, text="NOMBRE:")
    etiqueta_nombre.grid(row=0, column=2, padx=10, pady=10)
    entrada_nombre = CTkEntry(marco_principal)
    entrada_nombre.grid(row=0, column=3, padx=10, pady=10)
    etiqueta_categoria = CTkLabel(marco_principal, text="CATEGORIA:")
    etiqueta_categoria.grid(row=0, column=4, padx=10, pady=10)
    combo_categoria = CTkComboBox(marco_principal, values=lista_categorias,
                                        width=150, height=30, font=("Arial", 12), dropdown_font=("Arial", 11), fg_color="#343434", text_color="white", dropdown_fg_color="#343434",
                                        dropdown_hover_color="#006fa9", dropdown_text_color="white", button_color="#006fa9", button_hover_color="#006633", border_color="#555555",
                                        border_width=1, corner_radius=5, state="readonly"
                                        )
    combo_categoria.grid(row=0, column=5, padx=10, pady=10)
    combo_categoria.set("SELECCIONE")
    etiqueta_nombre = CTkLabel(marco_principal, text="FECHA:")
    etiqueta_nombre.grid(row=0, column=6, padx=10, pady=10)
    entrada_fecha_inicio = CTkEntry(marco_principal)
    entrada_fecha_inicio.grid(row=0, column=7, padx=10, pady=10, sticky="ew")
    boton_calendario = CTkButton(marco_principal, text="📅", width=25, height=25, font=("Arial", 30), fg_color="#343434", border_color="#343434",hover_color="#343434",
                                                        command=lambda: mostrar_calendario(entrada_fecha_inicio))
    boton_calendario.grid(row=0, column=8, padx=10, pady=10, sticky="w")
    etiqueta_nombre = CTkLabel(marco_principal, text="hasta")
    etiqueta_nombre.grid(row=0, column=9, padx=10, pady=10)
    entrada_fecha_fin = CTkEntry(marco_principal)
    entrada_fecha_fin.grid(row=0, column=10, padx=10, pady=10, sticky="ew")
    boton_calendario = CTkButton(marco_principal, text="📅", width=25, height=25, font=("Arial", 30), fg_color="#343434", border_color="#343434", hover_color="#343434",
                                                        command=lambda: mostrar_calendario(entrada_fecha_fin))
    boton_calendario.grid(row=0, column=11, padx=10, pady=10, sticky="w")

    def registrar_producto():
        try:
            from view.v_registrar_prod.registrar import registrar_producto
            registrar_producto(permiso, usuario, ventana, lista_categorias, id_usuarios, actualizar_tabla)
        except Exception as e:
            print(e)


    boton_registrar = CTkButton(marco_principal, text="REGISTRAR", fg_color="#2A8C55", command=registrar_producto) # Y aquí
    boton_registrar.grid(row=1, column=10, padx=10, pady=10)


    def reporte():
        try:
            from view.v_reporte.reporte import generar_reportes_ventana
            generar_reportes_ventana()
        except Exception as e:
            print(e)

    if  permiso == "ADMINISTRADOR" or permiso == "MASTER":    
        boton_reporte = CTkButton(marco_principal, text="REPORTE", fg_color="#2A8C55", command=reporte)
        boton_reporte.grid(row=1, column=7, padx=10, pady=10)
        

    def filtrar_productos():
        try:
            filtrar_codigo = entrada_codigo.get()
            filtrar_nombre = entrada_nombre.get()
            filtrar_categoria = combo_categoria.get()
            filtrar_fecha_inicio = entrada_fecha_inicio.get()
            filtrar_fecha_fin = entrada_fecha_fin.get()
            filtrar_resultado = api_filtrar_producto(filtrar_codigo, filtrar_nombre, filtrar_categoria, filtrar_fecha_inicio, filtrar_fecha_fin)
            actualizar_tabla(filtrar_resultado)
        except Exception as e:
            print(e)

    boton_buscar = CTkButton(marco_principal, text="🔎", width=25, height=25, fg_color="#006fa9", font=("Arial",20), command=filtrar_productos)
    boton_buscar.grid(row=1, column=11, padx=10, pady=10)

   # TabView
    tabview = CTkTabview(marco_principal, fg_color="#343434", text_color="#343434",
                                segmented_button_fg_color="#343434",
                                segmented_button_selected_color="#343434",
                                segmented_button_unselected_color="#343434",
                                segmented_button_unselected_hover_color="#343434",
                                segmented_button_selected_hover_color="#343434",)
    tabview.grid(row=3, column=0, columnspan=12, sticky="nsew")
    marco_principal.grid_rowconfigure(3, weight=1)
    marco_principal.grid_columnconfigure(0, weight=1)

    # Añadir pestaña principal
    tabview.add("INVENTARIO")
    tabview.set("INVENTARIO")

    # Frame contenedor con scrollbar
    frame_contenedor = CTkFrame(tabview.tab("INVENTARIO"))
    frame_contenedor.pack(fill="both", expand=True)

    header_frame = CTkFrame(frame_contenedor, fg_color="#464545")
    header_frame.pack(side="top", fill="x")

    # Canvas para la tabla
    canvas_tabla = Canvas(frame_contenedor, bg="#464545", highlightthickness=0)  
    canvas_tabla.pack(side="left", fill="both", expand=True)

    # Frame para la tabla (dentro del canvas)
    frame_tabla = CTkFrame(canvas_tabla, fg_color="#464545")
    frame_tabla.pack(fill="both", expand=True)
    canvas_tabla.create_window((0, 0), window=frame_tabla, anchor="nw")


    # Encabezados de columna mejorados
    encabezados = [
        {"text": "Código", "width": 240},  # Aumentado el ancho
        {"text": "Nombre", "width": 240},  # Aumentado el ancho
        {"text": "Cantidad", "width": 80},
        {"text": "Categoria", "width": 240}, # Aumentado el ancho
        {"text": "Fecha", "width": 260},    # Aumentado el ancho
        {"text": "Editar", "width": 100},
        {"text": "Eliminar", "width": 100}
    ]


    # Crear encabezados con estilo profesional
    for col, encabezado in enumerate(encabezados):
        CTkLabel(header_frame,
                 text=encabezado["text"],
                 font=("Arial", 12, "bold"),
                 width=encabezado["width"],
                 corner_radius=5,
                 fg_color="#2A8C55",
                 text_color="white").grid(
            row=0, column=col, padx=2, pady=2, sticky="ew")

    # Configurar peso de columnas
    for col in range(len(encabezados)):
        frame_tabla.grid_columnconfigure(col, weight=1 if col < 4 else 0)

    # Función para eliminar un ítem
    def eliminar_producto(codigo):
        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar el producto {codigo}?",
            icon="warning")
        if respuesta:
            # Aquí iría la lógica para eliminar de tu base de datos
            validarEliminar = api_eliminar_producto(codigo)
            if validarEliminar:
                messagebox.showinfo("Éxito", f"Producto {codigo} eliminado correctamente")
                actualizar_tabla()  # Llama a la función para actualizar la tabla

    # Función para editar un ítem
    def editar_producto(codigo, nombre, stock, categoria, usuario):
        try:
            from view.v_modificar_prod.modificar import modificar_producto
            modificar_producto(codigo, nombre, stock, categoria, usuario, actualizar_tabla)
        except Exception as e:
            print(e)

    # Función para actualizar la tabla
    def actualizar_tabla(datos_productos=None):
        """
        Actualiza la tabla de productos en la interfaz.
        """
        # Limpiar la tabla, conservando solo los encabezados
        for widget in frame_tabla.winfo_children():
            if widget.grid_info()["row"] > 0:  # Elimina solo las filas de datos, no los encabezados
                widget.destroy()
        if datos_productos is None:
            try:
                datos_productos = api_listar_productos()
            except Exception as e:
                    print(e)
                    messagebox.showerror("Error", "No se pudieron cargar los productos")
                    return  # Importante: Detener la actualización si hay un error
        # Añadir filas de datos
        for row, producto in enumerate(datos_productos, start=1):
            # Datos del producto
            for col, valor in enumerate(producto):
                label = CTkLabel(frame_tabla,
                                text=valor,
                                anchor="center",
                                width=encabezados[col]["width"])
                label.grid(
                    row=row, column=col, padx=2, pady=2, sticky="ew")
                label.grid_columnconfigure(col, weight=1)

            # Botón Editar
            CTkButton(frame_tabla,
                    text="✏️ Editar",
                    width=encabezados[5]["width"],
                    fg_color="#3B8ED0",
                    hover_color="#36719F",
                    command=lambda c=producto[0], n=producto[1], s=producto[2], ca=producto[3]: editar_producto(c, n, s, ca, usuario)).grid(
                row=row, column=5, padx=2, pady=2)

            # Botón Eliminar
            CTkButton(frame_tabla,
                    text="🗑️ Eliminar",
                    width=encabezados[6]["width"],
                    fg_color="#D03535",
                    hover_color="#A02A2A",
                    command=lambda c=producto[0]: eliminar_producto(c)).grid(
                row=row, column=6, padx=2, pady=2)

        # Actualizar el scrollregion del canvas después de que los datos se han insertado
        frame_tabla.update_idletasks()
        canvas_tabla.configure(scrollregion=canvas_tabla.bbox("all"))

        # Verificar si el contenido excede el tamaño del canvas para mostrar u ocultar el scrollbar
        if frame_tabla.winfo_height() > canvas_tabla.winfo_height():
            #scrollbar_tabla.pack(side="right", fill="y")  # Mostrar scrollbar
            pass
        else:
            #scrollbar_tabla.pack_forget()  # Ocultar scrollbar
            pass
        def on_mousewheel(event):
            if event.delta < 0:  # Solo hacer scroll si la rueda del ratón se mueve hacia abajo
                canvas_tabla.yview_scroll(int(-1 * (event.delta / 120)), "units")
            elif event.delta > 0: # Agregado para scroll hacia arriba
                # Obtener la posición actual del canvas
                posicion_actual = canvas_tabla.yview()[0]
                if posicion_actual > 0:
                    canvas_tabla.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas_tabla.bind_all("<MouseWheel>", on_mousewheel)

    # Inicializar la tabla
    actualizar_tabla()

    ventana.mainloop()




