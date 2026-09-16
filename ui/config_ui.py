import tkinter as tk
from tkinter import messagebox, colorchooser, filedialog
import pathlib

class VentanaSettings:
    def __init__(self, root_padre, gestor_config, funcion_actualizar):
        self.ventana = tk.Toplevel(root_padre)
        self.ventana.title("Settings")
        self.ventana.geometry("400x550")
        self.gestor = gestor_config
        self.funcion_actualizar = funcion_actualizar
        self.temp_color_letra = self.gestor.config["color_letra"]
        self.temp_foto = self.gestor.config["foto_perfil"]
        self.var_nom = tk.StringVar(value=self.gestor.config["nombre_usuario"])
        self.var_tema = tk.StringVar(value=self.gestor.config["tema_interfaz"])
        self.var_idio = tk.StringVar(value=self.gestor.config["idioma"])
        self.var_fuen = tk.StringVar(value=str(self.gestor.config["tamano_fuente"]))
        tk.Label(self.ventana, text="Nombre Usuario:").pack(pady=2)
        tk.Entry(self.ventana, textvariable=self.var_nom).pack(pady=2)
        tk.Label(self.ventana, text="Tema:").pack(pady=2)
        opciones_t = ["claro", "oscuro"]
        tk.OptionMenu(self.ventana, self.var_tema, *opciones_t).pack(pady=2)
        tk.Label(self.ventana, text="Idioma:").pack(pady=2)
        opciones_i = ["es", "es-ES", "en", "en-US"]
        tk.OptionMenu(self.ventana, self.var_idio, *opciones_i).pack(pady=2)
        tk.Label(self.ventana, text="Tamaño letra (numero):").pack(pady=2)
        tk.Entry(self.ventana, textvariable=self.var_fuen).pack(pady=2)
        self.btn_letra = tk.Button(self.ventana, text="Cambiar Color Letra", bg=self.temp_color_letra, command=self.escoger_color_letra)
        self.btn_letra.pack(pady=5)
        tk.Button(self.ventana, text="Elegir Foto (SOLO PNG)", command=self.escoger_foto).pack(pady=5)
        self.lbl_foto_preview = tk.Label(self.ventana, text="Sin foto")
        self.lbl_foto_preview.pack(pady=5)
        self.img_referencia = None 
        self.cargar_preview_foto(self.temp_foto)   
        tk.Button(self.ventana, text="Guardar Cambios", bg="green", fg="white", command=self.guardar_todo).pack(pady=20)
    def cargar_preview_foto(self, ruta):
        if ruta != "":
            path = pathlib.Path(ruta)
            if path.exists():
                try:
                    img = tk.PhotoImage(file=str(path))
                    img = img.subsample(4, 4)
                    self.img_referencia = img
                    self.lbl_foto_preview.config(image=self.img_referencia, text="")
                except Exception as e:
                    self.lbl_foto_preview.config(text="Error al cargar la foto", image="")
            else:
                self.lbl_foto_preview.config(text="Archivo no existe", image="")

    def escoger_color_letra(self):
        color = colorchooser.askcolor()[1]
        if color != None:
            self.temp_color_letra = color
            self.btn_letra.config(bg=color)
            
    def escoger_foto(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imagenes permitidas", "*.png *.gif")])
        if ruta != "":
            self.temp_foto = ruta
            self.cargar_preview_foto(self.temp_foto)

    def guardar_todo(self):
        try:
            fuente_entero = int(self.var_fuen.get())
        except ValueError:
            messagebox.showerror("Error", "El tamaño de fuente debe ser un numero entero")
            return
            
        self.gestor.config["nombre_usuario"] = self.var_nom.get()
        self.gestor.config["tema_interfaz"] = self.var_tema.get()
        self.gestor.config["idioma"] = self.var_idio.get()
        self.gestor.config["tamano_fuente"] = fuente_entero
        self.gestor.config["color_letra"] = self.temp_color_letra
        self.gestor.config["foto_perfil"] = self.temp_foto
        
        self.gestor.guardar_configuracion()
        self.funcion_actualizar()
        self.ventana.destroy()