import tkinter as tk
from tkinter import ttk, messagebox
from colorsNissan import PRINCIPAL_BODY,BARRA_SUPERIOR
from forms.Conex import crearbd_tablas
import sqlite3
import util.ventana_util as u_ventana
import util.imagenes_util as u_img
import hashlib
import tkinter.font as tkFont
#Clase principal
class usuarios():
    def __init__(self, username):
        super().__init__()
        self.username = username

    def crear_tabla(self, parent_frame):
        marco=tk.Frame(parent_frame, background=BARRA_SUPERIOR)
        marco.pack(fill='x', expand=0)

        self.labelTitle = tk.Label(marco, text="Usuarios",font=("Poppins-ExtraLight",15),fg="white" ,background=BARRA_SUPERIOR,width=16, anchor="w", padx=10)
        self.labelTitle.grid(row=1, column=0, sticky="w") 
        
        self.entry_buscar = tk.Entry(marco)
        self.entry_buscar.grid(row=1, column=1, padx=10 , sticky="ew")

        self.search_icon_label = tk.Label(marco, text="\uf002",fg="white" ,font=("Font Awesome 5 Free", 14), background=BARRA_SUPERIOR)
        self.search_icon_label.grid(row=1, column=2, sticky="e", padx=10)
        
        marco.columnconfigure(1, weight=1)

        marco2=tk.Frame(parent_frame, background=PRINCIPAL_BODY)
        marco2.pack(expand=0,fill="x", padx=5, pady=5)
    
        self.label_nom = tk.Label(marco2, text="Nombre:", anchor="w",font=("Poppins", 14))
        self.entry_nom = tk.Entry(marco2)

        self.label_user = tk.Label(marco2, text="Usuario:", anchor="w",font=("Poppins", 14))
        self.entry_user = tk.Entry(marco2)

        self.label_area = tk.Label(marco2, text="Área:", anchor="w",font=("Poppins", 14))
        self.entry_area = tk.Entry(marco2)
        
        self.label_rol = tk.Label(marco2, text="Rol:", anchor="w",font=("Poppins", 14))
        self.combo_rol = ttk.Combobox(marco2, values=["Colaborador","Administrador"])

        self.label_pass = tk.Label(marco2, text="Contraseña:", anchor="w",font=("Poppins", 14))
        self.entry_pass = tk.Entry(marco2,show='*')

        self.label_pass2 = tk.Label(marco2, text="Contraseña (Repetir):", anchor="w",font=("Poppins", 14))
        self.entry_pass2 = tk.Entry(marco2,show='*')

        self.label_nom.grid(padx=10, pady=5, sticky="w")
        self.entry_nom.grid(row=0, column=1,  pady=5, padx=10, sticky="we")

        self.label_user.grid(padx=10, pady=5, sticky="w")
        self.entry_user.grid(row=1, column=1,  pady=5, padx=10, sticky="we")
        
        self.label_area.grid(padx=10, pady=5, sticky="w",row=0,column=2)
        self.entry_area.grid(row=0, column=3,  pady=5, padx=10, sticky="we")

        self.label_rol.grid(padx=10, pady=5, sticky="w",row=1,column=2)
        self.combo_rol.grid(row=1, column=3,  pady=5, padx=10, sticky="we")
        
        self.label_pass.grid(padx=10, pady=5, sticky="w",row=0,column=4)
        self.entry_pass.grid(row=0, column=5,  pady=5, padx=10, sticky="we")

        # Configuración del ícono de ojo
        fa_font = tkFont.Font(family="Font Awesome 5 Free", size=14, weight="normal")
        self.eye_open_icon = "\uf06e"  # Ojo abierto
        self.eye_closed_icon = "\uf070"  # Ojo cerrado
        self.plus1 = tk.Label(marco2, text=self.eye_closed_icon, fg="#000", font=fa_font)
        self.plus1.grid(row=0, column=6, sticky="e", padx=10)
        # Configuración del evento del ícono
        self.plus1.bind("<Button-1>", self.toggle_password)

        self.label_pass2.grid(padx=10, pady=5, sticky="w", row=1, column=4)
        self.entry_pass2.grid(row=1, column=5,  pady=5, padx=10, sticky="we")

        # Configuración del ícono de ojo para entry_pass2
        self.plus2 = tk.Label(marco2, text=self.eye_closed_icon, fg="#000", font=fa_font)
        self.plus2.grid(row=1, column=6, sticky="e", padx=10)

        # Configuración del evento del ícono de entry_pass2
        self.plus2.bind("<Button-1>", self.toggle_password_pass2)

        marco2.columnconfigure(1, weight=1)
        marco2.columnconfigure(3, weight=1)
        marco2.columnconfigure(5, weight=1)

        #Botones principales.
        marco3=tk.Frame(parent_frame)
        marco3.pack(expand=0, fill="x",  pady=10)
       
        self.btn_registrar = tk.Button(marco3, text="Registrar",font=("Poppins-ExraLight", 12),bg=BARRA_SUPERIOR ,command=self.registrar_activo)
        self.btn_registrar.pack(side="right", padx=20, pady=5)
        self.btn_registrar.config(fg="#fff", width=15, height=1)

        self.btn_modif = tk.Button(marco3, text="Modificar",font=("Poppins-ExraLight", 12),bg=BARRA_SUPERIOR ,command=self.modificar_activo)
        self.btn_modif.pack(side="right", padx=20, pady=5)
        self.btn_modif.config(fg="#fff", width=15, height=1)

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

        #Tabla.
        tabla=tk.Frame(parent_frame, background=PRINCIPAL_BODY)
        tabla.pack(fill="both" ,expand=1, padx=10)

        self.label_nom = tk.Label(tabla, text="Todos los usuarios", anchor="w",font=("Poppins", 14))
        self.label_nom.pack(anchor="w",padx=10)

        #Encabezados de la tabla.
        self.tree = ttk.Treeview(tabla ,columns=("#", "nom","user","area","rol","cpass", "susp", "desb"), show="headings")
        
        self.tree.heading("#", text="#")
        self.tree.heading("nom", text="Nombre")
        self.tree.heading("user", text="Usuario")
        self.tree.heading("area", text="Área")
        self.tree.heading("rol", text="Rol")
        self.tree.heading("cpass", text="Cambiar Contraseña")
        self.tree.heading("susp", text="Suspender")
        self.tree.heading("desb", text="Desbloquear")

        for column in self.tree['columns']:
            self.tree.column(column, width=50,  anchor="center")
        self.tree.pack(fill="both", expand=1, padx=10, pady=10) 
        self.limpiar_tabla()

        self.search_icon_label.bind("<Button-1>", self.search)
        self.tree.bind("<<TreeviewSelect>>", self.fila_sel)#Acción para seleccionar un registro.
        self.tree.bind("<ButtonRelease-1>", self.item_click)#Acción al hacer click en un icono dentro de la tabla.
        
    def fila_sel(self, event):
        selection = self.tree.focus()
        values = self.tree.item(selection, "values")        
        if values and len(values) > 0:
            self.limpiar_campos()
            self.entry_nom.insert(0, values[1])
            self.entry_user.insert(0, values[2])
            self.entry_area.insert(0, values[3])
            self.combo_rol.insert(0, values[4])
            self.entry_pass.insert(0, "estoesunacontraseña")
            self.entry_pass2.insert(0, "estoesunacontraseña" )
        else:
            return
    
    def item_click(self, event):
        #Funcion al seleccionar el icono de eliminar.
        item = self.tree.selection()[0]
        column = self.tree.identify_column(event.x)
        if column == "#6":   
            self.cambiarPassw(item)
        elif column == "#7":   
            self.suspender(item)
        elif column == "#8":
            self.desbloquear(item)
        else:
            return

    def toggle_password(self, event):
        if self.entry_pass.cget('show') == '*':
            self.entry_pass.config(show='')
            self.plus1.config(text=self.eye_open_icon)
        else:
            self.entry_pass.config(show='*')
            self.plus1.config(text=self.eye_closed_icon)
    
    def toggle_password_pass2(self, event):
        if self.entry_pass2.cget('show') == '*':
            self.entry_pass2.config(show='')
            self.plus2.config(text=self.eye_open_icon)
        else:
            self.entry_pass2.config(show='*')
            self.plus2.config(text=self.eye_closed_icon)

    def pasw_actual(self, event):
        if self.entry_Actual.cget('show') == '*':
            self.entry_Actual.config(show='')
            self.plus1.config(text=self.eye_open_icon)
        else:
            self.entry_Actual.config(show='*')
            self.plus1.config(text=self.eye_closed_icon)

    def modificar_activo(self):
        #Funcion para modificar un registro.
        if not self.tree.selection():
            messagebox.showwarning("Advertencia", "Primero debes seleccionar un registro.")
            return
        
        confirmacion = messagebox.askyesno("Modificar", "¿Seguro que deseas modificar este registro?")
        if confirmacion: 
            selected_item = self.tree.selection()[0]
            iduser = self.tree.item(selected_item, "values")[0]
            nom = self.entry_nom.get()
            user = self.entry_user.get()
            area = self.entry_area.get()
            tipo = self.combo_rol.get()
            if user and nom and area and tipo:
                conexion = sqlite3.connect('scrnissan.db')
                cursor = conexion.cursor() 

                cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND idusuarios != ?", (user, iduser))
                resultado = cursor.fetchone()

                if resultado:
                    messagebox.showwarning("Advertencia", "El nombre de usuario ya está en uso.")
                    conexion.close()
                    return
                
                query = "UPDATE usuarios SET nombre=?, usuario=?, puesto=?, tipo=? WHERE idusuarios=?"
                cursor.execute(query, (nom,user,area,tipo,iduser))
                conexion.commit()
                self.limpiar_tabla()
                self.limpiar_campos()
            else:
                messagebox.showwarning("Advertencia", "Completa los campos del formulario.")
        else:
            return
                
    def suspender(self,item):
        confirmacion = messagebox.askyesno("Suspender", "¿Seguro que deseas suspender este usuario?")
        if confirmacion:
            try:
                id_user =self.tree.item(item, "values")[0]
                conexion = sqlite3.connect('scrnissan.db')
                cursor = conexion.cursor() 
                estado=0
                query = "UPDATE usuarios SET estado=? WHERE idusuarios=?"
                cursor.execute(query, (estado,id_user))
                conexion.commit()
                cursor.close()
                self.limpiar_tabla()
                self.limpiar_campos()
            except Exception:
                messagebox.showwarning("Advertencia","Ocurrio un error al suspender este usuario.")
        else:
            return
        
    def desbloquear(self,item):
        confirmacion = messagebox.askyesno("Desbloquear", "¿Seguro que deseas desbloquear este usuario?")
        if confirmacion:
            try: 
                id_user =self.tree.item(item, "values")[0]
                conexion = sqlite3.connect('scrnissan.db')
                cursor = conexion.cursor() 
                estado=1
                query = "UPDATE usuarios SET estado=? WHERE idusuarios=?"
                cursor.execute(query, (estado,id_user))
                conexion.commit()
                cursor.close()
                self.limpiar_tabla()
                self.limpiar_campos()
            except Exception:
                messagebox.showwarning("Advertencia","Ocurrio un error al desbloquear este usuario.")
        else:
            return

    def cambiarPassw(self,item):
            """id_user = self.tree.item(item, "values")[0]
            conexion = sqlite3.connect('scrnissan.db')
            cursor = conexion.cursor()
            cursor.execute("SELECT contraseña FROM usuarios WHERE idusuarios = ?", (id_user,))
            passw = cursor.fetchone()"""

            registro_window = tk.Toplevel()
            registro_window.title("Login")
            registro_window.resizable(False, False)
            w, h = 500, 550  # Dimensiones.
            u_ventana.centrar_window(registro_window, w, h)

            marco_Registro = tk.Frame(registro_window)
            marco_Registro.pack(expand=0, padx=10,pady=10, anchor="center",fill="x")

            image_path = "./imgs/llave.png"
            imagen = u_img.imagen(image_path, (170, 150))
            image_label = tk.Label(marco_Registro, image=imagen)
            image_label.imagen = imagen 
            image_label.pack(pady=5)

            self.texto=tk.Label(marco_Registro, text="Cambiar Contraseña",font=("Poppins-Bold", 25))
            self.texto.pack(pady=10,padx=20, anchor="w")

            self.Actual=tk.Label(marco_Registro, text="Contraseña Actual",font=("Poppins-ExtraLight", 13))
            self.Actual.pack(pady=5,padx=30,anchor="w")

            marcoActual=tk.Frame(marco_Registro, background=PRINCIPAL_BODY)
            marcoActual.pack(expand=0,fill="x", padx=5, pady=5)

            entry_Actual = tk.Entry(marcoActual,highlightbackground="white", highlightthickness=2, show='*')
            entry_Actual.pack(pady=5,padx=(30,5),expand=1,fill="x", side="left")
            self.create_eye_icon(marcoActual, entry_Actual, "actual")
            
            self.nueva=tk.Label(marco_Registro, text="Nueva Contraseña",font=("Poppins-ExtraLight", 13))
            self.nueva.pack(pady=5,padx=30,anchor="w")

            marconueva=tk.Frame(marco_Registro, background=PRINCIPAL_BODY)
            marconueva.pack(expand=0,fill="x", padx=5, pady=5)

            entry_nueva = tk.Entry(marconueva,highlightbackground="white", highlightthickness=2, show='*')
            entry_nueva.pack(pady=5,padx=(30,5),expand=1,fill="x",side="left")
            self.create_eye_icon(marconueva, entry_nueva, "nueva")

            self.repetir=tk.Label(marco_Registro, text="Repetir Contraseña", font=("Poppins-ExtraLight", 13))
            self.repetir.pack(pady=5,padx=30,anchor="w")

            marcorep=tk.Frame(marco_Registro, background=PRINCIPAL_BODY)
            marcorep.pack(expand=0,fill="x", padx=5, pady=5)

            entry_repetir = tk.Entry(marcorep,highlightbackground="white", highlightthickness=2, show='*')
            entry_repetir.pack(pady=5,padx=(30,5),expand=1,fill="x", side="left")
            self.create_eye_icon(marcorep, entry_repetir, "repetir")
            
            self.buton=tk.Button(marco_Registro, text="Guardar",bg=BARRA_SUPERIOR ,fg="white",width=15,font=("Poppins-ExtraLight", 13),command=lambda:self.nuevaContraseña(entry_Actual.get(),entry_nueva.get(),entry_repetir.get(),registro_window,item))
            self.buton.pack(pady=10)
        
    def create_eye_icon(self, frame, entry_field, tipo):
        fa_font = tkFont.Font(family="Font Awesome 5 Free", size=14, weight="normal")
        eye_open_icon = "\uf06e"  # Ojo abierto
        eye_closed_icon = "\uf070"  # Ojo cerrado
        plus1 = tk.Label(frame, text=eye_closed_icon, fg="#000", font=fa_font)
        plus1.pack(padx=10, side="right")

        plus1.bind("<Button-1>", lambda event: self.pasww2(entry_field, plus1, tipo))

    def pasww2(self, entry_field, icon_label, tipo):
        if entry_field.cget('show') == '*':
            entry_field.config(show='')
            icon_label.config(text="\uf06e")  # Ojo abierto
        else:
            entry_field.config(show='*')
            icon_label.config(text="\uf070")  # Ojo cerrado

    def nuevaContraseña(self,antigua, nueva, repetir,ventana,item):
        id_user =self.tree.item(item, "values")[0]
        # Función para actualizar la contraseña del usuario
        if not (antigua and nueva and repetir):
            messagebox.showwarning("Advertencia", "Completa todos los campos del formulario.")
            return
        if nueva != repetir:
            messagebox.showwarning("Advertencia", "Las contraseñas nuevas no coinciden.")
            return
        conexion = sqlite3.connect('scrnissan.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT contraseña FROM usuarios WHERE idusuarios=?", (id_user,))
        row = cursor.fetchone()
        
        if row:
            contra_hasheada = row[0]
            if self.verificar_contraseña(antigua, contra_hasheada):
                nueva_hasheada = self.hash_password(nueva)
                query = "UPDATE usuarios SET contraseña=?,confirmarC=? WHERE idusuarios=?"
                cursor.execute(query, (nueva_hasheada,nueva_hasheada ,id_user))
                conexion.commit()
                messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "La contraseña actual no es correcta.")
        else:
            messagebox.showerror("Error", "Usuario no encontrado.")

    def hash_password(self, password):
        # Función para hashear con SHA-256
        password_bytes = password.encode('utf-8')
        hashed_password = hashlib.sha256(password_bytes).hexdigest()
        return hashed_password
    
    def registrar_activo(self):
        nom = self.entry_nom.get()
        user = self.entry_user.get()
        passw = self.entry_pass.get()
        pass2 = self.entry_pass2.get()
        area= self.entry_area.get()
        tipo= self.combo_rol.get()

        if not (nom and user and passw and pass2 and area and tipo):
            messagebox.showwarning("Advertencia", "Completa todos los campos del formulario.")
            return
        confirmacion = messagebox.askyesno("Registrar", "¿Seguro que deseas registrar este usuario?")
        if confirmacion: 
            
            if passw != pass2:
                messagebox.showwarning("Advertencia", "Las contraseñas no coinciden.")
                return

            passw_hasheada = self.hash_password(passw)

            try:
                conexion = sqlite3.connect('scrnissan.db')
                cursor = conexion.cursor()

                cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (user,))
                resultado = cursor.fetchone()

                if resultado:
                    messagebox.showwarning("Advertencia", "El nombre de usuario ya está en uso.")
                    conexion.close()
                    return
            
                query = "INSERT INTO usuarios (nombre, usuario, contraseña, confirmarC, estado, puesto, tipo) VALUES (?, ?, ?, ?, ?, ?, ?)"
                datos = (nom, user, passw_hasheada, pass2, 1, area, tipo)
                cursor.execute(query, datos)
                conexion.commit()
                self.limpiar_tabla()
                conexion.close()
            except sqlite3.Error as error:
                messagebox.showerror("Error", f"No se pudo insertar el usuario.")

    def search(self, event=None):
            """Se realiza una busqueda de datos con base al texto ingresado en la caja de busqueda entry_buscar
            declarada en la funcion crear_tabla. """
            valor = self.entry_buscar.get()
            self.tree.delete(*self.tree.get_children())
            conexion = sqlite3.connect('scrnissan.db')
            cursor = conexion.cursor()
            cursor.execute("SELECT  idusuarios, nombre,usuario, puesto, tipo,estado FROM usuarios WHERE nombre LIKE ? OR usuario LIKE ? OR puesto LIKE ? OR estado LIKE ? OR tipo LIKE ?", 
                        ('%' + valor + '%', '%' + valor + '%', '%' + valor + '%', '%' + valor + '%', '%' + valor + '%'))
            rows = cursor.fetchall()
            
            for row in rows:
                idusuarios, nombre,usuario,puesto,tipo,estado = row
                if estado == 0:
                    tag_color = "ROJO"
                else:
                    tag_color = "NORMAL"
                self.tree.insert("", "end", values=(idusuarios, nombre, usuario,puesto,tipo,"\uf084", "\uf023","\uf09c"), tags=(tag_color,"ROW",))

            self.tree.tag_configure("ROJO", foreground="red")
            self.tree.tag_configure("NORMAL", foreground="black")
            conexion.commit() 

    def verificar_contraseña(self,contraseña_plana, contraseña_hasheada):
        return self.hash_password(contraseña_plana) == contraseña_hasheada

    def hash_password(self,password):
        password_bytes = password.encode('utf-8')
        hashed_password = hashlib.sha256(password_bytes).hexdigest()
        return hashed_password

    def limpiar_tabla(self):
            self.tree.delete(*self.tree.get_children())
            conexion = sqlite3.connect('scrnissan.db')
            cursor =conexion.cursor()
            cursor.execute("SELECT idusuarios, nombre,usuario,puesto,tipo,estado FROM usuarios")
            rows = cursor.fetchall()
            for row in rows:
                idusuarios, nombre,usuario,puesto,tipo,estado = row
                if estado == 0:
                    tag_color = "ROJO"
                else:
                    tag_color = "NORMAL"
                self.tree.insert("", "end", values=(idusuarios, nombre, usuario,puesto,tipo,"\uf084", "\uf023","\uf09c"), tags=(tag_color,"ROW",))

            self.tree.tag_configure("ROJO", foreground="red")
            self.tree.tag_configure("NORMAL", foreground="black")
            conexion.commit()  

    def limpiar_campos(self):
        self.entry_nom.delete(0, tk.END)
        self.entry_user.delete(0, tk.END)
        self.entry_pass.delete(0, tk.END)
        self.entry_pass2.delete(0, tk.END)
        self.entry_area.delete(0, tk.END)
        self.combo_rol.set(" ")
