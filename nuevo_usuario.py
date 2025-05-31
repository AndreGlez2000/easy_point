from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox
from PySide6.QtCore import Qt

class NuevoUsuarioDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Nuevo Usuario")
        self.setFixedSize(400, 450)  # Ajusto el tamaño para más espacio
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border-radius: 10px;
            }
            QLabel {
                font-size: 16px;
                color: #343a40;
            }
            QLineEdit {
                font-size: 16px;
                padding: 8px;
                border: 1px solid #007bff;
                border-radius: 8px;
                background: white;
                color: #333333;
                min-height: 30px;  /* Aumento el tamaño mínimo */
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
                padding: 10px 0;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(5)  # Aumento el espaciado entre elementos
        #layout.setContentsMargins(15, 15, 15, 15)  # Ajusto los márgenes

        # Tipo de usuario
        label_tipo = QLabel("Tipo de usuario:")
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Administrador", "Cajero"])
        layout.addWidget(label_tipo)
        layout.addWidget(self.combo_tipo)

        # Nombre
        label_nombre = QLabel("Nombre:")
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre completo")
        layout.addWidget(label_nombre)
        layout.addWidget(self.input_nombre)

        # PIN
        label_pin = QLabel("PIN:")
        self.input_pin = QLineEdit()
        self.input_pin.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pin.setMaxLength(8)
        self.input_pin.setPlaceholderText("PIN (4-8 dígitos)")
        layout.addWidget(label_pin)
        layout.addWidget(self.input_pin)

        # Confirmar PIN
        label_confirmar = QLabel("Confirmar PIN:")
        self.input_confirmar = QLineEdit()
        self.input_confirmar.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_confirmar.setMaxLength(8)
        self.input_confirmar.setPlaceholderText("Repite el PIN")
        layout.addWidget(label_confirmar)
        layout.addWidget(self.input_confirmar)

        # Botón aceptar
        self.btn_aceptar = QPushButton("Crear Usuario")
        self.btn_aceptar.clicked.connect(self.validar_campos)
        layout.addWidget(self.btn_aceptar)

    def validar_campos(self):
        nombre = self.input_nombre.text().strip()
        pin = self.input_pin.text()
        confirmar = self.input_confirmar.text()
        if not nombre:
            QMessageBox.warning(self, "Faltan datos", "Por favor ingresa el nombre.")
            return
        if not pin or not confirmar:
            QMessageBox.warning(self, "Faltan datos", "Por favor ingresa y confirma el PIN.")
            return
        if len(pin) < 4 or len(pin) > 8 or not pin.isdigit():
            QMessageBox.warning(self, "PIN inválido", "El PIN debe tener entre 4 y 8 dígitos numéricos.")
            return
        if pin != confirmar:
            QMessageBox.warning(self, "PIN no coincide", "El PIN y la confirmación no coinciden.")
            return
        self.accept()

    def get_data(self):
        return {
            "tipo": self.combo_tipo.currentText(),
            "nombre": self.input_nombre.text().strip(),
            "pin": self.input_pin.text()
        }
