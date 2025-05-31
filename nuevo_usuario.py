from PySide6.QtWidgets import QApplication,QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox
from PySide6.QtCore import Qt
import sys
import db_manager

class NuevoUsuarioDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        spacing = 5
        margins = 20
        self.setWindowTitle("Agregar Nuevo Usuario")
        self.setFixedSize(400, 600)  # Ajusto el tamaño para más espacio
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border-radius: 10px;
            }
            QLabel {
                font-size: 16px;
                color: #343a40;
                margin-bottom: 8px;
                margin-left: -2;
            }
            QLineEdit {
                font-size: 16px;
                padding: 1px;
                border: 1px solid #007bff;
                border-radius: 8px;
                background: white;
                color: #333333;
                min-height: 50px;  /* Aumento el tamaño mínimo */
            }
            QComboBox {
                font-size: 16px;
                padding: 8px;
                border: 1px solid #007bff;
                border-radius: 8px;
                background: white;
                color: #333333;
                min-height: 30px;  /* Aumento el tamaño mínimo */
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #333333;
            }
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 10px 15px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        # Tipo de usuario
        userLayout = QVBoxLayout()
        userLayout.setSpacing(1)
        label_tipo = QLabel("Tipo de usuario:")
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Administrador", "Cajero"])
        userLayout.addWidget(label_tipo)
        userLayout.addWidget(self.combo_tipo)

        # Nombre
        nameLayout = QVBoxLayout()
        nameLayout.setSpacing(1)
        label_nombre = QLabel("Nombre:")
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre completo")
        nameLayout.addWidget(label_nombre)
        nameLayout.addWidget(self.input_nombre)

        # PIN
        pinLayout = QVBoxLayout()
        pinLayout.setSpacing(1)
        label_pin = QLabel("PIN:")
        self.input_pin = QLineEdit()
        self.input_pin.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pin.setMaxLength(8)
        self.input_pin.setPlaceholderText("PIN (4-8 dígitos)")
        pinLayout.addWidget(label_pin)
        pinLayout.addWidget(self.input_pin)

        # Confirmar PIN
        confirmLayout = QVBoxLayout()
        confirmLayout.setSpacing(1)
        label_confirmar = QLabel("Confirmar PIN:")
        self.input_confirmar = QLineEdit()
        self.input_confirmar.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_confirmar.setMaxLength(8)
        self.input_confirmar.setPlaceholderText("Repite el PIN")
        confirmLayout.addWidget(label_confirmar)
        confirmLayout.addWidget(self.input_confirmar)

        # Botón aceptar
        self.btn_aceptar = QPushButton("Crear Usuario")
        self.btn_aceptar.setFixedHeight(50)
        self.btn_aceptar.clicked.connect(self.validar_campos)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(45)
        main_layout.setContentsMargins(20,30,20,30)
        main_layout.addLayout(userLayout)
        main_layout.addLayout(nameLayout)
        main_layout.addLayout(pinLayout)
        main_layout.addLayout(confirmLayout)
        main_layout.addWidget(self.btn_aceptar)

        self.setLayout(main_layout)

    def validar_campos(self):
        nombre = self.input_nombre.text().strip()
        pin = self.input_pin.text()
        confirmar = self.input_confirmar.text()
        tipo_usuario = self.combo_tipo.currentText()

        if not nombre:
            QMessageBox.warning(self, "Faltan datos", "Por favor ingresa el nombre.")
            return
        if not pin or not confirmar:
            QMessageBox.warning(self, "Faltan datos", "Por favor ingresa y confirma el PIN.")
            return
        if len(pin) < 4 or len(pin) > 8 or not pin.isdigit(): # Basic PIN validation
            QMessageBox.warning(self, "PIN inválido", "El PIN debe tener entre 4 y 8 dígitos numéricos.")
            return
        if pin != confirmar:
            QMessageBox.warning(self, "PIN no coincide", "El PIN y la confirmación no coinciden.")
            return

        # Database interaction
        success, message = db_manager.add_user(nombre, pin, tipo_usuario)
        if success:
            QMessageBox.information(self, "Usuario Creado", message)
            self.accept() # Close dialog only on success
        else:
            QMessageBox.critical(self, "Error al Crear Usuario", message)

    def get_data(self):
        return {
            "tipo": self.combo_tipo.currentText(),
            "nombre": self.input_nombre.text().strip(),
            "pin": self.input_pin.text()
        }
