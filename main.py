import tkinter as tk
from config.config import Configuracion_Usuario
from ui.main_ui import VentanaPrincipal

def arrancar_app():
    gestor = Configuracion_Usuario()
    raiz = tk.Tk()
    app = VentanaPrincipal(raiz, gestor)
    raiz.mainloop()


arrancar_app()