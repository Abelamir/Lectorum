import sqlite3


class DatabaseManager:

  def __init__(self, db_path="conocimiento.db"):
    self.db_path = db_path
    self._init_tables()

  def _get_connection(self):
    conexion = sqlite3.connect(self.db_path)
    # Habilita el soporte de claves foráneas en SQLite
    conexion.execute("PRAGMA foreign_keys = ON;")
    return conexion

  def _init_tables(self):
    # Usamos _get_connection() para que aplique la regla PRAGMA
    with self._get_connection() as conexion:
      cursor = conexion.cursor()

      cursor.execute("""CREATE TABLE IF NOT EXISTS materias (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                nombre TEXT NOT NULL UNIQUE
            )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS unidad_conocimiento (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                nombre TEXT NOT NULL,
                materia_id INTEGER NOT NULL,
                curso TEXT,
                urgencia TEXT,
                FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE
            )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS recursos (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                titulo TEXT NOT NULL,
                ruta_archivo TEXT NOT NULL,
                materia_id INTEGER NOT NULL,
                FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE
            )""")

      # Agregada la coma faltante y corregido 'recursos' en plural
      cursor.execute("""CREATE TABLE IF NOT EXISTS unidad_recurso (
                unidad_id INTEGER NOT NULL,
                recurso_id INTEGER NOT NULL,
                PRIMARY KEY (unidad_id, recurso_id),
                FOREIGN KEY (unidad_id) REFERENCES unidad_conocimiento(id) ON DELETE CASCADE,
                FOREIGN KEY (recurso_id) REFERENCES recursos(id) ON DELETE CASCADE
            )""")

  def buscar_recursos(self, texto_busqueda):
    with self._get_connection() as conexion:
      cursor = conexion.cursor()
      # Consulta JOIN para traer el recurso junto con su materia y unidad
      query = """
                SELECT r.id, r.titulo, r.ruta_archivo, u.nombre AS unidad, m.nombre AS materia
                FROM recursos r
                JOIN materias m ON r.materia_id = m.id
                LEFT JOIN unidad_recurso ur ON r.id = ur.recurso_id
                LEFT JOIN unidad_conocimiento u ON ur.unidad_id = u.id
                WHERE r.titulo LIKE ? OR u.nombre LIKE ? OR m.nombre LIKE ?
            """
      patron = f"%{texto_busqueda}%"
      cursor.execute(query, (patron, patron, patron))
      return cursor.fetchall()

  def insertar(self, tabla, columnas, valores):
    columnas_str = ", ".join(columnas)
    placeholders = ", ".join(["?" for _ in valores])
    query = f"INSERT INTO {tabla} ({columnas_str}) VALUES ({placeholders})"

    with self._get_connection() as conexion:
      cursor = conexion.cursor()
      cursor.execute(query, valores)
      return cursor.lastrowid

  def insertar_materia(self, nombre):
    return self.insertar(
        tabla="materias", columnas=["nombre"], valores=[nombre]
    )

  # Ajustado a los nombres de columna reales de la tabla
  def insertar_unidad_conocimiento(
      self, nombre, materia_id, curso="", urgencia="Media"
  ):
    return self.insertar(
        tabla="unidad_conocimiento",
        columnas=["nombre", "materia_id", "curso", "urgencia"],
        valores=[nombre, materia_id, curso, urgencia],
    )

  def insertar_recurso(self, titulo, ruta_archivo, materia_id):
    return self.insertar(
        tabla="recursos",
        columnas=["titulo", "ruta_archivo", "materia_id"],
        valores=[titulo, ruta_archivo, materia_id],
    )

  def insertar_unidad_recurso(self, unidad_id, recurso_id):
    return self.insertar(
        tabla="unidad_recurso",
        columnas=["unidad_id", "recurso_id"],
        valores=[unidad_id, recurso_id],
    )