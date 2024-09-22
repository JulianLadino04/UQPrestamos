import tkinter
import customtkinter as ctk
import os
from PIL import ImageTk, Image

carpeta_principal = os.path.dirname(__file__)
carpeta_imagenes = os.path.join(carpeta_principal, "imagenes")


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class Login:
    def __init__(self) :    
        #Crear la ventana principal
        self.root = ctk.CTk()
        self.root.title("Proyecto Final Bases de Datos")
        self.root.iconbitmap(os.path.join(carpeta_imagenes, "logo.ico"))
        self.root.geometry("750x450")
        self.root.resizable(False,False)
        
        #Contenido del login
        logo = ctk.CTkImage(
            light_image = Image.open(os.path.join(carpeta_imagenes, "logo.png")),
            dark_image = Image.open(os.path.join(carpeta_imagenes, "logo.png")),
            size = (250,250)
        )
        
        #Etiqueta para mostrar la imagen
        etiqueta = ctk.CTkLabel(master=self.root, image=logo).pack(pady = 15)
        
        ctk.CTkLabel(self.root, text = "Usuario").pack()
        self.usuario = ctk.CTkEntry(self.root)
        self.usuario.insert(0, "Ej: Laura")
        self.usuario.bind("<Button-1>", lambda e: self.usuario.delete(0, "end"))
        self.usuario.pack()
        
        ctk.CTkLabel(self.root, text = "Contraseña").pack()
        self.contrasena = ctk.CTkEntry(self.root)
        self.contrasena.insert(0, "*********")
        self.contrasena.bind("<Button-1>", lambda e: self.contrasena.delete(0, "end"))
        self.contrasena.pack()
        
        ctk.CTkButton(self.root, text = "Entrar").pack(pady = 10), 
        
        self.root.mainloop()