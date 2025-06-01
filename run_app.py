import sys
import traceback
from main_menu import MainMenu
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

try:
    app = QApplication(sys.argv)
    
    # Establecer la fuente predeterminada
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    ventana = MainMenu()
    ventana.show()
    
    sys.exit(app.exec())
except Exception as e:
    print("Error al ejecutar la aplicación:")
    print(traceback.format_exc())
    input("Presiona Enter para cerrar...") 