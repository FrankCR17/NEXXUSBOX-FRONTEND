# view/v_modificar_prod/modificar.py

from customtkinter import *
from tkinter import messagebox
# Importamos requests si lo necesitas para otras cosas, aunque no se usa directamente aquí
import requests 

# Asegúrate de que esta importación sea correcta para la nueva ventana de salida.
# La función 'abrir_ventana_salida_productos_directa' debe estar definida en ese archivo.
from view.v_modificar_prod.salida_productos import abrir_ventana_salida_productos_directa

# Asegúrate de que tus APIs estén correctamente importadas
from api.api_inventario import api_consulta_categorias, api_modificar_producto

def modificar_producto(codigo, nombre, stock, categoria, usuario, actualizar_tabla):
    """
    Abre una ventana para modificar los detalles de un producto existente.

    Args:
        codigo (str): Código único del producto.
        nombre (str): Nombre actual del producto.
        stock (int): Cantidad actual en stock del producto.
        categoria (str): Categoría actual del producto.
        actualizar_tabla (function): Función de la ventana principal para refrescar la tabla de productos.
    """
    try:
        # Crea la ventana de modificación como una ventana independiente (CTk)
        ventana_modificar = CTk()
        ventana_modificar.geometry("400x200") # Ajustado ligeramente para un mejor espacio
        ventana_modificar.title("MODIFICAR PRODUCTO")

        # Centrar ventana en la pantalla
        ancho_pantalla = ventana_modificar.winfo_screenwidth()
        alto_pantalla = ventana_modificar.winfo_screenheight()
        
        x_pos = int((ancho_pantalla - 400) / 2)
        y_pos = int((alto_pantalla - 200) / 2) # Ajustado si cambias el alto

        ventana_modificar.geometry(f"+{x_pos}+{y_pos}")
        ventana_modificar.grab_set()  # Captura el foco y evita interacciones con otras ventanas
        ventana_modificar.focus_force() # Asegura que la ventana reciba el foco

        # --- Campos de entrada para la modificación ---

        # Código (solo lectura)
        label_codigo_mod = CTkLabel(ventana_modificar, text="Código:")
        label_codigo_mod.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_codigo_mod = CTkEntry(ventana_modificar)
        entry_codigo_mod.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        entry_codigo_mod.insert(0, codigo)
        entry_codigo_mod.configure(state="readonly")

        # Nombre
        label_nombre_mod = CTkLabel(ventana_modificar, text="Nombre:")
        label_nombre_mod.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_nombre_mod = CTkEntry(ventana_modificar)
        entry_nombre_mod.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        entry_nombre_mod.insert(0, nombre)

        # Categoría (ComboBox de solo lectura)
        label_categoria_mod = CTkLabel(ventana_modificar, text="Categoría:")
        label_categoria_mod.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        lista_categorias = api_consulta_categorias() # Obtener categorías de tu API
        if not lista_categorias: # Manejo de caso si no hay categorías
            lista_categorias = ["Sin Categorías"]

        entry_categoria_mod = CTkComboBox(ventana_modificar, values=lista_categorias, state="readonly")
        entry_categoria_mod.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        # Establecer la categoría actual si existe en la lista, sino selecciona la primera
        if categoria in lista_categorias:
            entry_categoria_mod.set(categoria)
        else:
            entry_categoria_mod.set(lista_categorias[0])
            
        # Stock
        label_stock_mod = CTkLabel(ventana_modificar, text="Stock:")
        label_stock_mod.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        entry_stock_mod = CTkEntry(ventana_modificar)
        entry_stock_mod.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        entry_stock_mod.insert(0, str(stock))

        # --- Funciones de acción ---

        def guardar_modificacion():
            """Guarda los cambios del producto después de la validación."""
            if messagebox.askyesno("Modificar producto", "¿Estás seguro de hacer la modificación?", parent=ventana_modificar):
                nuevo_nombre = entry_nombre_mod.get()
                nueva_categoria = entry_categoria_mod.get()
                nuevo_stock_str = entry_stock_mod.get() # Obtener como string para validación
                
                # Validar los datos
                if not nuevo_nombre or nueva_categoria == "SELECCIONE" or not nuevo_stock_str:
                    messagebox.showerror("Error", "Por favor, complete todos los campos.", parent=ventana_modificar)
                    return
                try:
                    nuevo_stock = int(nuevo_stock_str)
                    if nuevo_stock < 0:
                        messagebox.showerror("Error", "El stock no puede ser negativo.", parent=ventana_modificar)
                        return
                except ValueError:
                    messagebox.showerror("Error", "El stock debe ser un número entero válido.", parent=ventana_modificar)
                    return
                
                # Llamar a la API para modificar el producto
                resultado = api_modificar_producto(codigo, nuevo_nombre, nueva_categoria, nuevo_stock)
                
                if resultado.get("success"): # Asumiendo que la API devuelve un diccionario con 'success'
                    messagebox.showinfo("Modificar", f"Producto modificado exitosamente: {codigo}", parent=ventana_modificar)
                    ventana_modificar.destroy() # Cierra la ventana de modificación
                    actualizar_tabla() # Refresca la tabla principal del inventario
                else:
                    messagebox.showerror(
                        "Error", 
                        f"Error al modificar el producto: {resultado.get('mensaje', 'Error desconocido')}", 
                        parent=ventana_modificar
                    )
        
        def abrir_ventana_salida_productos_wrapper():
            """
            Función wrapper para abrir la ventana de salida de productos,
            pasando los datos del producto actual.
            """
            try:
                # Intenta obtener el stock actual del campo de entrada de la ventana de modificación
                # Esto es importante si el usuario cambió el stock en esta ventana pero aún no lo guardó
                stock_actual_para_salida = int(entry_stock_mod.get())
            except ValueError:
                # Si el valor en el campo de stock no es un número válido, usa el stock original
                stock_actual_para_salida = stock
                messagebox.showwarning(
                    "Advertencia", 
                    "El stock ingresado no es válido para la salida. Usando el stock original.", 
                    parent=ventana_modificar
                )
            
            # Llama a la función de la ventana de salida, pasando los datos del producto
            # y la referencia de la ventana actual como su padre.
            abrir_ventana_salida_productos_directa(
                codigo,
                entry_nombre_mod.get(), # Usa el nombre del campo de entrada (por si se modificó)
                stock_actual_para_salida, 
                usuario,
                actualizar_tabla, # Pasa la función para actualizar la tabla principal
                ventana_modificar # Pasa la ventana de modificación como ventana padre
            )
            ventana_modificar.focus_force() # Opcional: para que la ventana de modificación recupere el foco al cerrar la de salida

        # --- Botones de acción ---
        
        boton_guardar_mod = CTkButton(ventana_modificar, text="Guardar", command=guardar_modificacion)
        boton_guardar_mod.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        boton_salida = CTkButton(
            ventana_modificar,
            text="DESPACHO DE PRODUCTOS",
            fg_color="#D03535", # Color rojo para indicar una acción de "retiro"
            hover_color="#A02A2A",
            command=abrir_ventana_salida_productos_wrapper # Llama al wrapper
        )
        boton_salida.grid(row=4, column=1, padx=10, pady=10, sticky="ew") 
        
        # --- Configuración final de la ventana ---
        ventana_modificar.grid_columnconfigure(1, weight=1) # Permite que la segunda columna se expanda

        ventana_modificar.mainloop() # Inicia el bucle de eventos de la ventana de modificación

        return True # Indica que la ventana se abrió y cerró correctamente

    except Exception as e:
        print(f"Error en modificar_producto: {e}") # Registro de errores para depuración
        messagebox.showerror("Error", f"Error al crear la ventana de modificación: {e}")
        return False # Indica que hubo un error