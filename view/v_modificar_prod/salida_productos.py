from customtkinter import *
from tkinter import messagebox
from api.api_inventario import api_consultar_tipo_movimientos, api_insertar_movimientos

def abrir_ventana_salida_productos_directa(codigo, nombre, stock_actual, usuario, actualizar_tabla_inventario_principal, parent_window):
    ventana_salida = CTkToplevel(parent_window) 
    ventana_salida.title(f"REGISTRAR DESPACHO: {nombre}")
    
    ventana_salida.geometry("400x280") 
    
    
    ancho_pantalla = ventana_salida.winfo_screenwidth()
    alto_pantalla = ventana_salida.winfo_screenheight()
    
    y_pos = int((alto_pantalla - 280) / 2) 
    x_pos = int((ancho_pantalla - 400) / 2)
    ventana_salida.geometry(f"+{x_pos}+{y_pos}")

    ventana_salida.grab_set()
    ventana_salida.focus_force()

    CTkLabel(ventana_salida, text="Código:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_codigo_display = CTkEntry(ventana_salida) 
    entry_codigo_display.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    
    entry_codigo_display.configure(state="normal")
    entry_codigo_display.insert(0, str(codigo))
    entry_codigo_display.configure(state="readonly")

    CTkLabel(ventana_salida, text="Nombre:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_nombre_display = CTkEntry(ventana_salida) 
    entry_nombre_display.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    entry_nombre_display.configure(state="normal")
    entry_nombre_display.insert(0, str(nombre))
    entry_nombre_display.configure(state="readonly")

    CTkLabel(ventana_salida, text="Stock Actual:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_stock_actual_display = CTkEntry(ventana_salida) 
    entry_stock_actual_display.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
    entry_stock_actual_display.configure(state="normal")
    entry_stock_actual_display.insert(0, str(stock_actual))
    entry_stock_actual_display.configure(state="readonly")


    CTkLabel(ventana_salida, text="Cantidad a Retirar:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_cantidad_retirar = CTkEntry(ventana_salida)
    entry_cantidad_retirar.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    # --- Reason for Output ---
    CTkLabel(ventana_salida, text="Motivo:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    opciones_motivo = api_consultar_tipo_movimientos()
    combobox_motivo = CTkComboBox(ventana_salida, values=opciones_motivo, state="readonly")
    combobox_motivo.set(opciones_motivo[0])
    combobox_motivo.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    # --- Detalles (Nuevo Campo) ---
    CTkLabel(ventana_salida, text="Detalles:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    entry_detalles = CTkEntry(ventana_salida)
    entry_detalles.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

    def confirmar_salida():
        cantidad_str = entry_cantidad_retirar.get()
        motivo = combobox_motivo.get()
        detalles = entry_detalles.get() # Obtener el valor del nuevo campo de detalles

        if not cantidad_str:
            messagebox.showerror("Error", "Por favor, ingrese la cantidad a retirar.", parent=ventana_salida)
            return

        try:
            cantidad_a_retirar = int(cantidad_str)
            if cantidad_a_retirar <= 0:
                messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.", parent=ventana_salida)
                return
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero válido.", parent=ventana_salida)
            return

        if cantidad_a_retirar > stock_actual:
            messagebox.showerror("Error", f"No hay suficiente stock. Disponible: {stock_actual} unidades.", parent=ventana_salida)
            return
        
        # Incluir los detalles en el mensaje de confirmación
        confirm_message = (
            f"¿Confirma la salida de {cantidad_a_retirar} unidades de '{nombre}' (código: {codigo}) "
            f"por motivo: '{motivo}'?"
        )
        if detalles: # Si hay detalles, agrégalos al mensaje
            confirm_message += f"\nDetalles: '{detalles}'"

        if messagebox.askyesno("Confirmar Salida", confirm_message, parent=ventana_salida):
            resultado = api_insertar_movimientos(motivo, cantidad_a_retirar, codigo, usuario, detalles)
        
            if resultado.get("status") == 1:
                messagebox.showinfo("Éxito", f"Salida de {cantidad_a_retirar} unidades de '{nombre}' registrada", parent=ventana_salida)
                ventana_salida.destroy()
                actualizar_tabla_inventario_principal() 
            else:
                messagebox.showerror("Error", "Error desconocido al registrar salida (simulado).", parent=ventana_salida)
            # --- End of simulation ---

    # --- Action Buttons ---
    # Ajustadas las filas de los botones
    btn_confirmar = CTkButton(ventana_salida, text="Confirmar Salida", command=confirmar_salida, fg_color="green", hover_color="darkgreen")
    btn_confirmar.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

    btn_cancelar = CTkButton(ventana_salida, text="Cancelar", command=ventana_salida.destroy, fg_color="gray", hover_color="dimgray")
    btn_cancelar.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

    ventana_salida.grid_columnconfigure(1, weight=1) 
    ventana_salida.grid_columnconfigure(0, weight=1)
    # Do not use ventana_salida.mainloop() here for a CTkToplevel window.