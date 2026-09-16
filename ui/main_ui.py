# ui/main_ui.py
import tkinter as tk
from tkinter import messagebox
import pathlib
import json
from ui.config_ui import VentanaSettings

class VentanaPrincipal:
    def __init__(self, root, gestor_config):
        self.root = root
        self.root.title("Mi Red Social - Lab 1")
        self.root.geometry("650x650")
        
        self.gestor = gestor_config
        self.comentarios = [] 
        self.imagenes_en_memoria = [] 
        self.archivo_comentarios = pathlib.Path("comentarios.json")
        
        self.cargar_comentarios()
        
        self.barra_menu = tk.Menu(self.root)
        self.root.config(menu=self.barra_menu)
        
        # Menú Archivo
        menu_archivo = tk.Menu(self.barra_menu, tearoff=0)
        menu_archivo.add_command(label="Nuevo", command=lambda: messagebox.showinfo("Info", "Funciom"))
        menu_archivo.add_command(label="Salir", command=self.root.quit)
        self.barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
        
        # Menú Ver (Opciones simuladas de Zoom)
        menu_ver = tk.Menu(self.barra_menu, tearoff=0)
        menu_ver.add_command(label="Zoom In (+)", command=lambda: messagebox.showinfo("Zoom", "Zoom ampliado"))
        menu_ver.add_command(label="Zoom Out (-)", command=lambda: messagebox.showinfo("Zoom", "Zoom reducido"))
        self.barra_menu.add_cascade(label="Ver", menu=menu_ver)
        
        # Menú Configuración funcional
        self.barra_menu.add_command(label="Configuración", command=self.abrir_settings)
        
        # Frame principal
        self.frame_feed = tk.Frame(self.root)
        self.frame_feed.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.lbl_titulo = tk.Label(self.frame_feed, text="Muro de Publicaciones")
        self.lbl_titulo.pack(pady=5)
        
        # Caja de texto para el feed
        self.caja_comentarios = tk.Text(self.frame_feed, height=18, width=65, state=tk.DISABLED)
        self.caja_comentarios.pack(pady=10)
        
        # Frame para escribir y reaccionar
        self.frame_nuevo = tk.Frame(self.frame_feed)
        self.frame_nuevo.pack(fill=tk.X, pady=5)
        
        self.lbl_escribe = tk.Label(self.frame_nuevo, text="Comentar:")
        self.lbl_escribe.pack(side=tk.LEFT, padx=2)
        
        self.entrada_comentario = tk.Entry(self.frame_nuevo, width=30)
        self.entrada_comentario.pack(side=tk.LEFT, padx=2)
        
        self.btn_publicar = tk.Button(self.frame_nuevo, text="Publicar", command=self.publicar_comentario)
        self.btn_publicar.pack(side=tk.LEFT, padx=2)
        self.btn_like = tk.Button(self.frame_nuevo, text="Me gusta", command=self.dar_like)
        self.btn_like.pack(side=tk.LEFT, padx=2)
        
        # Botones extra simulados que no hacen gran cosa
        self.frame_extras = tk.Frame(self.frame_feed)
        self.frame_extras.pack(fill=tk.X, pady=5)
        
        self.btn_compartir = tk.Button(self.frame_extras, text="Compartir", command=lambda: messagebox.showinfo("Compartido", "Publicación compartida con éxito"))
        self.btn_compartir.pack(side=tk.LEFT, padx=5)
        
        self.btn_reportar = tk.Button(self.frame_extras, text="Reportar", command=lambda: messagebox.showwarning("Reportado", "Reporte enviado al sistema"))
        self.btn_reportar.pack(side=tk.LEFT, padx=5)

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
                usuario = "Anonimo"
                
            ruta_foto = self.gestor.config["foto_perfil"]
            
            diccionario_comentario = {
                "nombre": usuario,
                "texto": texto,
                "foto": ruta_foto,
                "likes": 0  # Contador en 0
            }
            
            self.comentarios.append(diccionario_comentario)
            self.guardar_comentarios() 
            self.entrada_comentario.delete(0, tk.END)
            self.refrescar_caja_comentarios()

    def dar_like(self):
        if len(self.comentarios) > 0:
            # Suma un like al ultimo comentario publicado
            self.comentarios[-1]["likes"] += 1
            self.guardar_comentarios()
            self.refrescar_caja_comentarios()
        else:
            messagebox.showinfo("Aviso", "No hay comentarios para dar Me gusta.")

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
                
            # Mostramos el nombre, texto y los likes acumulados
            num_likes = c.get("likes", 0)
            texto_final = f"{c['nombre']}: {c['texto']}  |   {num_likes} Me gusta\n\n"
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
        self.frame_extras.config(bg=color_fondo)
        
        fuente_actual = ("Arial", c["tamano_fuente"])
        
        self.lbl_titulo.config(bg=color_fondo, fg=color_letra, font=("Arial", c["tamano_fuente"] + 4, "bold"))
        self.lbl_escribe.config(bg=color_fondo, fg=color_letra, font=fuente_actual)
        
        self.caja_comentarios.config(bg=fondo_input, fg=color_letra, font=fuente_actual)
        self.entrada_comentario.config(bg=fondo_input, fg=color_letra, font=fuente_actual)
        
        if c["idioma"] == "en" or c["idioma"] == "en-US":
            self.lbl_titulo.config(text="Timeline Feed")
            self.lbl_escribe.config(text="Comment:")
            self.btn_publicar.config(text="Post")
            self.btn_like.config(text="Like")
            self.btn_compartir.config(text="Share (Simulated)")
            self.btn_reportar.config(text="Report (Simulated)")
            self.barra_menu.entryconfig(1, label="File")
            self.barra_menu.entryconfig(2, label="View")
            self.barra_menu.entryconfig(3, label="Settings")
        else:
            self.lbl_titulo.config(text="Muro de Publicaciones")
            self.lbl_escribe.config(text="Comentar:")
            self.btn_publicar.config(text="Publicar")
            self.btn_like.config(text="Me gusta")
            self.btn_compartir.config(text="Compartir (Simulado)")
            self.btn_reportar.config(text="Reportar (Simulado)")
            self.barra_menu.entryconfig(1, label="Archivo")
            self.barra_menu.entryconfig(2, label="Ver")
            self.barra_menu.entryconfig(3, label="Configuración")
            
        self.barra_menu.config(fg=c["color_letra"])

    def abrir_settings(self):
        VentanaSettings(self.root, self.gestor, self.actualizar_vista)