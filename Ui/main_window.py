# ui/main_window.py
import customtkinter as ctk
from database import DatabaseManager
from ui.components import AddResourceDialog, ResourceCard

# Configuración del tema global de CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        # 1. Configuración de la Ventana Principal
        self.title("Gestor de Conocimiento y Recursos")
        self.geometry("950x600")
        self.minsize(800, 500)

        # Conectar con la Base de Datos
        self.db = DatabaseManager()

        # 2. Configurar el Grid Principal (1 fila, 2 columnas)
        self.grid_columnconfigure(0, weight=0)  # Panel lateral (ancho fijo)
        self.grid_columnconfigure(1, weight=1)  # Panel principal (expandible)
        self.grid_rowconfigure(0, weight=1)

        # 3. Construir la UI
        self._crear_sidebar()
        self._crear_panel_principal()

        # Cargar automáticamente todos los recursos al iniciar
        self._ejecutar_busqueda()

    def _crear_sidebar(self):
        """Crea el panel lateral de navegación."""
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="📚 Gestor BD",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.pack(padx=20, pady=(20, 10))

        self.btn_buscar = ctk.CTkButton(
            self.sidebar_frame,
            text="🔍 Buscar Recursos",
            command=self._accion_buscar
        )
        self.btn_buscar.pack(padx=20, pady=10)

        # Al presionar se abre la ventana emergente para registrar
        self.btn_agregar = ctk.CTkButton(
            self.sidebar_frame,
            text="➕ Agregar Recurso",
            command=self._accion_agregar
        )
        self.btn_agregar.pack(padx=20, pady=10)

    def _crear_panel_principal(self):
        """Crea la zona central de búsqueda y lista de tarjetas."""
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Barra de Búsqueda
        frame_busqueda = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_busqueda.pack(fill="x", padx=20, pady=(20, 10))

        self.search_entry = ctk.CTkEntry(
            frame_busqueda,
            placeholder_text="Buscar por materia, unidad o título de archivo..."
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Permite presionar 'Enter' para buscar
        self.search_entry.bind("<Return>", lambda event: self._ejecutar_busqueda())

        self.btn_ejecutar_busqueda = ctk.CTkButton(
            frame_busqueda,
            text="Buscar",
            width=100,
            command=self._ejecutar_busqueda
        )
        self.btn_ejecutar_busqueda.pack(side="right")

        # Área Desplazable de Resultados (Corregido sin el argumento 'title')
        self.results_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.results_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # --- MÉTODOS DE ACCIÓN ---

    def _accion_buscar(self):
        self.search_entry.delete(0, "end")
        self._ejecutar_busqueda()

    def _accion_agregar(self):
        """Abre el diálogo modal de components.py para registrar un recurso."""
        AddResourceDialog(
            master=self,
            db_manager=self.db,
            on_success_callback=self._ejecutar_busqueda
        )

    def _ejecutar_busqueda(self):
        """Consulta la BD y dibuja las tarjetas usando ResourceCard."""
        texto = self.search_entry.get().strip()
        resultados = self.db.buscar_recursos(texto)

        # Limpiar tarjetas anteriores
        for child in self.results_frame.winfo_children():
            child.destroy()

        if not resultados:
            label_vacio = ctk.CTkLabel(
                self.results_frame,
                text="No se encontraron recursos registrados."
            )
            label_vacio.pack(pady=20)
            return

        # Usamos ResourceCard importado de components.py
        for res in resultados:
            card = ResourceCard(
                master=self.results_frame,
                recurso=res,
                on_delete_callback=self._eliminar_recurso_bd
            )
            card.pack(fill="x", padx=10, pady=5)

    def _eliminar_recurso_bd(self, recurso_id):
        """Elimina el registro de la BD y refresca la lista."""
        self.db.eliminar_recurso(recurso_id)
        self._ejecutar_busqueda()