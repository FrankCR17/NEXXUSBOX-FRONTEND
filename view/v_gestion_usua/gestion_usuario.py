from customtkinter import *
from tkinter import messagebox, Canvas
import tkinter as tk
from tkcalendar import Calendar
from api.api_inventario import api_consulta_roles, api_registrar_usuario, api_listar_usuarios, api_modificar_usuarios, api_eliminar_usuarios, api_filtrar_usuarios

_editing_dni = None

# Variable global para almacenar los datos de los usuarios en formato de diccionario
# para facilitar la edición y la consulta por DNI.
_usuarios_db_dict_format = []

def mostrar_calendario(entry):
    """
    Muestra un calendario para seleccionar una fecha y la inserta en el entry.
    """
    top = tk.Toplevel(entry.master)
    top.title("Seleccionar Fecha")
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
    top.grab_set() # Make the calendar modal
    top.focus_force()
    top.transient(entry.master.winfo_toplevel()) # Link to parent window for better focus management


def gestion_usuario(dni_p):
    # Usamos nonlocal si _editing_dni y _usuarios_db_dict_format son globales
    # Declarar como nonlocal aquí las hace accesibles y modificables desde esta función
    # si se declaran fuera de ella (en el ámbito global del módulo).
    global _editing_dni
    global _usuarios_db_dict_format

    try:
        ventana_gestion_usuarios = CTk()
        ventana_gestion_usuarios.geometry("1200x750") # Aumentado el tamaño
        ventana_gestion_usuarios.title("Gestión de Usuarios")
        ventana_gestion_usuarios.resizable(width=True, height=True)

        ancho_pantalla = ventana_gestion_usuarios.winfo_screenwidth()
        alto_pantalla = ventana_gestion_usuarios.winfo_screenheight()

        x_pos = int((ancho_pantalla - 1200) / 2)
        y_pos = int((alto_pantalla - 750) / 2)

        ventana_gestion_usuarios.geometry(f"+{x_pos}+{y_pos}")
        ventana_gestion_usuarios.grab_set()
        ventana_gestion_usuarios.focus_force()

        # Configure rows and columns for the main window
        ventana_gestion_usuarios.grid_rowconfigure(0, weight=0) # Frame para filtros/botones de tabla
        ventana_gestion_usuarios.grid_rowconfigure(1, weight=0) # Frame para el formulario (Crear/Editar)
        ventana_gestion_usuarios.grid_rowconfigure(2, weight=1) # Frame para la tabla (expands)
        ventana_gestion_usuarios.grid_columnconfigure(0, weight=1) # Single column (expands)

        # --- Marco para filtros y botones de tabla ---
        frame_filtros_tabla = CTkFrame(ventana_gestion_usuarios, fg_color="#343434")
        frame_filtros_tabla.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")

        # Columnas para los filtros en frame_filtros_tabla
        frame_filtros_tabla.grid_columnconfigure(0, weight=0) # Label DNI
        frame_filtros_tabla.grid_columnconfigure(1, weight=1) # Entry DNI
        frame_filtros_tabla.grid_columnconfigure(2, weight=0) # Label Nombre
        frame_filtros_tabla.grid_columnconfigure(3, weight=1) # Entry Nombre
        frame_filtros_tabla.grid_columnconfigure(4, weight=0) # Label Rol
        frame_filtros_tabla.grid_columnconfigure(5, weight=1) # Combo Rol
        frame_filtros_tabla.grid_columnconfigure(6, weight=0) # Botón Buscar

        etiqueta_dni_filtro = CTkLabel(frame_filtros_tabla, text="DNI:")
        etiqueta_dni_filtro.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        entrada_dni_filtro = CTkEntry(frame_filtros_tabla, width=150)
        entrada_dni_filtro.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        etiqueta_nombre_filtro = CTkLabel(frame_filtros_tabla, text="NOMBRE:")
        etiqueta_nombre_filtro.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        entrada_nombre_filtro = CTkEntry(frame_filtros_tabla, width=150)
        entrada_nombre_filtro.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        etiqueta_rol_filtro = CTkLabel(frame_filtros_tabla, text="ROL:")
        etiqueta_rol_filtro.grid(row=0, column=4, padx=5, pady=5, sticky="e")

        lista_roles_filtro = api_consulta_roles() # Usa la función de API asignada
        lista_roles_filtro_completa = ["SELECCIONE"] + [rol for rol in lista_roles_filtro if rol != "SELECCIONE"]
        combo_rol_filtro = CTkComboBox(frame_filtros_tabla, values=lista_roles_filtro_completa, state="readonly",
                                       width=150, height=30, font=("Arial", 12), dropdown_font=("Arial", 11), fg_color="#343434", text_color="white", dropdown_fg_color="#343434",
                                       dropdown_hover_color="#006fa9", dropdown_text_color="white", button_color="#006fa9", button_hover_color="#006633", border_color="#555555",
                                       border_width=1, corner_radius=5)
        combo_rol_filtro.set("SELECCIONE")
        combo_rol_filtro.grid(row=0, column=5, padx=5, pady=5, sticky="w")

        def filtrar_usuarios():
            try:
                filtro_dni = entrada_dni_filtro.get().strip()
                filtro_nombre = entrada_nombre_filtro.get().strip()
                filtro_rol = combo_rol_filtro.get().strip()
                filtrar_resultado = api_filtrar_usuarios(filtro_dni, filtro_nombre, filtro_rol)
                actualizar_tabla_usuarios(filtrar_resultado)
            except Exception as e:
                messagebox.showerror("Error de Filtro", f"Ocurrió un error al buscar usuarios: {e}")
                print(f"Error en filtrar_usuarios: {e}")

        boton_buscar_filtro = CTkButton(frame_filtros_tabla, text="🔎", width=25, height=25, fg_color="#006fa9", font=("Arial", 20), command=filtrar_usuarios)
        boton_buscar_filtro.grid(row=0, column=6, padx=5, pady=5, sticky="w")


        # --- Marco para formularios de creación/modificación ---
        frame_form = CTkFrame(ventana_gestion_usuarios, fg_color="#343434")
        frame_form.grid(row=1, column=0, pady=10, padx=20, sticky="nsew")

        # Configure columns within frame_form
        frame_form.grid_columnconfigure(0, weight=0) # Labels column (minimal width)
        frame_form.grid_columnconfigure(1, weight=1) # Entries column (expands)
        frame_form.grid_columnconfigure(2, weight=0) # Calendar button column (minimal width)

        labels_entries = {}
        current_row = 0

        # DNI
        label_dni = CTkLabel(frame_form, text="DNI:")
        label_dni.grid(row=current_row, column=0, padx=5, pady=2, sticky="w")
        entry_dni = CTkEntry(frame_form)
        entry_dni.grid(row=current_row, column=1, padx=5, pady=2, sticky="ew")
        labels_entries["dni"] = entry_dni
        current_row += 1

        # Nombre
        label_nombre = CTkLabel(frame_form, text="Nombre:")
        label_nombre.grid(row=current_row, column=0, padx=5, pady=2, sticky="w")
        entry_nombre = CTkEntry(frame_form)
        entry_nombre.grid(row=current_row, column=1, padx=5, pady=2, sticky="ew")
        labels_entries["nombre"] = entry_nombre
        current_row += 1

        # Apellido Paterno
        label_apellido_paterno = CTkLabel(frame_form, text="Apellido Paterno:")
        label_apellido_paterno.grid(row=current_row, column=0, padx=5, pady=2, sticky="w")
        entry_apellido_paterno = CTkEntry(frame_form)
        entry_apellido_paterno.grid(row=current_row, column=1, padx=5, pady=2, sticky="ew")
        labels_entries["apellido_paterno"] = entry_apellido_paterno
        current_row += 1

        # Apellido Materno
        label_apellido_materno = CTkLabel(frame_form, text="Apellido Materno:")
        label_apellido_materno.grid(row=current_row, column=0, padx=5, pady=2, sticky="w")
        entry_apellido_materno = CTkEntry(frame_form)
        entry_apellido_materno.grid(row=current_row, column=1, padx=5, pady=2, sticky="ew")
        labels_entries["apellido_materno"] = entry_apellido_materno
        current_row += 1

        # Fecha Nacimiento (Se mantiene en el formulario para registrar/modificar)
        label_fecha_nacimiento = CTkLabel(frame_form, text="Fecha Nacimiento:")
        label_fecha_nacimiento.grid(row=current_row, column=0, padx=5, pady=2, sticky="w")
        entry_fecha_nacimiento = CTkEntry(frame_form)
        entry_fecha_nacimiento.grid(row=current_row, column=1, padx=5, pady=2, sticky="ew")
        labels_entries["fecha_nacimiento"] = entry_fecha_nacimiento

        boton_calendario_fn = CTkButton(frame_form, text="📅", width=25, height=25, font=("Arial", 20),
                                            fg_color="transparent", hover_color="#555555",
                                            command=lambda: mostrar_calendario(entry_fecha_nacimiento))
        boton_calendario_fn.grid(row=current_row, column=2, padx=2, pady=2, sticky="w")
        current_row += 1

        # Rol
        label_rol = CTkLabel(frame_form, text="Rol:")
        label_rol.grid(row=current_row, column=0, padx=5, pady=2, sticky="w")

        lista_roles = api_consulta_roles() # Usa la función de API asignada
        lista_roles_completa = ["SELECCIONE"] + [rol for rol in lista_roles if rol != "SELECCIONE"]
        combo_rol = CTkComboBox(frame_form, values=lista_roles_completa, state="readonly")
        combo_rol.grid(row=current_row, column=1, padx=5, pady=2, sticky="ew")
        combo_rol.set("SELECCIONE")
        labels_entries["rol"] = combo_rol
        current_row += 1

        # --- Botones de acción del formulario ---
        frame_botones_form = CTkFrame(frame_form, fg_color="transparent")
        frame_botones_form.grid(row=current_row, column=0, columnspan=3, pady=10, sticky="ew")

        frame_botones_form.grid_columnconfigure(0, weight=1) # Left spacer
        frame_botones_form.grid_columnconfigure(1, weight=0) # Button 1
        frame_botones_form.grid_columnconfigure(2, weight=0) # Button 2
        frame_botones_form.grid_columnconfigure(3, weight=1) # Right spacer


        def limpiar_formulario():
            """Limpia todos los campos del formulario y restablece los botones."""
            global _editing_dni # Modifica la variable global
            _editing_dni = None # Resetea el DNI en edición
            entry_dni.configure(state="normal") # Asegura que el DNI sea editable al limpiar/nuevo
            entry_dni.delete(0, END)
            entry_nombre.delete(0, END)
            entry_apellido_paterno.delete(0, END)
            entry_apellido_materno.delete(0, END)
            entry_fecha_nacimiento.delete(0, END)
            combo_rol.set("SELECCIONE")

            boton_crear.configure(state="normal")
            boton_guardar.configure(state="disabled")

        def guardar_cambios():
          try:
                if messagebox.askyesno("Modificar usuarios", "¿Estas seguro de hacer la modificación?", parent=frame_form):
                    dni = entry_dni.get().strip().upper()
                    nuevo_nombre = entry_nombre.get().strip().upper()
                    nuevo_apellido_paterno = entry_apellido_paterno.get().strip().upper()
                    nuevo_apellido_materno = entry_apellido_materno.get().strip().upper()
                    nuevo_fecha_nacimiento = entry_fecha_nacimiento.get().strip().upper()
                    nuevo_rol = combo_rol.get().strip().upper()
                    # Validar los datos antes de enviarlos
                    if not nuevo_nombre or nuevo_rol == "SELECCIONE" or not nuevo_apellido_paterno or not nuevo_apellido_materno or not nuevo_fecha_nacimiento:
                        messagebox.showerror("Error", "Por favor, complete todos los campos.", parent=frame_form)
                        return
                    resultado = api_modificar_usuarios(dni, nuevo_nombre, nuevo_apellido_paterno, nuevo_apellido_materno, nuevo_fecha_nacimiento, nuevo_rol)
                    print(resultado["mensaje"])
                    messagebox.showinfo("Modificar", f"Usuario modificado {dni}", parent=frame_form)
                    limpiar_formulario()
                    actualizar_tabla_usuarios()
                    return True
          except Exception as e:
              print(e)
              return False

        def registrar_usuario():
            global _editing_dni

            if _editing_dni is not None:
                messagebox.showwarning("Advertencia", "Actualmente estás editando un usuario. Por favor, guarda o cancela los cambios para registrar uno nuevo.")
                return

            try:
                dni = entry_dni.get().strip().upper()
                nombre = entry_nombre.get().strip().upper()
                apellido_paterno = entry_apellido_paterno.get().strip().upper()
                apellido_materno = entry_apellido_materno.get().strip().upper()
                fecha_nacimiento = entry_fecha_nacimiento.get().strip().upper()
                rol = combo_rol.get().strip().upper()

                if not dni or not nombre or not apellido_paterno or not apellido_materno or not fecha_nacimiento or rol == "SELECCIONE":
                    messagebox.showerror("Error de Validación", "Todos los campos obligatorios deben ser llenados.", parent=frame_form)
                    return

                if messagebox.askyesno("Registrar usuario", "¿Estás seguro de hacer el registro?", parent = frame_form):
                    resultado = api_registrar_usuario(dni, nombre, apellido_paterno, apellido_materno, fecha_nacimiento, rol) # Usa la función de API asignada
                    print(f"API Registrar Usuario Resultado: {resultado}")
                    if resultado.get("status") == 2:
                        messagebox.showinfo("ADVERTENCIA", resultado.get("mensaje", "Error desconocido"), parent = frame_form)
                    elif resultado.get("status") == 3:
                        messagebox.showinfo("ADVERTENCIA", resultado.get("mensaje", "Error desconocido"), parent = frame_form)
                    elif resultado.get("status") == 4:
                        messagebox.showinfo("ADVERTENCIA", resultado.get("mensaje", "Error desconocido"), parent = frame_form)
                    else:
                        messagebox.showinfo("Éxito", resultado.get("mensaje", "Registro exitoso"), parent = frame_form)
                        limpiar_formulario()
                        actualizar_tabla_usuarios()
                        print(resultado.get("mensaje", "Mensaje de registro no disponible"))
            except Exception as e:
                messagebox.showerror("Error de Registro", f"Ocurrió un error al registrar: {e}", parent=frame_form)
                print(f"Error en registrar_usuario: {e}")

        boton_crear = CTkButton(frame_botones_form, text="Crear Usuario", fg_color="#2A8C55", command=registrar_usuario)
        boton_crear.grid(row=0, column=1, padx=5, pady=5)

        boton_guardar = CTkButton(frame_botones_form, text="Guardar Cambios", fg_color="#3B8ED0", command=guardar_cambios)
        boton_guardar.grid(row=0, column=2, padx=5, pady=5)
        boton_guardar.configure(state="disabled")

        boton_limpiar = CTkButton(frame_botones_form, text="Limpiar / Nuevo", fg_color="#646464", command=limpiar_formulario)
        boton_limpiar.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # --- TabView para la tabla ---
        tabview = CTkTabview(ventana_gestion_usuarios, fg_color="#343434", text_color="#343434",
                            segmented_button_fg_color="#343434",
                            segmented_button_selected_color="#343434",
                            segmented_button_unselected_color="#343434",
                            segmented_button_unselected_hover_color="#343434",
                            segmented_button_selected_hover_color="#343434",)
        tabview.grid(row=2, column=0, sticky="nsew", padx=20, pady=10) # row=2 para estar debajo del formulario

        # Añadir pestaña de usuarios
        tabview.add("USUARIOS")
        tabview.set("USUARIOS")

        # Frame contenedor con scrollbar
        frame_contenedor = CTkFrame(tabview.tab("USUARIOS"))
        frame_contenedor.pack(fill="both", expand=True)

        header_frame_tabla = CTkFrame(frame_contenedor, fg_color="#2A8C55") # Cambiado a color del encabezado
        header_frame_tabla.pack(side="top", fill="x")

        # Canvas para la tabla
        canvas_tabla_usuarios = Canvas(frame_contenedor, bg="#464545", highlightthickness=0)
        canvas_tabla_usuarios.pack(side="left", fill="both", expand=True)

        # Scrollbar vertical
        scrollbar_tabla_usuarios = CTkScrollbar(frame_contenedor, command=canvas_tabla_usuarios.yview)

        # Configurar el canvas para el scrollbar
        canvas_tabla_usuarios.configure(yscrollcommand=scrollbar_tabla_usuarios.set)

        # Frame para la tabla (dentro del canvas)
        frame_datos_tabla = CTkFrame(canvas_tabla_usuarios, fg_color="#464545")
        canvas_tabla_usuarios_window_id = canvas_tabla_usuarios.create_window(
            (0, 0), window=frame_datos_tabla, anchor="nw", tags="table_frame"
        )

        # Encabezados de columna - AJUSTADOS A LA NUEVA ESTRUCTURA
        # Asegúrate que los widths sean apropiados para el contenido
        encabezados_tabla = [
            {"text": "DNI", "width": 100},
            {"text": "Nombre", "width": 120},
            {"text": "Ape. Paterno", "width": 120},
            {"text": "Ape. Materno", "width": 120},
            {"text": "Rol", "width": 100},
            {"text": "Usuario", "width": 100},
            {"text": "Estado", "width": 80},
            {"text": "Editar", "width": 60}, # Reducido el ancho para los botones
            {"text": "Act./Desh.", "width": 60} # Reducido el ancho para los botones
        ]

        # Crear encabezados con estilo profesional
        for col, encabezado in enumerate(encabezados_tabla):
            # Configurar el peso de la columna para el frame_datos_tabla
            # Las columnas de datos (0 a 6) se expanden, las de botones (7 y 8) tienen ancho fijo
            if col < 7: # Data columns
                frame_datos_tabla.grid_columnconfigure(col, weight=1)
                header_frame_tabla.grid_columnconfigure(col, weight=1) # Also expand header
            else: # Button columns
                frame_datos_tabla.grid_columnconfigure(col, weight=0)
                header_frame_tabla.grid_columnconfigure(col, weight=0) # Also fix header

            CTkLabel(header_frame_tabla,
                    text=encabezado["text"],
                    font=("Arial", 12, "bold"),
                    width=encabezado["width"], # Specify width for header labels
                    corner_radius=5,
                    fg_color="#2A8C55",
                    text_color="white",
                    anchor="center").grid( # Ensure text is centered in header
                row=0, column=col, padx=2, pady=2, sticky="ew")


        def resize_and_center_table_frame(event=None):
            """
            Redimensiona frame_datos_tabla para que coincida con el ancho del canvas y gestiona el scrollbar.
            """
            canvas_width = canvas_tabla_usuarios.winfo_width()
            canvas_height = canvas_tabla_usuarios.winfo_height()

            # Update the width of the window inside the canvas
            canvas_tabla_usuarios.itemconfig(canvas_tabla_usuarios_window_id, width=canvas_width)

            # Update idletasks to get correct frame_datos_tabla size
            frame_datos_tabla.update_idletasks()

            # Configure scrollregion
            canvas_tabla_usuarios.configure(scrollregion=canvas_tabla_usuarios.bbox("all"))

            # Show/hide scrollbar based on content height
            if frame_datos_tabla.winfo_height() > canvas_height:
                scrollbar_tabla_usuarios.pack(side="right", fill="y")
            else:
                scrollbar_tabla_usuarios.pack_forget()

        canvas_tabla_usuarios.bind("<Configure>", resize_and_center_table_frame)
        canvas_tabla_usuarios.bind_all("<MouseWheel>", lambda event: canvas_tabla_usuarios.yview_scroll(int(-1*(event.delta/120)), "units"))

        def eliminar_usuario(dni):
            try:
                respuesta = messagebox.askyesno("Confirmar cambio de estado", f"¿Estás seguro que deseas cambiar el estado de {dni}?", icon="warning", parent=ventana_gestion_usuarios)
                if respuesta:
                    # Aquí iría la lógica para eliminar de tu base de datos
                    validarEliminar = api_eliminar_usuarios(dni)
                    if validarEliminar:
                        messagebox.showinfo("Éxito", f"Usuario {dni} habilitado/deshabilitado correctamente", parent=ventana_gestion_usuarios)
                        actualizar_tabla_usuarios()  # Llama a la función para actualizar la tabla
                return True
            except Exception as e:
                print(e)
                return False
            
        def cargar_usuario_para_edicion(dni_usuario):
            """
            Carga los datos de un usuario en el formulario para su edición.
            """
            global _editing_dni
            global _usuarios_db_dict_format # Accede a la lista global de usuarios en formato diccionario

            usuario_a_editar = next((u for u in _usuarios_db_dict_format if u.get("dni") == dni_usuario), None)

            if usuario_a_editar:
                _editing_dni = dni_usuario # Establece el DNI del usuario que se está editando

                # Limpiar el formulario primero
                limpiar_formulario() # Esto resetea _editing_dni, así que lo reestablecemos después
                _editing_dni = dni_usuario # Re-establece el DNI después de limpiar

                # Rellenar los campos del formulario con los datos del usuario
                labels_entries["dni"].configure(state="normal") # Temporalmente editable para insertar
                labels_entries["dni"].delete(0, END)
                labels_entries["dni"].insert(0, usuario_a_editar.get("dni", ""))
                labels_entries["dni"].configure(state="readonly") # Luego lo hacemos de solo lectura

                labels_entries["nombre"].delete(0, END)
                labels_entries["nombre"].insert(0, usuario_a_editar.get("nombre", ""))

                labels_entries["apellido_paterno"].delete(0, END)
                labels_entries["apellido_paterno"].insert(0, usuario_a_editar.get("apellido_paterno", ""))

                labels_entries["apellido_materno"].delete(0, END)
                labels_entries["apellido_materno"].insert(0, usuario_a_editar.get("apellido_materno", ""))

                labels_entries["fecha_nacimiento"].delete(0, END)
                # Asegúrate que "fecha_nacimiento" esté disponible en el dict_format si lo necesitas para edición.
                # Si tu API de listar no lo devuelve, considera obtener los detalles completos del usuario en otra API
                # o modificar tu api_listar_usuarios para incluirlo.
                labels_entries["fecha_nacimiento"].insert(0, usuario_a_editar.get("fecha_nacimiento", ""))

                labels_entries["rol"].set(usuario_a_editar.get("rol", "SELECCIONE"))

                boton_crear.configure(state="disabled")
                boton_guardar.configure(state="normal")
            else:
                messagebox.showerror("Error", "Usuario no encontrado para edición.", parent=ventana_gestion_usuarios)
                print(f"DEBUG: No se encontró el usuario con DNI {dni_usuario} en _usuarios_db_dict_format.")

        def actualizar_tabla_usuarios(datos_usuarios_param=None):
            """
            Actualiza la tabla de usuarios en la interfaz.
            Si no se proporciona datos_usuarios, se obtienen de la API.
            """
            print("--- Actualizando tabla de usuarios ---")
            for widget in frame_datos_tabla.winfo_children():
                widget.destroy()

            global _usuarios_db_dict_format # Accede a la variable global

            if datos_usuarios_param is None:
                try:
                    datos_usuarios_raw = api_listar_usuarios(dni_p) # Usa la función de API asignada
                    print(f"Resultado de _api_listar_usuarios(): {datos_usuarios_raw}")

                    _usuarios_db_dict_format = [] # Limpia la lista global antes de rellenarla

                    if datos_usuarios_raw and isinstance(datos_usuarios_raw, list):
                        for user_list in datos_usuarios_raw:
                            # Asegúrate de que los índices coincidan con tu nueva estructura:
                            # a.dni, a.nombre, a.apellido_paterno, a.apellido_materno, b.rolesNombre, a.usuario, a.tmUsersEstado, a.fecha_nacimiento (si se añade)
                            if isinstance(user_list, (list, tuple)) and len(user_list) >= 7: # Mínimo 7 elementos
                                user_dict = {
                                    "dni": str(user_list[0] if user_list[0] is not None else ""),
                                    "nombre": str(user_list[1] if user_list[1] is not None else ""),
                                    "apellido_paterno": str(user_list[2] if user_list[2] is not None else ""),
                                    "apellido_materno": str(user_list[3] if user_list[3] is not None else ""),
                                    "rol": str(user_list[4] if user_list[4] is not None else ""),
                                    "usuario": str(user_list[5] if user_list[5] is not None else ""),
                                    "estado": str(user_list[6] if user_list[6] is not None else ""),
                                    "fecha_nacimiento": str(user_list[7] if len(user_list) > 7 and user_list[7] is not None else "") # Added for completeness if API provides it
                                }
                                _usuarios_db_dict_format.append(user_dict)
                            else:
                                print(f"DEBUG: Fila de usuario con formato inesperado (no es lista/tupla o tiene menos de 7 elementos): {user_list}")
                        datos_usuarios_to_display = _usuarios_db_dict_format
                    else:
                        print(f"DEBUG: _api_listar_usuarios() no devolvió una lista válida o está vacía: {datos_usuarios_raw}")
                        datos_usuarios_to_display = []

                except Exception as e:
                    print(f"ERROR: Falló al llamar a _api_listar_usuarios o procesar su respuesta: {e}")
                    messagebox.showerror("Error de Carga", f"No se pudieron cargar los usuarios: {e}", parent=ventana_gestion_usuarios)
                    datos_usuarios_to_display = []
            else:
                # Si se pasan datos (ej. desde el filtro), úsalos directamente
                _usuarios_db_dict_format = [] # Limpiar también al filtrar para mantener sincronizado
                for user_list in datos_usuarios_param:
                    if isinstance(user_list, (list, tuple)) and len(user_list) >= 7:
                        user_dict = {
                            "dni": str(user_list[0] if user_list[0] is not None else ""),
                            "nombre": str(user_list[1] if user_list[1] is not None else ""),
                            "apellido_paterno": str(user_list[2] if user_list[2] is not None else ""),
                            "apellido_materno": str(user_list[3] if user_list[3] is not None else ""),
                            "rol": str(user_list[4] if user_list[4] is not None else ""),
                            "usuario": str(user_list[5] if user_list[5] is not None else ""),
                            "estado": str(user_list[6] if user_list[6] is not None else ""),
                            "fecha_nacimiento": str(user_list[7] if len(user_list) > 7 and user_list[7] is not None else "")
                        }
                        _usuarios_db_dict_format.append(user_dict)
                datos_usuarios_to_display = _usuarios_db_dict_format


            print(f"DEBUG: Datos a mostrar en la tabla (final): {datos_usuarios_to_display}")

            if not datos_usuarios_to_display:
                CTkLabel(frame_datos_tabla, text="No hay usuarios registrados.", text_color="white", anchor="center").grid(row=0, column=0, columnspan=len(encabezados_tabla), pady=20, sticky="ew")
                # Ensure the single column with the message expands
                frame_datos_tabla.grid_columnconfigure(0, weight=1)
                for i in range(1, len(encabezados_tabla)): # Ensure other columns have no weight
                    frame_datos_tabla.grid_columnconfigure(i, weight=0)

                frame_datos_tabla.update_idletasks()
                resize_and_center_table_frame()
                return

            # Add data rows
            for row_idx, user_data in enumerate(datos_usuarios_to_display):
                # Usar .get() es más seguro en caso de que una clave falte
                dni = user_data.get("dni", "")
                nombre = user_data.get("nombre", "")
                apellido_paterno = user_data.get("apellido_paterno", "")
                apellido_materno = user_data.get("apellido_materno", "")
                rol_display = user_data.get("rol", "")
                usuario_display = user_data.get("usuario", "")
                estado_display = user_data.get("estado", "")

                # Data labels (columna por columna)
                # Use sticky="ew" for data labels to make them expand horizontally
                CTkLabel(frame_datos_tabla, text=dni, anchor="center").grid(row=row_idx, column=0, padx=2, pady=2, sticky="ew")
                CTkLabel(frame_datos_tabla, text=nombre, anchor="center").grid(row=row_idx, column=1, padx=2, pady=2, sticky="ew")
                CTkLabel(frame_datos_tabla, text=apellido_paterno, anchor="center").grid(row=row_idx, column=2, padx=2, pady=2, sticky="ew")
                CTkLabel(frame_datos_tabla, text=apellido_materno, anchor="center").grid(row=row_idx, column=3, padx=2, pady=2, sticky="ew")
                CTkLabel(frame_datos_tabla, text=rol_display, anchor="center").grid(row=row_idx, column=4, padx=2, pady=2, sticky="ew")
                CTkLabel(frame_datos_tabla, text=usuario_display, anchor="center").grid(row=row_idx, column=5, padx=2, pady=2, sticky="ew")
                CTkLabel(frame_datos_tabla, text=estado_display, anchor="center").grid(row=row_idx, column=6, padx=2, pady=2, sticky="ew")

                # Botones de Acción (Editar y Eliminar)
                CTkButton(frame_datos_tabla,
                          text="✏️",
                          width=encabezados_tabla[7]["width"],
                          fg_color="#3B8ED0",
                          hover_color="#36719F",
                          command=lambda d=dni: cargar_usuario_para_edicion(d)).grid(
                    row=row_idx, column=7, padx=2, pady=2) # No sticky="ew" for buttons if fixed width

                CTkButton(frame_datos_tabla,
                          text="⚫​",
                          width=encabezados_tabla[8]["width"],
                          fg_color="#E06E10",
                          hover_color="#D16206",
                          command=lambda d=dni: eliminar_usuario(d)).grid(
                    row=row_idx, column=8, padx=2, pady=2) # No sticky="ew" for buttons if fixed width

            frame_datos_tabla.update_idletasks()
            resize_and_center_table_frame() # Call resize after content is added

        # Initial table update
        actualizar_tabla_usuarios()

        ventana_gestion_usuarios.mainloop()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al iniciar la gestión de usuarios: {e}")
        print(f"Error in gestion_usuario: {e}")


if __name__ == "__main__":
    set_appearance_mode("dark") # Set default appearance mode (optional)
    gestion_usuario()