import json
import pathlib

class Configuracion_Usuario:
    def __init__(self, nombre_archivo = "configuracion_usuario.json"):  # Clase para crear y manejar la configuración del usuario
        self.file_name = pathlib.Path(nombre_archivo)
        self.temp_path = pathlib.Path(f"{nombre_archivo}.temp")
        self.bak_path = pathlib.Path(f"{nombre_archivo}.bak")

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
        if self.file_name.exists():
            encontrado = True
            try:
                contenido_viejo = self.file_name.read_bytes()
                self.bak_path.write_bytes(contenido_viejo)
            except Exception as e:
                print("Error al hacer el backup:", e)

        try:
            with open(self.temp_path, "w", encoding="utf-8") as f_temp:
                json.dump(self.config, f_temp, indent=4, ensure_ascii=False)
            self.temp_path.replace(self.file_name)
        except Exception as e:
            print("Error guardando el archivo:", e)
    def cargar_configuracion(self):
        if not self.file_name.exists():
            return self.user_config.copy()
        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                datos = json.load(f)
                config_cargada = self.user_config.copy()
                if "nombre_usuario" in datos:
                    config_cargada["nombre_usuario"] = datos["nombre_usuario"]
                if "tema_interfaz" in datos:
                    config_cargada["tema_interfaz"] = datos["tema_interfaz"]
                if "idioma" in datos:
                    config_cargada["idioma"] = datos["idioma"]
                if "tamano_fuente" in datos:
                    config_cargada["tamano_fuente"] = datos["tamano_fuente"]
                if "color_letra" in datos:
                    config_cargada["color_letra"] = datos["color_letra"]
                if "color_barra_menu" in datos:
                    config_cargada["color_barra_menu"] = datos["color_barra_menu"]
                if "foto_perfil" in datos:
                    config_cargada["foto_perfil"] = datos["foto_perfil"]
                return config_cargada
        except json.JSONDecodeError:
            print("El archivo esta corrupo")
            return self.user_config.copy()
        except Exception as e: # Maneja el error por si el archivo no se puede leer
            return self.user_config.copy()

