from customtkinter import *
from PIL import Image
from tkinter import messagebox
from customtkinter import CTkImage
from view.principal import principal
from view.login import *  
from api.api_inventario import api_login

def login():
    try:
        app = CTk()
        app.geometry("800x400")
        app.title("INVENTARIO")

        app.grid_columnconfigure(0, weight=1)
        app.grid_columnconfigure(1, weight=1)
        app.grid_rowconfigure(0, weight=1)

        left_frame = CTkFrame(app)
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_rowconfigure(6, weight=1)

        usuario_label = CTkLabel(left_frame, text="Usuario:")
        usuario_label.grid(row=1, column=0, padx=20, pady=(60, 5), sticky="ew")
        usuario_entry = CTkEntry(left_frame)
        usuario_entry.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        contrasena_label = CTkLabel(left_frame, text="Contraseña")
        contrasena_label.grid(row=3, column=0, padx=20, pady=(0, 5), sticky="ew")
        contrasena_entry = CTkEntry(left_frame, show="*")
        contrasena_entry.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")

        def verificar_credenciales():
            usuario = usuario_entry.get()
            contrasena = contrasena_entry.get()
            resultado = api_login(usuario, contrasena)
            if resultado['status'] == 1:
                permiso = resultado['permiso']
                return True, permiso, usuario
            elif resultado['status'] == 2:
                messagebox.showerror('Error',resultado['mensaje'])
                #usuario_entry.delete(0, 'end')  
                contrasena_entry.delete(0, 'end')
                permiso = " "
                return False, permiso, usuario
            elif resultado['status'] == 3:
                messagebox.showerror('Error',resultado['mensaje'])
                usuario_entry.delete(0, 'end')  
                contrasena_entry.delete(0, 'end')
                permiso = " "
                return False, permiso, usuario
            elif resultado['status'] == 4:
                messagebox.showerror('Error',resultado['mensaje'])
                usuario_entry.delete(0, 'end')  
                contrasena_entry.delete(0, 'end')
                permiso = " "
                return False, permiso, usuario

        def iniciar_sesion(event=None):
            verif_cred, permiso, usuario = verificar_credenciales()
            if verif_cred == True:
                app.destroy()
                principal(permiso, usuario)

        login_button = CTkButton(left_frame, text="Iniciar Sesion", command=iniciar_sesion)
        login_button.grid(row=5, column=0, padx=20, pady=(15, 60), sticky="ew")

        usuario_entry.bind('<Return>', iniciar_sesion)
        contrasena_entry.bind('<Return>', iniciar_sesion)

        right_frame = CTkFrame(app, fg_color="white")
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=1)

        try:
            image = Image.open("img/fondo_login.png")
            resized_image = image.resize((350, 350))
            photo = CTkImage(resized_image, size=(350, 350)) 
            image_label = CTkLabel(right_frame, image=photo, text="")
            image_label.place(relx=0.5, rely=0.5, anchor="center")
        except FileNotFoundError:
            error_label = CTkLabel(right_frame, text="Imagen no encontrada")
            error_label.place(relx=0.5, rely=0.5, anchor="center")

        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()
        window_width = 800
        window_height = 400
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        app.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        app.mainloop()
        return True
    except Exception as e:
        print(f"Ocurrió un error al crear la ventana de login: {e}")
        return False