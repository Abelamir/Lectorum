# main.py
import os
import sys

# Fuerza a Python a buscar módulos en la carpeta raíz del proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow


def main():
  """Punto de entrada principal de la aplicación."""
  try:
    app = MainWindow()
    app.mainloop()
  except Exception as e:
    print(f"Error crítico al iniciar la aplicación: {e}", file=sys.stderr)


if __name__ == "__main__":
  main()