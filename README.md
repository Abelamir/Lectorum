Está **casi perfecto**, pero hay dos pequeños detalles de formato en la sección de instalación y al final del archivo que se pueden corregir para que Markdown los muestre impecables:

1. **Bloques de código sin cerrar:** En los pasos 2 y 3 de instalación faltan las comillas triples (```) de cierre.
2. **Formato del enlace:** En el comando `git clone` conviene usar solo la URL limpia sin corchetes de Markdown.

---

### **README.md (Versión Corregida)**

```markdown
# 📚 Lectorum - Gestor de Conocimiento y Recursos

**Lectorum** es una aplicación de escritorio desarrollada en Python para organizar, categorizar y buscar rápidamente archivos locales (PDFs, documentos, imágenes, etc.) asociados a materias y unidades de estudio.

---

## 🚀 Características Principales

* **Búsqueda Dinámica:** Filtra instantáneamente por materia, unidad/tema o título del recurso.
* **Apertura Rápida:** Abre cualquier archivo o su carpeta contenedora directamente desde la aplicación.
* **Categorización Automática:** Detecta el tipo de archivo (PDF, Word, Excel, Imagen, etc.) según su extensión.
* **Interfaz Moderna:** Desarrollada con CustomTkinter en modo oscuro.
* **Base de Datos Relacional:** Gestión eficiente basada en SQLite.

---

## 🛠️ Tecnologías Utilizadas

* **Python 3.x**
* **CustomTkinter** (Interfaz gráfica)
* **SQLite3** (Base de datos)

---

## 💻 Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Abelamir/Lectorum.git
   cd Lectorum

```

2. **Instalar dependencias:**
```bash
pip install customtkinter

```


3. **Iniciar la aplicación:**
```bash
python main.py

```



---

## 📁 Estructura del Proyecto

```text
Lectorum/
│
├── core.py           # Gestión de rutas y categorías de archivos
├── database.py       # Consultas SQL e interacción con SQLite
├── main.py           # Punto de entrada de la aplicación
├── .gitignore        # Exclusión de base de datos y archivos temporales
└── ui/
    ├── __init__.py
    ├── components.py # Tarjetas de recursos y ventanas modales
    └── main_window.py# Ventana principal y barra de búsqueda

```

```
