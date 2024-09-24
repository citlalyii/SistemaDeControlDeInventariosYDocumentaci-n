import tkinter as tk
from tkinter import ttk, messagebox
from colorsNissan import PRINCIPAL_BODY,BARRA_SUPERIOR
from forms.pdf import solicitud,toner
from PIL import Image, ImageDraw
import sqlite3
import io
import random
from PIL import Image, ImageTk
import util.imagenes_util as u_img
import datetime
#Clase principal
class inventToner():

    def __init__(self, username):
        super().__init__()
        self.username = username

    def crear_tabla(self, parent_frame):
        #Opciones de busqueda de registros
        marco=tk.Frame(parent_frame, background=BARRA_SUPERIOR)
        marco.pack(fill='x', expand=0)

        self.labelTitle = tk.Label(marco, text="Consumibles",font=("Poppins-ExtraLight",15),fg="white" ,background=BARRA_SUPERIOR,width=16, anchor="w", padx=10)
        self.labelTitle.grid(row=1, column=0, sticky="w") 
        
        self.entry_buscar = tk.Entry(marco)
        self.entry_buscar.grid(row=1, column=1, padx=10 , sticky="ew")

        self.search_icon_label = tk.Label(marco, text="\uf002",fg="white" ,font=("Font Awesome 5 Free", 14), background=BARRA_SUPERIOR)
        self.search_icon_label.grid(row=1, column=2, sticky="e", padx=10)
        
        marco.columnconfigure(1, weight=1)

        #Formulario principal
        marco2=tk.Frame(parent_frame, background=PRINCIPAL_BODY)
        marco2.pack(expand=0,fill="x", padx=5, pady=5)
    
        self.label_cantidad = tk.Label(marco2, text="Cantidad:", anchor="w",font=("Poppins", 14))
        self.entry_cantidad = tk.Entry(marco2)

        self.label_tipo = tk.Label(marco2, text="Tipo:", anchor="w",font=("Poppins", 14))
        self.combo_tipo = ttk.Combobox(marco2)
        self.actualizar_combobox_tipo()
        
        self.label_modelo = tk.Label(marco2, text="Modelo:", anchor="w",font=("Poppins", 14))
        self.combo_modelo = ttk.Combobox(marco2)
        self.actualizar_combobox_modelo()

        self.label_color = tk.Label(marco2, text="Color:", anchor="w",font=("Poppins", 14))
        self.combo_color = ttk.Combobox(marco2)
        self.actualizar_combobox_color()

        self.label_cantidad.grid(padx=10, pady=5, sticky="we", row=0)
        self.entry_cantidad.grid(row=1, column=0,  pady=5, padx=10, sticky="we")

        self.label_tipo.grid(padx=10, pady=5, sticky="we",row=0, column=1)
        self.combo_tipo.grid(row=1, column=1,  pady=5, padx=30, sticky="we")
        self.plus1 = tk.Label(marco2, text="+",fg="white" ,font=("Font Awesome 5 Free", 12), background=BARRA_SUPERIOR)
        self.plus1.grid(row=1, column=1,sticky="e",padx=10)
        
        self.label_modelo.grid(padx=10, pady=5, sticky="we", row=0, column=3)
        self.combo_modelo.grid(row=1, column=3, pady=5, padx=30, sticky="we")
        self.plus2 = tk.Label(marco2, text="+",fg="white" ,font=("Font Awesome 5 Free", 12), background=BARRA_SUPERIOR)
        self.plus2.grid(row=1, column=3, sticky="e",padx=10)

        self.label_color.grid(padx=10, pady=5, sticky="we", row=0, column=5)
        self.combo_color.grid(row=1, column=5, pady=5, padx=30, sticky="we")
        self.plus3 = tk.Label(marco2,text="+",fg="white" ,font=("Font Awesome 5 Free", 12), background=BARRA_SUPERIOR)
        self.plus3.grid(row=1, column=5, sticky="e",padx=10)

        marco2.columnconfigure(0, weight=1)
        marco2.columnconfigure(1, weight=1)
        marco2.columnconfigure(3, weight=1)
        marco2.columnconfigure(5, weight=1)

        #Botones principales.
        marco3=tk.Frame(parent_frame)
        marco3.pack(expand=0, fill="x",  pady=10)

        self.btn_registrar = tk.Button(marco3, text="Registrar",font=("Poppins-ExraLight", 12),bg=BARRA_SUPERIOR ,command=self.registrar_activo)
        self.btn_modificar = tk.Button(marco3, text="Modificar" ,font=("Poppins-ExtraLight", 12), bg=BARRA_SUPERIOR, command=self.modificar_activo)
        self.btn_imprimir = tk.Button(marco3, text="Descargar" ,font=("Poppins-ExtraLight", 12), bg=BARRA_SUPERIOR, command= self.pdf)
        
        self.btn_registrar.pack(side="right", padx=20, pady=5)
        self.btn_modificar.pack(side="right", padx=20, pady=5)
        self.btn_imprimir.pack(side="right", padx=20, pady=5)

        self.btn_registrar.config(fg="#fff", width=15, height=1)
        self.btn_modificar.config(fg="#fff", width=15, height=1)
        self.btn_imprimir.config(fg="#fff", width=15, height=1)

        style = ttk.Style()
        style.configure("Treeview",
                foreground="#000",
                cellpadding=19,
                font=("Poppins", 10))

        style.configure("Treeview.Heading",
                font=("Poppins", 15, "bold"),
                foreground="#000",
                background="#7A7A7A")
        
        style.map('Treeview',
                  background=[('selected','#7A7A7A')],foreground=[('selected','white')])

        tabla=tk.Frame(parent_frame, background=PRINCIPAL_BODY)
        tabla.pack(fill="both" ,expand=1, padx=10, side="left")

        titulo_label2 = tk.Label(tabla, text="Stock", font=("Helvetica", 16), background=PRINCIPAL_BODY)
        titulo_label2.pack(fill="x", padx=10, pady=(10, 0),side="top")
        
        #Encabezados de la tabla.
        self.tree1 = ttk.Treeview(tabla ,columns=("#", "cant","tipo","mod","col","print", "trash"), show="headings")
        
        self.tree1.heading("#", text="#")
        self.tree1.heading("cant", text="Cantidad")
        self.tree1.heading("tipo", text="Tipo")
        self.tree1.heading("mod", text="Modelo")
        self.tree1.heading("col", text="Color")
        self.tree1.heading("print")
        self.tree1.heading("trash")
       
        for column in self.tree1['columns']:
            self.tree1.column(column, width=50,  anchor="center")
        self.tree1.pack(fill="both", expand=1, padx=10, pady=10) 
        self.limpiar_tabla()

        self.search_icon_label.bind("<Button-1>", self.search)
        self.plus1.bind("<Button-1>", self.agregar_opcion1)
        self.plus2.bind("<Button-1>", self.agregar_opcion2)
        self.plus3.bind("<Button-1>", self.agregar_opcion3)
        self.tree1.bind("<<TreeviewSelect>>", self.fila_sel)#Acción para seleccionar un registro.
        self.tree1.bind("<ButtonRelease-1>", self.item_click)#Acción al hacer click en un icono dentro de la tabla.

        tabla2=tk.Frame(parent_frame, background=PRINCIPAL_BODY)
        tabla2.pack(fill="both" ,expand=1, padx=10,side="right")
        
        titulo_label2 = tk.Label(tabla2, text="Salidas", font=("Helvetica", 16), background=PRINCIPAL_BODY)
        titulo_label2.pack(fill="x", padx=10, pady=(10, 0),side="top")

        self.salida = ttk.Treeview(tabla2 ,columns=("idS","nombre","producto","fecha","trash","ver"), show="headings")
        
        self.salida.heading("idS", text="#")
        self.salida.heading("nombre", text="Nombre")
        self.salida.heading("producto", text="Producto")
        self.salida.heading("fecha", text="Fecha")
        self.salida.heading("trash", text="")
        self.salida.heading("ver", text="")
       
        for column in self.salida['columns']:
            self.salida.column(column, width=50,  anchor="center")
        self.salida.pack(fill="both", expand=1, padx=10, pady=10) 
        self.limpiar_tablaSalidas()
        self.salida.bind("<ButtonRelease-1>", self.item_click2)

    def combobox_modelo(self):
        conn = sqlite3.connect('scrnissan.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM toner_modelo")
        rows = cursor.fetchall()
        modelos = [row[0] for row in rows]
        conn.close()
        return modelos
    
    def combobox_tipo(self):
        conn = sqlite3.connect('scrnissan.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM toner_tipo")
        rows = cursor.fetchall()
        tipo = [row[0] for row in rows] 
        conn.close() 
        return tipo
    
    def combobox_color(self):
        conn = sqlite3.connect('scrnissan.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM toner_color")
        rows = cursor.fetchall()
        color = [row[0] for row in rows]
        conn.close()
        return color
    
    def agregar_opcion2(self, event=None):
        nueva_opcion = self.combo_modelo.get()
        if nueva_opcion:
            conexion = sqlite3.connect('scrnissan.db')
            cursor = conexion.cursor()
            cursor.execute(f"INSERT INTO toner_modelo (nombre) VALUES (?)", (nueva_opcion,))
            conexion.commit()
            conexion.close()
            self.actualizar_combobox_modelo()
            self.combo_modelo.set("")

    def agregar_opcion1(self, event=None):
        nueva_opcion = self.combo_tipo.get()
        if nueva_opcion:
            conexion = sqlite3.connect('scrnissan.db')
            cursor = conexion.cursor()
            cursor.execute(f"INSERT INTO toner_tipo (nombre) VALUES (?)", (nueva_opcion,))
            conexion.commit()
            conexion.close()
            self.actualizar_combobox_tipo()
            self.combo_tipo.set("")

    def agregar_opcion3(self, event=None):
        nueva_opcion = self.combo_color.get()
        if nueva_opcion:
            conexion = sqlite3.connect('scrnissan.db')
            cursor = conexion.cursor()
            cursor.execute(f"INSERT INTO toner_color (nombre) VALUES (?)", (nueva_opcion,))
            conexion.commit()
            conexion.close()
            self.actualizar_combobox_color()
            self.combo_color.set("")
    
    def actualizar_combobox_color(self):
        self.combo_color['values'] = self.combobox_color()

    def actualizar_combobox_tipo(self):
        self.combo_tipo['values'] = self.combobox_tipo()

    def actualizar_combobox_modelo(self):
        self.combo_modelo['values'] = self.combobox_modelo()

    def fila_sel(self, event):
        selection = self.tree1.focus()
        values = self.tree1.item(selection, "values")
        
        if values and len(values) > 0:
            self.limpiar_campos()
            self.entry_cantidad.insert(0, values[1])
            self.combo_tipo.insert(0, values[2])
            self.combo_modelo.insert(0, values[3])
            self.combo_color.insert(0, values[4])
        else:
            return
    
    def item_click(self, event):
        #Funcion al seleccionar el icono de eliminar.
        item = self.tree1.selection()[0]
        column = self.tree1.identify_column(event.x)
        if column == "#7":   
            self.eliminar_activo(item)
        elif column == "#6":   
            self.popup(item)
        else:
            return
    
    def item_click2(self, event):
        #Funcion al seleccionar el icono de eliminar.
        item = self.salida.selection()[0]
        column = self.salida.identify_column(event.x)
        if column == "#5":   
            self.eliminar2(item)
        elif column == "#6":
            self.ver_imagen(item)
        else:
            return
    
    def eliminar2(self, item):
        confirmacion = messagebox.askyesno("Eliminar", "¿Seguro que deseas eliminar este registro?")
        if confirmacion:
            try:
                id_ton = self.salida.item(item, "values")[0]
                conexion = sqlite3.connect('scrnissan.db')
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM salida_toner WHERE idsalida = ?", (id_ton,))
                conexion.commit()
                cursor.close()            
                self.limpiar_tablaSalidas()
            except Exception:
                messagebox.showerror("Error", "Ocurrio un error al eliminar el dato.")
        else:
            return
        
    def modificar_activo(self):
        if not self.tree1.selection():
            messagebox.showwarning("Advertencia", "Primero debes seleccionar un registro.")
            return
        
        confirmacion = messagebox.askyesno("Modificar", "¿Seguro que deseas modificar este registro?")
        if confirmacion: 
            selected_item = self.tree1.selection()[0]
            idtoner = self.tree1.item(selected_item, "values")[0]
            cantidad = self.entry_cantidad.get()
            tipo = self.combo_tipo.get()
            modelo = self.combo_modelo.get()
            color = self.combo_color.get()

            if cantidad.isdigit():
                conexion = sqlite3.connect('scrnissan.db')
                cursor = conexion.cursor() 
                query = "UPDATE toner SET cantidad=?, tipo=?, modelo=?,color=? WHERE idtoner=?"
                cursor.execute(query, (cantidad,tipo,modelo,color,idtoner))
                conexion.commit()

                self.limpiar_tabla()
                self.limpiar_campos()
            else:
                messagebox.showwarning("Advertencia", "La cantidad debe ser numérica.")
                
    def eliminar_activo(self, item):
        confirmacion = messagebox.askyesno("Eliminar", "¿Seguro que deseas eliminar este registro?")
        if confirmacion: 
            try:
                id_ton =self.tree1.item(item, "values")[0]
                conexion = sqlite3.connect('scrnissan.db')
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM toner WHERE idtoner = ?", (id_ton,))
                conexion.commit()
                cursor.close()
                self.limpiar_tabla()
                self.limpiar_campos()
            except Exception:
                messagebox.showerror("Error", "Ocurrio un error al eliminar el dato.")
        else:
            return

    def registrar_activo(self):
        #Funcion para registrar un equipo.
        if (not self.entry_cantidad.get() or
            not self.combo_tipo.get() or
            not self.combo_modelo.get() or
            not self.combo_color.get()):
            messagebox.showwarning("Advertencia","Completa todos los campos del formulario.")
            return
        confirmacion = messagebox.askyesno("Registrar", "¿Seguro que deseas ingresar un registro a la tabla?")
        if confirmacion:
            cantidad = self.entry_cantidad.get()
            tipo = self.combo_tipo.get()
            modelo = self.combo_modelo.get()
            color = self.combo_color.get()

            if cantidad.isdigit():
                conexion = sqlite3.connect('scrnissan.db')
                cursor = conexion.cursor()
                query = "INSERT INTO toner (cantidad,tipo,modelo,color) VALUES (?, ?, ?, ?)"
                datos = (cantidad,tipo,modelo,color)
                cursor.execute(query, datos)
                conexion.commit()
                conexion.close()
                self.limpiar_campos()
                self.limpiar_tabla()
            else:
                messagebox.showwarning("Advertencia", "La cantidad debe ser numérica.")
    
    def popup(self,item):
        id_ton = self.tree1.item(item, "values")[0]
        conexion = sqlite3.connect('scrnissan.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT cantidad FROM toner WHERE idtoner = ?", (id_ton,))
        cantidad = cursor.fetchone()[0]

        if cantidad > 0:
            ventana_flotante = tk.Toplevel()
            ventana_flotante.title("Solicitud de Consumibles")
            ventana_flotante.resizable(False, False)

            label_seleccion = tk.Label(ventana_flotante, text="Completa la siguiente información", font=("Poppins-ExtraLight", 15))
            label_seleccion.pack(pady=5, padx=5, anchor="w")

            label_nom = tk.Label(ventana_flotante, text="Nombre del solicitante:", font=("Poppins-ExtraLight", 12))
            label_nom.pack(padx=5, pady=5, anchor="w")

            entry_nom = tk.Entry(ventana_flotante)
            entry_nom.pack(padx=10, pady=5, expand=True, fill="x")

            label_area = tk.Label(ventana_flotante, text="Área de trabajo:", font=("Poppins-ExtraLight", 12))
            label_area.pack(padx=5, pady=5, anchor="w")

            entry_area = tk.Entry(ventana_flotante)
            entry_area.pack(padx=10, pady=5, expand=True, fill="x")

            marcoFirma = tk.Frame(ventana_flotante)
            marcoFirma.pack(fill="both", expand=1, padx=10, side="left")

            boton_limpiar = tk.Button(marcoFirma, width=10, text="Limpiar", bg=BARRA_SUPERIOR, fg="white", command=lambda: self.limpiar_firma(canvas_f))
            boton_limpiar.pack(anchor="w")

            canvas_f = tk.Canvas(marcoFirma, width=400, height=200, bg='white')
            canvas_f.pack(pady=5)
            self.dibujar_firma(canvas_f)

            label_firma1 = tk.Label(marcoFirma, text="Firma quien recibe.", font=("Poppins-ExtraLight", 12))
            label_firma1.pack(pady=5, anchor="center")

            marcoFirma2 = tk.Frame(ventana_flotante)
            marcoFirma2.pack(fill="both", expand=1, padx=10, side="right")

            boton_limpiar2 = tk.Button(marcoFirma2, width=10, text="Limpiar", bg=BARRA_SUPERIOR, fg="white", command=lambda: self.limpiar_firma(canvas_f2))
            boton_limpiar2.pack(anchor="e")

            canvas_f2 = tk.Canvas(marcoFirma2, width=400, height=200, bg='white')
            canvas_f2.pack(pady=5)
            self.dibujar_firma(canvas_f2)

            label_firma2 = tk.Label(marcoFirma2, text="Firma quien autoriza.", font=("Poppins-ExtraLight", 12))
            label_firma2.pack(pady=5, anchor="center")

            botones=tk.Frame(marcoFirma2)
            botones.pack(fill="both", expand=1, padx=10, side="bottom")

            boton_imprimir = tk.Button(botones, width=20, text="Imprimir", bg=BARRA_SUPERIOR, fg="white", command=lambda: self.ticket(entry_nom.get(), entry_area.get(), item, ventana_flotante, canvas_f, canvas_f2))
            boton_imprimir.pack(pady=5,padx=10 ,anchor="e", side="right")

            boton_omitir = tk.Button(botones, width=20, text="Omitir", bg=BARRA_SUPERIOR, fg="white", command=lambda: self.omitir_firma(entry_nom.get(), entry_area.get(), item, ventana_flotante))
            boton_omitir.pack(pady=5,padx=10 ,anchor="e",side="right")

        else:
            messagebox.showwarning("Advertencia", "Ya no tienes este producto en Stock.")

    def dibujar_firma(self, canvas):
        self.old_x = None
        self.old_y = None
        self.line_width = 2
        self.color = "black"

        def paint(event):
            if self.old_x and self.old_y:
                canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=self.line_width, fill=self.color, capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36)
            self.old_x = event.x
            self.old_y = event.y

        def reset(event):
            self.old_x, self.old_y = None, None

        canvas.bind('<B1-Motion>', paint)
        canvas.bind('<ButtonRelease-1>', reset)

    def limpiar_firma(self, canvas):
        canvas.delete("all")
    
    def valida_firma(self, canvas):
    # Verifica si el canvas contiene alguna firma
        return len(canvas.find_all()) > 0
    
    def omitir_firma(self, nombre, area, item, ventana_flotante):
        if not nombre or not area: 
            messagebox.showwarning("Advertencia", "Ingresa el Nombre y Área del solicitante.")
            return
        
        ruta_firma = "./imgs/fondo.png"
        firma_bytes = self.leer_imagen(ruta_firma)
        firma_bytes2 = self.leer_imagen(ruta_firma)

        fecha = datetime.datetime.now()
        fechaSi = fecha.strftime("%Y/%m/%d")
        hora = fecha.strftime("%H:%M %p")
        folio = ''.join(map(str, [random.randint(1, 10) for _ in range(5)]))
        id_act = self.tree1.item(item, "values")[0]
        conexion = sqlite3.connect('scrnissan.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT modelo, cantidad FROM toner WHERE idtoner = ?", (id_act,))
        producto = cursor.fetchone()

        if producto:
            nombre_producto = producto[0]
            cantidad = producto[1]
        else:
            messagebox.showwarning("Advertencia", "No se encontro el producto.")

        query_insert = "INSERT INTO salida_toner (Nombre, Area, producto, Firma, autoriza, fecha, hora,folio) VALUES (?, ?, ?, ?, ?, ?,?,?)"
        datos = (nombre, area, nombre_producto, firma_bytes, firma_bytes2, fechaSi, hora,folio)
        cursor.execute(query_insert, datos)

        cantidad_nueva = cantidad - 1
        query_delete = "UPDATE toner SET cantidad=? WHERE idtoner=?"
        cursor.execute(query_delete, (cantidad_nueva, id_act))
        conexion.commit()
        # Limpiar tabla de salidas
        self.limpiar_tablaSalidas()
        self.limpiar_tabla()
        ventana_flotante.destroy()
        
    def ticket(self, nombre, area, item, ventana_flotante, canvas_f, canvas_f2):
        if not self.valida_firma(canvas_f) or not self.valida_firma(canvas_f2) or not nombre or not area: 
            messagebox.showwarning("Advertencia", "Completa todos los campos del formulario.")
            return
        firma_bytes=self.guardar_como_imagen(canvas_f, f"firma_recibe_{nombre}.png")
        firma_bytes2=self.guardar_como_imagen(canvas_f2, f"firma_autoriza_{nombre}.png")

        fecha = datetime.datetime.now()
        fechaSi = fecha.strftime("%Y/%m/%d")
        hora = fecha.strftime("%H:%M %p")
        folio = ''.join(map(str, [random.randint(1, 10) for _ in range(5)]))
        id_act = self.tree1.item(item, "values")[0]
        conexion = sqlite3.connect('scrnissan.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT modelo, cantidad FROM toner WHERE idtoner = ?", (id_act,))
        producto = cursor.fetchone()

        if producto:
            nombre_producto = producto[0]
            cantidad = producto[1]
        else:
            messagebox.showwarning("Advertencia", "No se encontro el producto.")

        query_insert = "INSERT INTO salida_toner (Nombre, Area, producto, Firma, autoriza, fecha, hora,folio) VALUES (?, ?, ?, ?, ?, ?,?,?)"
        datos = (nombre, area, nombre_producto, firma_bytes, firma_bytes2, fechaSi, hora,folio)
        cursor.execute(query_insert, datos)

        cantidad_nueva = cantidad - 1
        query_delete = "UPDATE toner SET cantidad=? WHERE idtoner=?"
        cursor.execute(query_delete, (cantidad_nueva, id_act))
        conexion.commit()
        # Limpiar tabla de salidas
        self.limpiar_tablaSalidas()
        self.limpiar_tabla()
        ventana_flotante.destroy()
    
    def leer_imagen(self,ruta):
        with open(ruta, 'rb') as archivo:
            return archivo.read()
         
    def guardar_como_imagen(self, canvas, filename):
        # Obtener las dimensiones del canvas
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        # Crear una imagen vacía
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        
        # Dibujar el contenido del canvas en la imagen
        for item in canvas.find_all():
            coords = canvas.coords(item)
            if len(coords) == 4:  #  línea
                draw.line(coords, fill="black", width=2)
        
        with io.BytesIO() as output:
            image.save(output, format="PNG")
            image_bytes = output.getvalue()
        return image_bytes

    def ver_imagen(self, item):
        username = self.username
        id_salida = self.salida.item(item, "values")[0]
        conexion = sqlite3.connect('scrnissan.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM salida_toner WHERE idsalida = ?", (id_salida,))
        datos = cursor.fetchone()

        cursor.execute("SELECT nombre FROM usuarios WHERE usuario = ? ", (username,))
        user = cursor.fetchone()[0]
        conexion.commit()

        if datos:
           
            ventana_flotante = tk.Toplevel(background="white",pady=10)
            ventana_flotante.title("Solicitud de Consumibles")
            ventana_flotante.resizable(False, False)
            recibe=datos[3]
            autoriza=datos[4]
            folio=datos[9]

           
            firma_recibe = Image.open(io.BytesIO(recibe)).resize((150, 150))
            firma_autoriza = Image.open(io.BytesIO(autoriza)).resize((150, 150))
           
            firma_recibe_tk = ImageTk.PhotoImage(firma_recibe)
            firma_autoriza_tk = ImageTk.PhotoImage(firma_autoriza)
            # Cargar imagen
            image_path = "./imgs/CarOne456.png"
            image_path2="./imgs/nissan_1.png"

            imagen = u_img.imagen(image_path, (100, 90))
            imagen2 = u_img.imagen(image_path2, (80, 70))

            marcoImgs=tk.Frame(ventana_flotante)
            marcoImgs.pack(fill="x", expand=False, padx=10)
        
            image_label = tk.Label(marcoImgs, image=imagen)
            image_label.imagen = imagen  
            image_label.pack(side="left")

            image_label2 = tk.Label(marcoImgs, image=imagen2)
            image_label2.imagen = imagen2 
            image_label2.pack(side="right")

            marcoDatos1=tk.Frame(ventana_flotante)
            marcoDatos1.pack(padx=10,fill="both", expand=False)

            label_seleccion = tk.Label(marcoDatos1, text="Salida de Consumibles", font=("Poppins-ExtraLight", 15))
            label_seleccion.pack(padx=10, anchor="w")
            fecha= datos[6]
            hora= datos[7]
            label_folio= tk.Label(marcoDatos1, text=f"Folio: {folio}", font=("Poppins-ExtraLight", 10))
            label_folio.pack(padx=10, anchor="e")
            label_fecha= tk.Label(marcoDatos1, text=f"Fecha: {fecha} {hora}", font=("Poppins-ExtraLight", 10))
            label_fecha.pack(padx=10, anchor="e")

            marcotabla=tk.Frame(ventana_flotante)
            marcotabla.pack(padx=10,fill="x", expand=True)
            #Encabezados de la tabla.
            self.tree = ttk.Treeview(marcotabla,columns=("Nombre", "Area", "Producto","Cantidad"), show="headings",height=5)
            self.tree.heading("Nombre", text="Nombre")
            self.tree.heading("Area", text="Área")
            self.tree.heading("Producto", text="Producto")
            self.tree.heading("Cantidad", text="Cantidad")
            nombre = datos[1]  
            area = datos[2]   
            producto = datos[5] 
            cantidad = 1  
            self.tree.insert("", "end", values=(nombre, area, producto, cantidad))
        
            for column in ("Nombre", "Area", "Producto", "Cantidad"):
                self.tree.column(column, width=100, anchor="center")
            self.tree.pack(fill="x", expand=1, padx=10,pady=10)

            marcoFirma = tk.Frame(ventana_flotante, background="white")
            marcoFirma.pack(fill="both", expand=1, padx=10,pady=5 ,side="left")

            label_firma_recibe = tk.Label(marcoFirma, image=firma_recibe_tk,background="white")
            label_firma_recibe.image = firma_recibe_tk  
            label_firma_recibe.pack(pady=5)

            label_firma1 = tk.Label(marcoFirma, text="Recibe.",background="white" ,font=("Poppins-ExtraLight", 12))
            label_firma1.pack(pady=5, anchor="center")

            marcoFirma2 = tk.Frame(ventana_flotante,background="white")
            marcoFirma2.pack(fill="both", expand=1, padx=10,pady=5 ,side="right")

            label_firma_autoriza = tk.Label(marcoFirma2, image=firma_autoriza_tk,background="white")
            label_firma_autoriza.image = firma_autoriza_tk  
            label_firma_autoriza.pack(pady=5)

            label_firma2 = tk.Label(marcoFirma2,text="Autoriza.", font=("Poppins-ExtraLight", 12),background="white")
            label_firma2.pack(pady=5, anchor="center")
            label_firma_nom = tk.Label(marcoFirma2,text=f"{user}", font=("Poppins-ExtraLight", 12),background="white")
            label_firma_nom.pack(pady=5, anchor="center")

            boton_imprimir = tk.Button(marcoFirma2, width=20, text="Imprimir", bg=BARRA_SUPERIOR, fg="white", command=lambda: toner(nombre, area, producto,hora,fecha,recibe, autoriza,folio ,user,ventana_flotante))
            boton_imprimir.pack(pady=5, anchor="e")

        else:
            messagebox.showwarning("Advertencia", "Ha ocurrido un error al mostrar la información.")

    def pdf(self):
        confirmacion=messagebox.askyesno("Solicitar Consumibles", "¿Seguro que deseas descargar esta información?")
        if confirmacion:
                conexion = sqlite3.connect('scrnissan.db')
                cursor = conexion.cursor()
                cursor.execute("SELECT cantidad, tipo, modelo FROM toner WHERE tipo IN ('Toner', 'Cartucho')")
                cartucho_toner = cursor.fetchall()  

                cursor.execute("SELECT cantidad, tipo, color FROM toner WHERE tipo = ?", ('Tinta(Litro)',))
                tinta = cursor.fetchall() 
                solicitud(tinta,cartucho_toner)
        else:
            return

    def search(self, event=None):
            valor = self.entry_buscar.get()
            self.salida.delete(*self.salida.get_children())
            conexion = sqlite3.connect('scrnissan.db')
            cursor = conexion.cursor()
            cursor.execute("SELECT idsalida,Nombre, Producto, fecha FROM salida_toner WHERE Nombre LIKE ? OR Producto LIKE ? OR Fecha LIKE ? OR idsalida LIKE ?", 
                        ('%' + valor + '%', '%' + valor + '%', '%' + valor + '%', '%' + valor + '%'))
            rows = cursor.fetchall()
            for row in rows:
                self.salida.insert("", "end", values=row +("\uf1f8",)+("\uf06e",))

    def limpiar_tabla(self):
            self.tree1.delete(*self.tree1.get_children())
            conexion = sqlite3.connect('scrnissan.db')
            cursor =conexion.cursor()
            cursor.execute("SELECT idtoner, cantidad, tipo, modelo, color FROM toner")
            rows = cursor.fetchall()
            for row in rows:
                self.tree1.insert("", "end", values=row + ("\uf02f",)+ ("\uf1f8",))  
    
    def limpiar_tablaSalidas(self):
            self.salida.delete(*self.salida.get_children())
            conexion = sqlite3.connect('scrnissan.db')
            cursor =conexion.cursor()
            cursor.execute("SELECT idsalida,Nombre, Producto, fecha FROM salida_toner")
            rows = cursor.fetchall()
            for row in rows:
                self.salida.insert("", "end", values=row +("\uf1f8",)+("\uf06e",))  

    def limpiar_campos(self):
        self.entry_cantidad.delete(0, tk.END)
        self.combo_tipo.set("")
        self.combo_modelo.set("")
        self.combo_color.set("")
