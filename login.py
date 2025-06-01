from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, 
                              QPushButton, QLabel, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sqlite3

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iniciar Sesión - Sistema de Inventario")
        self.setup_ui()
        
    def setup_ui(self):
        # Configurar el layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Título
        titulo = QLabel("Sistema de Inventario")
        titulo.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #343a40;
            }
        """)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Subtítulo
        subtitulo = QLabel("Iniciar Sesión")
        subtitulo.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #6c757d;
            }
        """)
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Campo de usuario
        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Usuario")
        self.usuario_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #80bdff;
                outline: 0;
                box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
            }
        """)
        
        # Campo de contraseña
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(self.usuario_input.styleSheet())
        
        # Botón de inicio de sesión
        btn_login = QPushButton("Iniciar Sesión")
        btn_login.setStyleSheet("""
            QPushButton {
                padding: 12px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        btn_login.clicked.connect(self.iniciar_sesion)
        
        # Agregar widgets al layout
        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        layout.addStretch()
        layout.addWidget(self.usuario_input)
        layout.addWidget(self.password_input)
        layout.addWidget(btn_login)
        layout.addStretch()
        
        # Configurar la ventana
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: white;")
        
    def iniciar_sesion(self):
        usuario = self.usuario_input.text()
        password = self.password_input.text()
        
        if not usuario or not password:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos")
            return
            
        try:
            conn = sqlite3.connect("easypoint.db")
            cursor = conn.cursor()
            
            # Verificar credenciales
            cursor.execute("""
                SELECT id_usuario, nombre_usuario, es_administrador 
                FROM Usuarios 
                WHERE nombre_usuario = ? AND password = ?
            """, (usuario, password))
            
            user = cursor.fetchone()
            
            if user:
                from historial_ventas import HistorialVentas
                self.ventana_principal = HistorialVentas()
                self.ventana_principal.resize(1200, 800)
                self.ventana_principal.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")
                
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error de base de datos: {str(e)}")
        finally:
            conn.close()

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Establecer la fuente predeterminada
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    ventana = LoginWindow()
    ventana.show()
    
    sys.exit(app.exec()) 