import os
import subprocess


class FileManager:

  @staticmethod
  def limpiar_ruta(ruta):
    if not ruta:
      return ""
    
    return os.path.normpath(ruta.strip('"').strip("'"))

  @staticmethod
  def abrir_archivo(ruta):
    ruta_limpia = FileManager.limpiar_ruta(ruta)

    if os.path.exists(ruta_limpia):
      os.startfile(ruta_limpia)
      return True, "Archivo abierto correctamente."
    else:
      return False, f"La ruta no existe: {ruta_limpia}"

  @staticmethod
  def abrir_carpeta_contenedora(ruta):
    ruta_limpia = FileManager.limpiar_ruta(ruta)

    if os.path.exists(ruta_limpia):
      subprocess.run(f'explorer /select,"{ruta_limpia}"')
      return True, "Carpeta contenedora abierta."
    else:
      return False, f"No se encontró la ruta para abrir la carpeta."

  @staticmethod
  def obtener_categoria(ruta):
    ruta_limpia = FileManager.limpiar_ruta(ruta)
    
    if os.path.isdir(ruta_limpia):
      return "Carpeta"

    extension = os.path.splitext(ruta_limpia)[1].lower()

    categorias = {
        ".pdf": "Documento PDF",
        ".docx": "Documento Word",
        ".doc": "Documento Word",
        ".xlsx": "Excel",
        ".pptx": "Presentación",
        ".txt": "Texto",
        ".png": "Imagen",
        ".jpg": "Imagen",
        ".jpeg": "Imagen",
        ".mp4": "Video",
        ".mkv": "Video",
        ".mp3": "Audio",
    }

    return categorias.get(extension, "Otro")