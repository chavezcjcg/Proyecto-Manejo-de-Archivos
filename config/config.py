import json
import os
class Configuracion_Usuario:
    def __init__(self, nombre_archivo  = "configuracion_usuario.json"): #Clase para crear y manejar la configuración del usuario
        self.file_name = nombre_archivo
        self.temp_path = f"{nombre_archivo}.temp"
        self.bak_path = f"{nombre_archivo}.bak"

        self.user_config = {
            "nombre_usuario": "",
            "tema_interfaz": "claro",
            "idioma": "es",
            "tamano_fuente": 12,
            "color_letra": "#000000",
            "color_barra_menu": "#FFFFFF",
            "foto_perfil": "",
        }

        self.config = self.cargar_configuracion()
    def guardar_configuracion(self):
        encontrado = False
        if os.path.exists(self.file_name):
