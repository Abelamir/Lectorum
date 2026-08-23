# ui/components.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
from core import FileManager

class ResourceCard(ctk.CTkFrame):
    """Tarjeta reutilizable para mostrar cada recurso encontrado en las búsquedas."""
    
    def __init__(self, master, recurso, on_delete_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Desempaquetar los datos devueltos por database.py
        # recurso -> (id, titulo, ruta_archivo, unidad_nombre, materia_nombre)
        self.rec_id, self.titulo, self.ruta, self.unidad, self.materia = recurso
        self.on_delete_callback = on_delete_callback
        self.categoria = FileManager.obtener_categoria(self.ruta)
        
        self._construir_ui()

    def _construir_ui(self):
        # Información del recurso (Lado Izquierdo)
        lbl_texto = f"📄 [{self.categoria}] {self.titulo}\n📚 Materia: {self.materia} ➔ Unidad: {self.unidad or 'Sin asignar'}"
        self.lbl_info = ctk.CTkLabel(self, text=lbl_texto, justify="left", font=ctk.CTkFont(size=13))
        self.lbl_info.pack(side="left", padx=15, pady=10)

        # Botón Eliminar (Lado Derecho - Rojo)
        self.btn_eliminar = ctk.CTkButton(
            self, text="🗑️", width=35, fg_color="#C0392B", hover_color="#922B21",
            command=self._confirmar_eliminacion
        )
        self.btn_eliminar.pack(side="right", padx=(2, 10), pady=10)

        # Botón Abrir Carpeta Contenedora
        self.btn_folder = ctk.CTkButton(
            self, text="📁", width=35,
            command=lambda: FileManager.abrir_carpeta_contenedora(self.ruta)
        )
        self.btn_folder.pack(side="right", padx=2, pady=10)

        # Botón Abrir Archivo
        self.btn_abrir = ctk.CTkButton(
            self, text="Abrir Archivo", width=100,
            command=lambda: FileManager.abrir_archivo(self.ruta)
        )
        self.btn_abrir.pack(side="right", padx=2, pady=10)

    def _confirmar_eliminacion(self):
        if messagebox.askyesno("Confirmar", f"¿Deseas eliminar el recurso '{self.titulo}' de la base de datos?"):
            if self.on_delete_callback:
                self.on_delete_callback(self.rec_id)


class AddResourceDialog(ctk.CTkToplevel):
    """Ventana modal emergente para registrar materias, unidades y recursos."""

    def __init__(self, master, db_manager, on_success_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db_manager
        self.on_success_callback = on_success_callback

        # Configuración de la ventana modal
        self.title("➕ Agregar Nuevo Recurso")
        self.geometry("500x520")
        self.resizable(False, False)
        
        # Mantener foco en esta ventana emergente
        self.transient(master)
        self.grab_set()

        self._construir_formulario()

    def _construir_formulario(self):
        # Título
        ctk.CTkLabel(self, text="Registrar Recurso", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(15, 10))

        # 1. Campo Materia
        ctk.CTkLabel(self, text="Nombre de la Materia:").pack(anchor="w", padx=30, pady=(5, 0))
        self.entry_materia = ctk.CTkEntry(self, placeholder_text="Ej: Historia Universal")
        self.entry_materia.pack(fill="x", padx=30, pady=(0, 10))

        # 2. Campo Unidad / Tema
        ctk.CTkLabel(self, text="Unidad o Tema de Conocimiento:").pack(anchor="w", padx=30, pady=(5, 0))
        self.entry_unidad = ctk.CTkEntry(self, placeholder_text="Ej: Revolución Industrial")
        self.entry_unidad.pack(fill="x", padx=30, pady=(0, 10))

        # 3. Campo Título del Recurso
        ctk.CTkLabel(self, text="Título del Archivo/Recurso:").pack(anchor="w", padx=30, pady=(5, 0))
        self.entry_titulo = ctk.CTkEntry(self, placeholder_text="Ej: Resumen Capitulo 1 PDF")
        self.entry_titulo.pack(fill="x", padx=30, pady=(0, 10))

        # 4. Campo Ruta del Archivo con Selector
        ctk.CTkLabel(self, text="Ruta del Archivo:").pack(anchor="w", padx=30, pady=(5, 0))
        frame_ruta = ctk.CTkFrame(self, fg_color="transparent")
        frame_ruta.pack(fill="x", padx=30, pady=(0, 15))

        self.entry_ruta = ctk.CTkEntry(frame_ruta, placeholder_text="Selecciona o pega una ruta...")
        self.entry_ruta.pack(side="left", fill="x", expand=True, padx=(0, 5))

        btn_examinar = ctk.CTkButton(frame_ruta, text="📁", width=40, command=self._seleccionar_archivo)
        btn_examinar.pack(side="right")

        # 5. Botón de Guardado
        self.btn_guardar = ctk.CTkButton(
            self, text="Guardar Recurso", fg_color="#27AE60", hover_color="#1E8449",
            height=40, command=self._guardar
        )
        self.btn_guardar.pack(fill="x", padx=30, pady=20)

    def _seleccionar_archivo(self):
        archivo = filedialog.askopenfilename(title="Seleccionar archivo para el recurso")
        if archivo:
            self.entry_ruta.delete(0, "end")
            self.entry_ruta.insert(0, archivo)

    def _guardar(self):
        materia_nom = self.entry_materia.get().strip()
        unidad_nom = self.entry_unidad.get().strip()
        titulo = self.entry_titulo.get().strip()
        ruta = self.entry_ruta.get().strip()

        # Validación básica de campos vacíos
        if not materia_nom or not titulo or not ruta:
            messagebox.showwarning("Atención", "Por favor completa la materia, el título y la ruta del archivo.")
            return

        try:
            # 1. Insertar o reusar materia
            materia_id = self.db.insertar_materia(materia_nom)
            
            # 2. Insertar unidad de conocimiento
            unidad_id = None
            if unidad_nom:
                unidad_id = self.db.insertar_unidad_conocimiento(nombre=unidad_nom, materia_id=materia_id)

            # 3. Insertar recurso
            recurso_id = self.db.insertar_recurso(titulo=titulo, ruta_archivo=ruta, materia_id=materia_id)

            # 4. Vincular unidad con recurso (si se especificó la unidad)
            if unidad_id:
                self.db.insertar_unidad_recurso(unidad_id=unidad_id, recurso_id=recurso_id)

            messagebox.showinfo("Éxito", "Recurso registrado correctamente.")
            
            if self.on_success_callback:
                self.on_success_callback()
                
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el recurso:\n{e}")