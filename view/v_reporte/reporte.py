from customtkinter import *
from tkinter import messagebox
import tkinter as tk
from tkcalendar import Calendar
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime, timedelta
from api.api_inventario import api_listar_movimientos

# --- Simulaciones de API (PLACEHOLDER - DEBES REEMPLAZAR CON TU API REAL) ---
# Esta lista simula los movimientos de productos en tu base de datos.
# Cada diccionario representa un movimiento.

def mostrar_calendario(entry_widget, string_var_to_update):
    """
    Muestra un calendario para seleccionar una fecha y la inserta en la StringVar asociada
    y también actualiza el contenido del CTkEntry directamente.
    """
    top = tk.Toplevel(entry_widget.master)
    cal = Calendar(top, selectmode='day',
                        firstweekday='monday',
                        showweeknumbers=False,
                        date_pattern='yyyy-mm-dd')
    cal.pack(padx=10, pady=10)

    def seleccionar_y_cerrar():
        fecha_seleccionada = cal.get_date()
        string_var_to_update.set(fecha_seleccionada) # Actualiza la StringVar
        entry_widget.delete(0, END) # Limpia el entry
        entry_widget.insert(0, fecha_seleccionada) # Inserta la fecha en el entry
        top.destroy()

    boton_seleccionar = CTkButton(top, text="Seleccionar", command=seleccionar_y_cerrar)
    boton_seleccionar.pack(pady=5)

