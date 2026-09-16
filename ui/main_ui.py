import tkinter as tk
import pathlib
import json
from ui.config_ui import VentanaSettings

class VentanaPrincipal:
    def __init__(self, root, gestor_config):
        self.root = root
        self.root.geometry("600x600")
        
        self.gestor = gestor_config
        self.comentarios = [] 
        self.imagenes_en_memoria = [] 
        self.archivo_comentarios = pathlib.Path("comentarios.json")
        
        self.cargar_comentarios()
        
        self.barra_menu = tk.Menu(self.root)
        self.root.config(menu=self.barra_menu)
        
        menu_archivo = tk.Menu(self.barra_menu, tearoff=0)
        menu_archivo.add_command(label="Salir", command=self.root.quit)
        self.barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
        
        self.barra_menu.add_command(label="Configuración", command=self.abrir_settings)
        
        self.frame_feed = tk.Frame(self.root)
        self.frame_feed.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.lbl_titulo = tk.Label(self.frame_feed, text="Muro de Publicaciones")
        self.lbl_titulo.pack(pady=5)
        
        self.caja_comentarios = tk.Text(self.frame_feed, height=20, width=60, state=tk.DISABLED)
        self.caja_comentarios.pack(pady=10)
        
        self.frame_nuevo = tk.Frame(self.frame_feed)
        self.frame_nuevo.pack(fill=tk.X, pady=5)
        
        self.lbl_escribe = tk.Label(self.frame_nuevo, text="Comentar:")
        self.lbl_escribe.pack(side=tk.LEFT, padx=5)
        
        self.entrada_comentario = tk.Entry(self.frame_nuevo, width=40)
        self.entrada_comentario.pack(side=tk.LEFT, padx=5)
        
        self.btn_publicar = tk.Button(self.frame_nuevo, text="Publicar", command=self.publicar_comentario)
        self.btn_publicar.pack(side=tk.LEFT, padx=5)
        
        self.actualizar_vista()
        self.refrescar_caja_comentarios()

    def cargar_comentarios(self):
        if self.archivo_comentarios.exists():
            try:
                with open(self.archivo_comentarios, "r", encoding="utf-8") as f:
                    self.comentarios = json.load(f)
            except Exception as e:
                print("Error cargando comentarios:", e)
                self.comentarios = []

    def guardar_comentarios(self):
        try:
            with open(self.archivo_comentarios, "w", encoding="utf-8") as f:
                json.dump(self.comentarios, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print("Error guardando comentarios:", e)

    def publicar_comentario(self):
        texto = self.entrada_comentario.get()
        if texto != "":
            usuario = self.gestor.config["nombre_usuario"]
            if usuario == "":
                usuario = "Anónimo"
                
            ruta_foto = self.gestor.config["foto_perfil"]
            
            diccionario_comentario = {
                "nombre": usuario,
                "texto": texto,
                "foto": ruta_foto
            }
            
            self.comentarios.append(diccionario_comentario)
            self.guardar_comentarios() 
            self.entrada_comentario.delete(0, tk.END)
            self.refrescar_caja_comentarios()

    def refrescar_caja_comentarios(self):
        self.caja_comentarios.config(state=tk.NORMAL)
        self.caja_comentarios.delete("1.0", tk.END)
        self.imagenes_en_memoria.clear() 
        
        for c in self.comentarios:
            pudo_poner_foto = False
            
            if c["foto"] != "":
                ruta = pathlib.Path(c["foto"])
                if ruta.exists():
                    try:
                        img_original = tk.PhotoImage(file=str(ruta))
                        img_chiquita = img_original.subsample(8, 8) 
                        
                        self.imagenes_en_memoria.append(img_chiquita)
                        self.caja_comentarios.image_create(tk.END, image=img_chiquita)
                        self.caja_comentarios.insert(tk.END, " ")
                        pudo_poner_foto = True
                    except Exception as e:
                        print("Error cargando imagen:", e)
            
            if pudo_poner_foto == False:
                self.caja_comentarios.insert(tk.END, "[Sin foto] ")
                
            texto_final = c["nombre"] + ": " + c["texto"] + "\n\n"
            self.caja_comentarios.insert(tk.END, texto_final)
            
        self.caja_comentarios.config(state=tk.DISABLED)
        self.caja_comentarios.see(tk.END)

    def actualizar_vista(self):
        c = self.gestor.config
        
        if c["tema_interfaz"] == "oscuro":
            color_fondo = "#2b2b2b"
            color_letra = "#ffffff"
            fondo_input = "#404040"
        else:
            color_fondo = "#f0f0f0"
            color_letra = "#000000"
            fondo_input = "#ffffff"
            
        self.root.config(bg=color_fondo)
        self.frame_feed.config(bg=color_fondo)
        self.frame_nuevo.config(bg=color_fondo)
        
        fuente_actual = ("Arial", c["tamano_fuente"])
        
        self.lbl_titulo.config(bg=color_fondo, fg=color_letra, font=("Arial", c["tamano_fuente"] + 4, "bold"))
        self.lbl_escribe.config(bg=color_fondo, fg=color_letra, font=fuente_actual)
        
        self.caja_comentarios.config(bg=fondo_input, fg=color_letra, font=fuente_actual)
        self.entrada_comentario.config(bg=fondo_input, fg=color_letra, font=fuente_actual)
        
        if c["idioma"] == "en" or c["idioma"] == "en-US":
            self.lbl_titulo.config(text="Timeline Feed")
            self.lbl_escribe.config(text="Comment:")
            self.btn_publicar.config(text="Post")
            self.barra_menu.entryconfig(1, label="File")
            self.barra_menu.entryconfig(2, label="Settings")
        else:
            self.lbl_titulo.config(text="Muro de Publicaciones")
            self.lbl_escribe.config(text="Comentar:")
            self.btn_publicar.config(text="Publicar")
            self.barra_menu.entryconfig(1, label="Archivo")
            self.barra_menu.entryconfig(2, label="Configuración")
            
        self.barra_menu.config(fg=c["color_letra"])

    def abrir_settings(self):
        VentanaSettings(self.root, self.gestor, self.actualizar_vista)