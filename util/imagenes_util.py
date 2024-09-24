#Manejar las imagenes mas facil, para imagenes png, tkinter no puede con jpg.
from PIL import ImageTk, Image

def imagen(path, size):
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.ADAPTIVE))