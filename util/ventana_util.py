#centrar la ventana
def centrar_window(ventana, ancho, largo):
    #cerrar ventana de la app
    pantalla_a=ventana.winfo_screenwidth()
    pantalla_l=ventana.winfo_screenheight()
    x=int((pantalla_a/2)-(ancho/2))
    y=int((pantalla_l/2)-(largo/2))
    return ventana.geometry(f"{ancho}x{largo}+{x}+{y}")