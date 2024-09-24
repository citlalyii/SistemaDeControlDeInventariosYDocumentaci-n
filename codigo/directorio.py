import tkinter as tk
from tkinter import ttk, messagebox
from colorsNissan import PRINCIPAL_BODY,BARRA_SUPERIOR
from forms.Conex import crearbd_tablas
from forms.pdf import directorio
import util.ventana_util as u_ventana
import csv
import sqlite3
import datetime
#Clase principal
class directorios():
    def crear_tabla(self, parent_frame):
        """Función que contiene todos los elementos visuales del inventario de cómputo."""
        #Opciones de busqueda de registros
        marco=tk.Frame(parent_frame, background=BARRA_SUPERIOR)
        marco.pack(fill='x', expand=0)

        self.labelTitle = tk.Label(marco, text="Directorio",font=("Poppins-ExtraLight",15),fg="white" ,background=BARRA_SUPERIOR,width=16, anchor="w", padx=10)
        self.labelTitle.grid(row=1, column=0, sticky="w") 
        
        self.entry_buscar = tk.Entry(marco)
        self.entry_buscar.grid(row=1, column=1, padx=10 , sticky="ew")

        self.search_icon_label = tk.Label(marco, text="\uf002",fg="white" ,font=("Font Awesome 5 Free", 14), background=BARRA_SUPERIOR)
        self.search_icon_label.grid(row=1, column=2, sticky="e", padx=10)
        
        marco.columnconfigure(1, weight=1)

        #Formulario principal
        marco2=tk.Frame(parent_frame, background=PRINCIPAL_BODY)
        marco2.pack(expand=0,fill="x", padx=5, pady=5)
    
        self.label_ext = tk.Label(marco2, text="Extensión:", anchor="w",font=("Poppins", 14))
        self.entry_ext = tk.Entry(marco2)

        self.label_nom = tk.Label(marco2, text="Nombre:", anchor="w",font=("Poppins", 14))
        self.entry_nom = tk.Entry(marco2)

        self.label_puesto = tk.Label(marco2, text="Puesto:", anchor="w",font=("Poppins", 14))
        self.entry_puesto = tk.Entry(marco2)

        self.label_correo = tk.Label(marco2, text="Correo:", anchor="w",font=("Poppins", 14))
        self.entry_correo = tk.Entry(marco2)

        self.label_cel = tk.Label(marco2, text="Celular:", anchor="w",font=("Poppins", 14))
        self.entry_cel = tk.Entry(marco2)

        self.label_empresa = tk.Label(marco2, text="Empresa:", anchor="w",font=("Poppins", 14))
        self.entry_empresa = tk.Entry(marco2)

        self.label_lDirect = tk.Label(marco2, text="Linea Directa:", anchor="w",font=("Poppins", 14))
        self.entry_lDirect = tk.Entry(marco2)
       
        self.label_ext.grid(padx=10, pady=5, sticky="w")
        self.entry_ext.grid(row=0, column=1,  pady=5, padx=10, sticky="we")

        self.label_nom.grid(padx=10, pady=5, sticky="w")
        self.entry_nom.grid(row=1, column=1,  pady=5, padx=10, sticky="we")
        
        self.label_puesto.grid(padx=10, pady=5, sticky="w")
        self.entry_puesto.grid(row=2, column=1,  pady=5, padx=10, sticky="we")

        self.label_correo.grid(padx=10, pady=5, sticky="w", row=0, column=2)
        self.entry_correo.grid(row=0, column=3,  pady=5, padx=10, sticky="we")

        self.label_cel.grid(padx=10, pady=5, sticky="w", row=1, column=2)
        self.entry_cel.grid(row=1, column=3,  pady=5, padx=10, sticky="we")
        
        self.label_empresa.grid(padx=10, pady=5, sticky="w", row=2, column=2)
        self.entry_empresa.grid(row=2, column=3,  pady=5, padx=10, sticky="we")

        self.label_lDirect.grid(padx=10, pady=5, sticky="w", row=0, column=4)
        self.entry_lDirect.grid(row=0, column=5,  pady=5, padx=10, sticky="we")
        
        marco2.columnconfigure(1, weight=1)
        marco2.columnconfigure(3, weight=1)
        marco2.columnconfigure(5, weight=1)

        #Botones principales.
        marco3=tk.Frame(parent_frame)
        marco3.pack(expand=0, fill="x",  pady=10)

        self.btn_registrar = tk.Button(marco3, text="Registrar",font=("Poppins-ExraLight", 12),bg=BARRA_SUPERIOR ,command=self.registrar_activo)
        self.btn_modificar = tk.Button(marco3, text="Modificar" ,font=("Poppins-ExtraLight", 12), bg=BARRA_SUPERIOR, command=self.modificar_activo)
        self.btn_imprimir = tk.Button(marco3, text="Descargar" ,font=("Poppins-ExtraLight", 12), bg=BARRA_SUPERIOR, command=lambda:self.imprimir_pdf([1,2,3,4,5,6,7]))
        
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

        #Tabla.
        tabla=tk.Frame(parent_frame, background=PRINCIPAL_BODY)
        tabla.pack(fill="both" ,expand=1, padx=10)

        #Encabezados de la tabla.
        self.tree = ttk.Treeview(tabla ,columns=("#", "ext","nom","puesto","correo","cel","empresa","lDirect", "trash"), show="headings")
        
        self.tree.heading("#", text="#")
        self.tree.heading("ext", text="Extensión")
        self.tree.heading("nom", text="Nombre")
        self.tree.heading("puesto", text="Puesto")
        self.tree.heading("correo", text="Correo")
        self.tree.heading("cel", text="Celular")
        self.tree.heading("empresa", text="Empresa")
        self.tree.heading("lDirect", text="Linea Directa")
        self.tree.heading("trash")
       
        for column in self.tree['columns']:
            self.tree.column(column, width=50,  anchor="center")
        self.tree.pack(fill="both", expand=1, padx=10, pady=10) 
        self.limpiar_tabla()

        self.search_icon_label.bind("<Button-1>", self.search)
        self.tree.bind("<<TreeviewSelect>>", self.fila_sel)#Acción para seleccionar un registro.
        self.tree.bind("<ButtonRelease-1>", self.item_click)#Acción al hacer click en un icono dentro de la tabla.
        
    def fila_sel(self, event):
        """Al seleccionar un registro los valores de este se posicionan
          en su campo correspondiente en el formulario."""
        selection = self.tree.focus()
        values = self.tree.item(selection, "values")
        
        if values and len(values) > 0:
            self.limpiar_campos()
            self.entry_ext.insert(0, values[1])
            self.entry_nom.insert(0, values[2])
            self.entry_puesto.insert(0, values[3])
            self.entry_correo.insert(0, values[4])
            self.entry_cel.insert(0,values[5])
            self.entry_empresa.insert(0,values[6])
            self.entry_lDirect.insert(0,values[7])
        else:
            return
    
    def item_click(self, event):
        #Funcion al seleccionar el icono de eliminar.
        item = self.tree.selection()[0]
        column = self.tree.identify_column(event.x)
        if column == "#9":   
            self.eliminar_activo(item)
        else:
            return
    
    def modificar_activo(self):
        #Funcion para modificar un registro.
        if not self.tree.selection():
            messagebox.showwarning("Advertencia", "Primero debes seleccionar un registro.")
            return
        confirmacion = messagebox.askyesno("Modificar", "¿Seguro que deseas modificar este registro?")
        if confirmacion: 
            selected_item = self.tree.selection()[0]
            idactiv = self.tree.item(selected_item, "values")[0]
            ext = self.entry_ext.get()
            nom = self.entry_nom.get()
            puesto = self.entry_puesto.get()
            correo = self.entry_correo.get()
            cel = self.entry_cel.get()
            empresa = self.entry_empresa.get()
            ldirect = self.entry_lDirect.get()
            try:
                conexion = sqlite3.connect('scrnissan.db')
                cursor = conexion.cursor() 
                query = "UPDATE directorio SET extencion=?, nombre=?, puesto=?,correo=?, celular=?,empresa=?, ldirect=? WHERE iddirect=?"
                cursor.execute(query, (ext,nom,puesto,correo,cel,empresa,ldirect,idactiv))
                conexion.commit()
                self.limpiar_tabla()
                self.limpiar_campos()
            except Exception:
                messagebox.showwarning("Advertencia", "El celular, empresa y/o linea directa deben ser numericos.")
                return
        else:
            return  
             
    def eliminar_activo(self,item):
        #Funcion para eliminar un registro.
        confirmacion = messagebox.askyesno("Eliminar", "¿Seguro que deseas eliminar este registro?")
        if confirmacion:
            try: 
                id_act =self.tree.item(item, "values")[0]
                conexion = sqlite3.connect('scrnissan.db')
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM directorio WHERE iddirect = ?", (id_act,))
                conexion.commit()
                cursor.close()
                self.limpiar_tabla()
                self.limpiar_campos()
            except Exception:
                messagebox.showerror("Error","Ocurrio un error al eliminar el registro.")
        else:
            return

    def registrar_activo(self):
        #Funcion para registrar un equipo.
        if (not self.entry_nom.get() or
            not self.entry_puesto.get() or
            not self.entry_correo.get()):
            messagebox.showwarning("Advertencia","Completa todos los campos del formulario.")
            return
        confirmacion = messagebox.askyesno("Registrar", "¿Seguro que deseas ingresar un registro a la tabla?")
        if confirmacion: 
            ext = self.entry_ext.get()
            nom = self.entry_nom.get()
            puesto = self.entry_puesto.get()
            correo = self.entry_correo.get()
            cel = self.entry_cel.get()
            empresa = self.entry_empresa.get()
            ldirect = self.entry_lDirect.get()

             # Validar que cel y ldirect sean numéricos si no están vacíos
            if cel:
                try:
                    int(cel)  
                except ValueError:
                    messagebox.showwarning("Advertencia", "El celular debe ser numérico.")
                    return
            if ldirect:
                try:
                    int(ldirect) 
                except ValueError:
                    messagebox.showwarning("Advertencia", "La línea directa debe ser numérica.")
                    return
                
            if empresa:
                try:
                    int(empresa)  
                except ValueError:
                    messagebox.showwarning("Advertencia", "El número de empresa debe ser numérico.")
                    return
            
            try:
                conexion = sqlite3.connect('scrnissan.db')
                cursor = conexion.cursor()
                query = "INSERT INTO directorio (extencion,nombre,puesto,correo,celular,empresa,ldirect) VALUES (?, ?, ?, ?, ?, ?, ?)"
                datos = (ext,nom,puesto,correo,cel,empresa,ldirect)
                cursor.execute(query, datos)
                conexion.commit()

                self.limpiar_tabla()
                self.limpiar_campos()
            except Exception:
                messagebox.showwarning("Error", "Ocurrio un error al ingresar los datos.")
    
    def imprimir_pdf(self, indices):
        confirmacion= messagebox.askyesno("Descargar", "¿Seguro que deseas descargar esta información?")
        if confirmacion:
            try:
                datos = []
                for row in self.tree.get_children():
                    campo = self.tree.item(row, 'values')
                    if campo:
                        valores= [campo[i] if len(campo) > i else '' for i in indices]
                        datos.append(valores)
                        if indices ==[1,2,3,4,5,6,7]:
                            directorio(datos)
            except Exception as e:
                messagebox.showerror("Error", "Ocurrio un error al descargar el archivo.")
                               
    def search(self, event=None):
            """Se realiza una busqueda de datos con base al texto ingresado en la caja de busqueda entry_buscar
            declarada en la funcion crear_tabla. """
            valor = self.entry_buscar.get()
            self.tree.delete(*self.tree.get_children())
            conexion = sqlite3.connect('scrnissan.db')
            cursor = conexion.cursor()
            cursor.execute("SELECT iddirect, extencion,nombre,puesto,correo,celular,empresa,ldirect FROM directorio WHERE nombre LIKE ? OR extencion LIKE ? OR celular LIKE ? OR correo LIKE ?", 
                        ('%' + valor + '%', '%' + valor + '%', '%' + valor + '%', '%' + valor + '%'))
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert("", "end", values=row + ("\uf1f8",))

    def limpiar_tabla(self):
            """Limpia los datos de la tabla,los recupera de la base de datos, 
            los muestra en la tabla y devuelve los datos recuperados en forma de lista."""
            self.tree.delete(*self.tree.get_children())
            conexion = sqlite3.connect('scrnissan.db')
            cursor =conexion.cursor()
            cursor.execute("SELECT iddirect,extencion,nombre,puesto,correo,celular,empresa,ldirect FROM directorio")
            rows = cursor.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row + ("\uf1f8",))  

    def limpiar_campos(self):
        """Vacia los campos de entrada del formulario."""
        self.entry_ext.delete(0, tk.END)
        self.entry_nom.delete(0, tk.END)
        self.entry_puesto.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_cel.delete(0, tk.END)
        self.entry_empresa.delete(0, tk.END)
        self.entry_lDirect.delete(0, tk.END)
