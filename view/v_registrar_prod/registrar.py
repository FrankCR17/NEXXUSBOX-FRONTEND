from customtkinter import *
from tkinter import messagebox
from api.api_inventario import api_registrar_prod, api_insertar_movimientos, api_obtener_ultimo_id_producto


def registrar_producto(permiso, usuario, ventana, lista_categorias, id_usuarios, actualizar_tabla):
    try:
        ventana_registrar = CTk()
        ventana_registrar.geometry("400x200")  
        ventana_registrar.title("REGISTRAR PRODUCTO")
        ancho_pantalla = ventana_registrar.winfo_screenwidth()
        alto_pantalla = ventana_registrar.winfo_screenheight()

        x_pos = int((ancho_pantalla - 400) / 2)
        y_pos = int((alto_pantalla - 200) / 2)

        ventana_registrar.geometry(f"+{x_pos}+{y_pos}")
        ventana_registrar.grab_set()  # Captura el foco y evita interacciones con otras ventanas
        ventana_registrar.focus_force()
        
        label_nombre_reg = CTkLabel(ventana_registrar, text="Nombre:")
        label_nombre_reg.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        entry_nombre_reg = CTkEntry(ventana_registrar)
        entry_nombre_reg.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        label_categoria_reg = CTkLabel(ventana_registrar, text="Categoría:")
        label_categoria_reg.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        entry_categoria_reg = CTkComboBox(ventana_registrar, values=lista_categorias)  # Llama a la función al cambiar la selección
        entry_categoria_reg.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        entry_categoria_reg.set("SELECCIONE")

        label_stock_reg = CTkLabel(ventana_registrar, text="Stock:")
        label_stock_reg.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        entry_stock_reg = CTkEntry(ventana_registrar)
        entry_stock_reg.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        entry_stock_reg.insert(0, "0")  #Valor por defecto para el stock

        #Volver a deshabilitar

        def registrar_nuevo_producto():
            try:
                if messagebox.askyesno("Registrar producto", "¿Estas seguro de hacer el registro?", parent=ventana_registrar):
                    nombre = entry_nombre_reg.get()
                    categoria = entry_categoria_reg.get()
                    stock = entry_stock_reg.get()
                    resultado = api_registrar_prod(nombre, categoria, stock, id_usuarios)
                    if resultado["status"] == 3:
                        messagebox.showinfo("ADVERTENCIA", resultado["mensaje"], parent=ventana_registrar)
                    elif resultado["status"] == 5:
                        messagebox.showinfo("ADVERTENCIA", resultado["mensaje"], parent=ventana_registrar)
                    elif resultado["status"] == 6:
                        messagebox.showinfo("ADVERTENCIA", resultado["mensaje"], parent=ventana_registrar)
                    elif resultado["status"] == 7:
                        messagebox.showinfo("ADVERTENCIA", resultado["mensaje"], parent=ventana_registrar)
                    elif resultado["status"] == 8:
                        messagebox.showinfo("ADVERTENCIA", resultado["mensaje"], parent=ventana_registrar)
                    elif resultado["status"] == 9:
                        messagebox.showinfo("ADVERTENCIA", resultado["mensaje"], parent=ventana_registrar)
                    elif resultado["status"] == 10:
                        messagebox.showinfo("ADVERTENCIA", resultado["mensaje"], parent=ventana_registrar)
                    elif resultado["status"] == 11:
                        messagebox.showinfo("ADVERTENCIA", resultado["mensaje"], parent=ventana_registrar)
                    elif resultado["status"] == 12:
                        messagebox.showinfo("ADVERTENCIA", resultado["mensaje"], parent=ventana_registrar)
                        
                    else:
                        messagebox.showinfo("Éxito", resultado["mensaje"], parent=ventana_registrar)
                        entry_nombre_reg.delete(0, 'end') 
                        entry_categoria_reg.set("SELECCIONE")
                        entry_stock_reg.delete(0, 'end') 
                        print(resultado["mensaje"])
                        ventana_registrar.destroy()
                        actualizar_tabla()
                        tipo_movimiento = 1
                        detalles = ""   
                        codigo = api_obtener_ultimo_id_producto()
                        movimiento = api_insertar_movimientos(tipo_movimiento, stock, codigo, usuario, detalles)
                        if movimiento:
                            print("Movimiento registrado correctamente")
                        ventana_registrar.focus_force() 
            except Exception as e:
                print(e)

        boton_registrar_nuevo = CTkButton(ventana_registrar, text="Registrar", command=registrar_nuevo_producto)
        boton_registrar_nuevo.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

        ventana_registrar.grid_columnconfigure(1, weight=1)
        ventana_registrar.mainloop()
    except Exception as e:
        print(e)