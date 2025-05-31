from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QDialog, QLineEdit
from PySide6.QtGui import QFont, Qt
from PySide6.QtCore import QSize
from nuevo_usuario import NuevoUsuarioDialog


class PinDialog(QDialog):
    def __init__(self, user_type, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"PIN de {user_type}")
        self.setModal(True)
        self.setFixedSize(350, 220)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border-radius: 10px;
            }
            QLabel {
                font-size: 18px;
                color: #343a40;
            }
            QLineEdit {
                font-size: 20px;
                padding: 10px;
                border: 1px solid #007bff;
                border-radius: 8px;
                background: white;
                color: #333333;
            }
            QPushButton {
                font-size: 18px;
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
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        label = QLabel(f"Ingrese el PIN de {user_type}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setMaxLength(8)
        self.pin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_input.setPlaceholderText("PIN")
        self.ok_button = QPushButton("Aceptar")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(label)
        layout.addWidget(self.pin_input)
        layout.addWidget(self.ok_button)

    def get_pin(self):
        return self.pin_input.text()


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Principal")
        self.showMaximized()
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 16px;
                color: #333333;
            }
            #titleLabel {
                font-size: 35px;
                font-weight: bold;
                color: #343a40;
            }
            #subtitleLabel {
                font-size: 18px;
                color: #6c757d;
            }
            QPushButton {
                font-size: 20px;
                font-weight: bold;
                padding: 12px 0;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            #addUserButton {
                background-color: #1e293b;
                color: white;
                border: 1px solid white;
                border-radius: 8px;
                font-size: 16px;
            }
            #addUserButton:hover {
                background-color: #334155;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 50, 50, 150)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("PuntoLite")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Seleccione el modo de acceso")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button_cashier = QPushButton("🛒 Modo Cajero")
        button_admin = QPushButton("⚙️ Modo Admin")
        for btn in (button_cashier, button_admin):
            btn.setMinimumSize(QSize(50, 25))
            btn.setMaximumSize(QSize(250, 100))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        button_cashier.clicked.connect(lambda: self.show_pin_dialog("Cajero"))
        button_admin.clicked.connect(lambda: self.show_pin_dialog("Administrador"))

        button_layout = QHBoxLayout()
        button_layout.setSpacing(50)
        button_layout.addWidget(button_cashier)
        button_layout.addWidget(button_admin)

        main_layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding))

        footer_layout = QVBoxLayout()
        footer_layout.setSpacing(10)
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        add_user_button = QPushButton("➕ Agregar Usuario")
        add_user_button.setObjectName("addUserButton")
        add_user_button.setMinimumSize(QSize(200, 40))
        add_user_button.clicked.connect(self.open_add_user_dialog)

        footer_layout.addWidget(add_user_button)
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addLayout(button_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addLayout(footer_layout)

        self.setLayout(main_layout)

    def show_pin_dialog(self, user_type):
        dialog = PinDialog(user_type, self)
        if dialog.exec() == QDialog.Accepted:
            pin = dialog.get_pin()
            print(f"PIN ingresado para {user_type}: {pin}")

    def open_add_user_dialog(self):
        dialog = NuevoUsuarioDialog(self)
        if dialog.exec() == QDialog.Accepted:
            user_data = dialog.get_data()
            print(f"Nuevo usuario creado: {user_data}")
