import tkinter as tk
from tkinter import font, ttk, messagebox, filedialog
from colorsNissan import SIDE_BAR,PRINCIPAL_BODY,CURSOR, ROJO
import util.ventana_util as u_ventana
import util.imagenes_util as u_img
from forms.toner import inventToner
from forms.inventario import inventRecursos
from forms.directorio import directorios
from forms.usuarios import usuarios
import sqlite3
import csv

class menuPrincipal(tk.Tk):
    def __init__(self, username, tipo):
        """Constructor de la clase FormDesign. Inicializa la ventana principal y configura los elementos visuales."""
        super().__init__()
        self.username = username
        self.tipo_user = tipo
        self.logo = u_img.imagen("./imgs/CarOne456.png",(250,220)) #Imagen central.
        self.perfil = u_img.imagen("./imgs/imagen2.png",(80,70)) #Imagen del panel lateral.
        #self.img_sitio =u_img.imagen("./imgs/cono.png",(100,100)) #Icono de la aplicación.
        self.config_ventana()
        self.panel()
        #self.control_b_sup()
        self.menu_lat_control()
        self.controles_cuerpo()

    def config_ventana(self):
        """Configura la ventana principal de la aplicacion, titulo, icono, dimensiones y posición."""
        self.title("Nissan Car One Tuxpan 456") #Titulo de la ventana.
        #self.iconbitmap("./imgs/UNID_Logo3.ico") #Icono de la ventana.
        #w,h =1024,600 #Dimensiones.
        #u_ventana.centrar_window(self,w,h) #Funcion para centrar la ventana en medio de la pantalla.
        self.state('zoomed')

    def panel(self):
        """Configura el color, tamaño, fuente y posición de la barra superior, el panel o menú lateral y el cuerpo principal."""
        #self.barra_sup=tk.Frame(self, bg=BARRA_SUPERIOR,height=50) #Color de fondo "BARRA_SUPERIOR" y largo de la barra.
        #self.barra_sup.pack(side=tk.TOP, fill='both') #Posición y expansión.

        self.side_bar=tk.Frame(self, bg=SIDE_BAR, width=150) #Panel lateral.
        self.side_bar.pack(side=tk.LEFT, fill='both', expand=False) #Posicion y expansión.

        #Cuerpo principal.
        self.cuerpo =tk.Frame(self, bg= PRINCIPAL_BODY)
        self.cuerpo.pack(side=tk.RIGHT,fill='both', expand=True) #Posición a la derecha.

    def menu_lat_control(self):
        """ crea y configura los botones del menú lateral junto con sus iconos y funciones asociadas.
    También agrega separadores entre las secciones del menú."""

        ancho_menu=20
        alto_menu=2
        font_awesome = font.Font(family='FontAwesome', size=15)

        #Logo del menu lateral.
        self.labelperfil=tk.Label(self.side_bar, image=self.perfil, bg=SIDE_BAR)
        self.labelperfil.pack(side=tk.TOP, pady=10)
        self.labelTitle = tk.Label(self.side_bar,text=f"{self.username}",font=("Poppins-ExtraLight",15),fg="white" ,width=16, anchor="center", padx=10,bg=SIDE_BAR)
        self.labelTitle.pack() 
        #Separador de Biblioteca.
        separador = tk.Label(self.side_bar, text="Inventarios", bg=PRINCIPAL_BODY, fg="black", font=("Poppins-ExtraLight",12))
        separador.pack(side=tk.TOP, pady=10, fill="x")
        
        #Botones del menu lateral cada uno dentro de side_bar.
        self.bib=tk.Button(self.side_bar)
        self.prestam=tk.Button(self.side_bar)
        self.comp=tk.Button(self.side_bar)
        self.imp=tk.Button(self.side_bar)
        self.users=tk.Button(self.side_bar)

        #Funciones de los botones.
        buttons_info=[
            ("Equipos", "\ue4e5", self.bib, self.inventarios),
            ("Consumibles", "\uf02f", self.prestam, self.prestamos),
            ("Directorio", "\uf095", self.comp, self.panel_info),
            ("Importar", "\uf1c0", self.imp, self.importar),
            ("Usuarios", "\uf007", self.users, self.users_ventana)
        ]

        is_colaborador = self.tipo_user != "Administrador"

        for index, (text, icon, button, command) in enumerate(buttons_info):
            if is_colaborador and text in ["Importar", "Usuarios"]:
                continue  # Omitir estos botones si el usuario es colaborador
            #Agrega los botones al menu.
            self.config_btn_menu(button, text, icon, font_awesome, ancho_menu, alto_menu, command)
            #Separador de Cómputo.
            if index == 1:
                separator = tk.Label(self.side_bar, text="Personal", bg=PRINCIPAL_BODY, fg="black", font=("Poppins-ExtraLight",12))
                separator.pack(side=tk.TOP, pady=10, fill="x")

             # Separador de Ajustes después del botón "Directorio" (index 2).
            if index == 2:
                if not is_colaborador:
                    separador_ajustes = tk.Label(self.side_bar, text="Ajustes", bg=PRINCIPAL_BODY, fg="black", font=("Poppins-ExtraLight", 12))
                    separador_ajustes.pack(side=tk.TOP, pady=10, fill="x")
            
        # Botón de Cerrar Sesión
        self.logout_button = tk.Button(self.side_bar, text="Cerrar Sesión", fg="white", bg="black", font=("Poppins-ExtraLight", 12), height=alto_menu,relief="flat" ,command=self.cerrar_sesion)
        self.logout_button.pack(side=tk.BOTTOM, pady=10, fill="x")

    def controles_cuerpo(self):
        #Imagen en el cuerpo principal, posicion con relacion a la ventana
        label = tk.Label(self.cuerpo, image=self.logo, bg=PRINCIPAL_BODY)
        label.place(x=0, y=0, relwidth=1, relheight=1)
        rights= tk.Label(self.cuerpo, text="© 2024 Citlalli Chavez",  font=("Poppins-ExtraLight",12))
        rights.place(relx=0.5, rely=0.95, anchor="center")

    def config_btn_menu(self, button,text,icon, font_awesome, ancho_menu, alto_menu, comand):
        button.config(text=f"  {icon}    {text}", anchor="w", font=font_awesome,
                        bd=0, bg=SIDE_BAR, fg="white", width=ancho_menu, height=alto_menu,
                        command= comand) 
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)
   
    def bind_hover_events(self, button):
        
        button.bind("<Enter>", lambda event: self.on_enter(event, button)) #Entrada del cursor
        button.bind("<Leave>", lambda event: self.on_leave(event, button))#Salida del cursos
        
    def on_enter(self, event, button):
        """Entrada del cursor:
        color de fondo amarillo (CURSOR) y letra blanca
        """
        button.config(bg=CURSOR, fg="white")

    def on_leave(self, event, button):
        """Salida del cursor:
        Fondo color del menu lateral, letra blanca
        """
        button.config(bg=SIDE_BAR, fg="white")
  
    def  panel_info(self):
        
        self.limpiar(self.cuerpo)
        inv = directorios()
        inv.crear_tabla(self.cuerpo)   

    def importar(self):
            """Ventana flotante de la configuracion de la base de datos."""
            #configuracion del tamaño , titulo y resize de la ventana
            ventana_importar = tk.Toplevel(background="white",pady=10)
            ventana_importar.title("BD")
            ventana_importar.resizable(False,False)
            w, h = 300, 300
            u_ventana.centrar_window(ventana_importar, w, h)
            self.label_tabla = tk.Label(ventana_importar, text="Seleccione la tabla:",font=("Poppins-ExtraLight",15), background="white")
            self.label_tabla.pack(anchor="w", padx=10, pady=10)
            
            self.combo = ttk.Combobox(ventana_importar, values=["inventario_computo", "directorio"], font=("Poppins-ExtraLight",12),state="readonly")
            self.combo.pack(fill="x", padx=10, pady=10)

            #label de ruta del archivo
            self.label_archivo = tk.Label(ventana_importar, text="Ruta del archivo CSV:",font=("Poppins-ExtraLight",15), background="white")
            self.label_archivo.pack(anchor="w", padx=10, pady=10)
            #contenedor para el cuadro de texto y boton de ruta del archivo
            marco3=tk.Frame(ventana_importar, background="white")
            marco3.pack(expand=1, fill="x",  pady=10, padx=10)
            #entrada de texto
            self.ruta_archivo = tk.Entry(marco3,font=("Poppins-ExtraLight",12))
            self.ruta_archivo.pack( side="left",padx=5, anchor="w",expand=0,fill="x")
            #boton el cual esta relacionado con el evento seleccionar_archivo
            self.button_seleccionar = tk.Button(marco3, text="Abrir", font=("Poppins-ExraLight", 12),bg="#000000",fg="#fff" ,command=self.seleccionar_archivo)
            self.button_seleccionar.pack(side="right",padx=5)
            #mcontenedor de los botones vaciar, aceptar y cancelar, con sus respectivos eventos asociados
            button_frame = tk.Frame(ventana_importar,background="white") 
            button_frame.pack(pady=10)

            self.button_vaciar = tk.Button(button_frame, text="Vaciar", font=("Poppins-ExtraLight", 12),bg="#000000",fg="#fff" ,command=lambda: self.validar(ventana_importar, "vaciar"))
            self.button_vaciar.pack(side="left", padx=10)

            self.button_aceptar = tk.Button(button_frame, text="Aceptar", font=("Poppins-ExtraLight", 12),bg="#000000",fg="#fff" ,command=lambda: self.validar(ventana_importar, "aceptar"))
            self.button_aceptar.pack(side="left", padx=10)

            self.button_cancelar = tk.Button(button_frame, text="Cancelar", font=("Poppins-ExtraLight", 12),bg="#000000",fg="#fff", command=ventana_importar.destroy)
            self.button_cancelar.pack(side="left", padx=10)

    def validar(self, ventana_importar, accion):
        tabla = self.combo.get()
        if accion == "vaciar":
            if tabla:
                self.vaciar_tablas(ventana_importar)
            else:
                messagebox.showwarning("Advertencia", "Por favor complete todos los campos antes de vaciar.")
        elif accion == "aceptar":
            ruta = self.ruta_archivo.get()
            if tabla and ruta:
                self.importar_datos(ventana_importar)
            else:
                messagebox.showwarning("Advertencia", "Por favor complete todos los campos antes de aceptar.")

    def seleccionar_archivo(self):

        archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if archivo:
            self.ruta_archivo.delete(0, tk.END)
            self.ruta_archivo.insert(tk.END, archivo)

    def importar_datos(self, ventana_importar):
        try:
            
            tabla_seleccionada = self.combo.get()
            archivo_csv = self.ruta_archivo.get()
            conexion = sqlite3.connect('scrnissan.db')
            cursor = conexion.cursor()

            tablas = {
                    "directorio": 8,
                    "inventario_computo": 12
                }

            with open(archivo_csv, 'r') as file:
                lector_csv = csv.reader(file)
                next(lector_csv)  
                num_columnas = tablas.get(tabla_seleccionada)
                    
                if num_columnas is not None:
                    for fila in lector_csv:
                        cursor.execute(f'INSERT INTO {tabla_seleccionada} VALUES (NULL,' + ','.join(['?'] * (num_columnas - 1)) + ')', fila[1:])

            conexion.commit()
            conexion.close()
            ventana_importar.destroy()
        except Exception as e:
            messagebox.showerror("Error","Ocurrió un error al insertar los datos: {}".format(str(e)))

    def vaciar_tablas(self, ventana_importar):
        """Vacía la tabla selecionada y reinicia la secuencia o ID de los registros de
          1 hasta el ultimo dato con sqlite_sequence."""
        try:
            tabla_seleccionada= self.combo.get()
            conexion = sqlite3.connect('scrnissan.db')
            cursor = conexion.cursor()
            cursor.execute(f"DELETE FROM {tabla_seleccionada}")
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{tabla_seleccionada}'")
            conexion.commit()
            cursor.close()
            ventana_importar.destroy()
        except Exception as e:
            messagebox.showerror("Error","Ocurrió un error al vacias la tabla: {}".format(str(e))) 

    def inventarios(self):
        self.limpiar(self.cuerpo)
        inv = inventRecursos(self.username)
        inv.crear_tabla(self.cuerpo)

    def prestamos(self):
        self.limpiar(self.cuerpo)
        inv=inventToner(self.username)
        inv.crear_tabla(self.cuerpo) 

    def users_ventana(self):
        self.limpiar(self.cuerpo)
        inv=usuarios(self.username)
        inv.crear_tabla(self.cuerpo) 
          
    def cerrar_sesion(self):
        self.destroy()
        
    def limpiar (self, panel):
        #Limpia el cuerpo principal
        for widget in panel.winfo_children():
            widget.destroy()