def generar_reportes_ventana():
    """
    Crea y muestra la ventana para generar reportes de movimientos de productos.
    """
    ventana_reportes = CTk()
    ventana_reportes.geometry("700x500")
    ventana_reportes.title("Generar Reportes de Movimientos")
    ventana_reportes.resizable(width=False, height=False)

    # Centrar la ventana en la pantalla
    ancho_pantalla = ventana_reportes.winfo_screenwidth()
    alto_pantalla = ventana_reportes.winfo_screenheight()

    x_pos = int((ancho_pantalla - 700) / 2)
    y_pos = int((alto_pantalla - 500) / 2)

    ventana_reportes.geometry(f"+{x_pos}+{y_pos}")
    ventana_reportes.grab_set()  # Captura el foco y evita interacciones con otras ventanas
    ventana_reportes.focus_force()

    frame_controles = CTkFrame(ventana_reportes, fg_color="#343434")
    frame_controles.pack(pady=20, padx=20, fill="x")

    # Variables de control para los widgets
    report_type_var = tk.StringVar(value="mensual") # Por defecto: reporte mensual
    month_var = tk.StringVar(value=str(datetime.now().month)) # Mes actual
    year_var = tk.StringVar(value=str(datetime.now().year)) # Año actual
    start_date_var = tk.StringVar(value="")
    end_date_var = tk.StringVar(value="")

    # Radio buttons para seleccionar el tipo de reporte
    radio_mensual = CTkRadioButton(frame_controles, text="Reporte Mensual",
                                   variable=report_type_var, value="mensual",
                                   command=lambda: toggle_date_inputs("mensual"))
    radio_mensual.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    radio_semanal = CTkRadioButton(frame_controles, text="Reporte Semanal",
                                   variable=report_type_var, value="semanal",
                                   command=lambda: toggle_date_inputs("semanal"))
    radio_semanal.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # Controles para entrada mensual (inicialmente visibles)
    label_mes = CTkLabel(frame_controles, text="Mes:")
    combo_mes = CTkComboBox(frame_controles, values=[str(i) for i in range(1, 13)],
                            variable=month_var, state="readonly")

    label_anio = CTkLabel(frame_controles, text="Año:")
    entry_anio = CTkEntry(frame_controles, textvariable=year_var)

    # Controles para entrada semanal (inicialmente ocultos)
    label_fecha_inicio = CTkLabel(frame_controles, text="Fecha Inicio:")
    entry_fecha_inicio = CTkEntry(frame_controles, textvariable=start_date_var)
    # Pasa la StringVar al comando del botón del calendario
    btn_cal_inicio = CTkButton(frame_controles, text="📅", width=25, command=lambda: mostrar_calendario(entry_fecha_inicio, start_date_var))

    label_fecha_fin = CTkLabel(frame_controles, text="Fecha Fin:")
    entry_fecha_fin = CTkEntry(frame_controles, textvariable=end_date_var)
    # Pasa la StringVar al comando del botón del calendario
    btn_cal_fin = CTkButton(frame_controles, text="📅", width=25, command=lambda: mostrar_calendario(entry_fecha_fin, end_date_var))

    def toggle_date_inputs(report_type):
        """
        Alterna la visibilidad de los campos de fecha según el tipo de reporte.
        """
        if report_type == "mensual":
            # Mostrar controles mensuales
            label_mes.grid(row=1, column=0, padx=10, pady=5, sticky="w")
            combo_mes.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
            label_anio.grid(row=2, column=0, padx=10, pady=5, sticky="w")
            entry_anio.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

            # Ocultar controles semanales
            label_fecha_inicio.grid_forget()
            entry_fecha_inicio.grid_forget()
            btn_cal_inicio.grid_forget()
            label_fecha_fin.grid_forget()
            entry_fecha_fin.grid_forget()
            btn_cal_fin.grid_forget()
        else: # semanal
            # Ocultar controles mensuales
            label_mes.grid_forget()
            combo_mes.grid_forget()
            label_anio.grid_forget()
            entry_anio.grid_forget()

            # Mostrar controles semanales
            label_fecha_inicio.grid(row=1, column=0, padx=10, pady=5, sticky="w")
            entry_fecha_inicio.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
            btn_cal_inicio.grid(row=1, column=2, padx=2, pady=5, sticky="w")
            label_fecha_fin.grid(row=2, column=0, padx=10, pady=5, sticky="w")
            entry_fecha_fin.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
            btn_cal_fin.grid(row=2, column=2, padx=2, pady=5, sticky="w")
    
    # Inicializar la visibilidad de los campos de entrada según el tipo de reporte por defecto
    toggle_date_inputs(report_type_var.get())

    def get_report_dates():
        """
        Obtiene el rango de fechas para el reporte según el tipo seleccionado.
        Valida las entradas del usuario.
        """
        current_type = report_type_var.get()
        if current_type == "mensual":
            try:
                month = int(month_var.get())
                year = int(year_var.get())
                if not (1 <= month <= 12 and 1900 <= year <= 2100): # Rango de años básico
                    messagebox.showerror("Error de Fecha", "Mes o año inválido.", parent=ventana_reportes)
                    return None, None
                
                # Calcular la fecha de inicio y fin del mes
                start_date = datetime(year, month, 1)
                if month == 12:
                    end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
                else:
                    end_date = datetime(year, month + 1, 1) - timedelta(days=1)
                return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error de Fecha", "Por favor, ingrese un mes y año válidos.", parent=ventana_reportes)
                return None, None
        else: # semanal
            start_date_str = start_date_var.get()
            end_date_str = end_date_var.get()
            # print(f"DEBUG: start_date_str = '{start_date_str}', end_date_str = '{end_date_str}'") # Debug print
            if not start_date_str or not end_date_str:
                messagebox.showerror("Error de Fecha", "Por favor, seleccione las fechas de inicio y fin.", parent=ventana_reportes)
                return None, None
            try:
                # Validación básica del formato de fecha (YYYY-MM-DD)
                parsed_start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                parsed_end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                # print(f"DEBUG: Parsed start_date = {parsed_start_date}, parsed_end_date = {parsed_end_date}") # Debug print
                return start_date_str, end_date_str
            except ValueError as ve: # Captura el error específico para dar un mensaje más útil
                messagebox.showerror("Error de Fecha", f"Formato de fecha inválido. Use YYYY-MM-DD. Error: {ve}", parent=ventana_reportes)
                return None, None

    def generate_report_data():
        """
        Obtiene los datos de movimientos de la API para el período seleccionado.
        """
        fecha_inicio, fecha_fin = get_report_dates()
        if not fecha_inicio or not fecha_fin:
            return None, None, None

        response = api_listar_movimientos(fecha_inicio, fecha_fin)
        
        print(response[0])
        print(response[1])
        mensaje = response[0]
        flitro = response[1]
        if mensaje["status"] == 1:
            return flitro, fecha_inicio, fecha_fin
        else:
            messagebox.showerror("Error API", response["mensaje"], parent=ventana_reportes)
            return None, None, None

    def save_report_as_pdf():
        """
        Genera y guarda el reporte de movimientos como un archivo PDF.
        """
        report_data, fecha_inicio, fecha_fin = generate_report_data()
        if report_data is None:
            return

        if not report_data:
            messagebox.showinfo("Reporte Vacío", "No hay movimientos para el período seleccionado.", parent=ventana_reportes)
            return

        report_folder = "reportes" 
        try:
            os.makedirs(report_folder, exist_ok=True)
        except OSError as e:
            messagebox.showerror("Error de Carpeta", f"No se pudo crear la carpeta '{report_folder}': {e}", parent=ventana_reportes)
            return

        file_name_base  = f"Reporte_Movimientos_{fecha_inicio}_a_{fecha_fin}.pdf"
        file_path = os.path.join(report_folder, file_name_base)
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Título del reporte
        title_text = f"Reporte de Movimientos de Productos"
        story.append(Paragraph(title_text, styles['h1']))
        story.append(Spacer(1, 0.2 * inch))

        # Rango de fechas del reporte
        date_range_text = f"Período: del {fecha_inicio} al {fecha_fin}"
        story.append(Paragraph(date_range_text, styles['h2']))
        story.append(Spacer(1, 0.2 * inch))

        # Tabla de datos
        data = [["Fecha y Hora", "Tipo", "Cantidad", "Producto", "Usuario", "Observación"]] # Encabezados de la tabla
        for mov in report_data:
            data.append([
                mov["fecha_hora"],
                mov["tipo_movimiento"],
                str(mov["cantidad"]),
                mov["producto"],
                mov["usuario"],
                mov["observacion"]
            ])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2A8C55")), # Fondo del encabezado
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), # Color del texto del encabezado
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'), # Alineación del texto
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), # Fuente del encabezado
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12), # Relleno inferior del encabezado
            ('BACKGROUND', (0, 1), (-1, -1), colors.white), # Fondo del cuerpo de la tabla (cambiado a blanco)
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black), # Color del texto del cuerpo (cambiado a negro)
            ('GRID', (0, 0), (-1, -1), 1, colors.black), # Bordes de la tabla
            ('BOX', (0, 0), (-1, -1), 1, colors.black), # Borde exterior de la tabla
        ]))
        story.append(table)

        try:
            doc.build(story)
            messagebox.showinfo("PDF Generado", f"Reporte guardado como {file_path}", parent=ventana_reportes)
        except Exception as e:
            messagebox.showerror("Error al Generar PDF", f"No se pudo generar el PDF: {e}", parent=ventana_reportes)

    # Botones de acción
    btn_generate_pdf = CTkButton(frame_controles, text="Guardar Reporte como PDF", command=save_report_as_pdf)
    btn_generate_pdf.grid(row=3, column=0, columnspan=3, pady=10)

    ventana_reportes.mainloop()


if __name__ == "__main__":
    generar_reportes_ventana()
