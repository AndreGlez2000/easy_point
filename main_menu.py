from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QFont, Qt
from PySide6.QtCore import QSize


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Principal")
        self.showMaximized()
        self.setStyleSheet("background-color: #3680f7;")

        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 50, 50, 150)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Título
        title = QLabel("EasyPoint")
        title.setFont(QFont("Arial", 35, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Seleccione el modo de acceso")
        subtitle.setFont(QFont("Arial", 15))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botones modo cajero / admin
        button_cashier = QPushButton("🛒 Modo Cajero")
        button_admin = QPushButton("⚙️ Modo Admin")

        for btn in (button_cashier, button_admin):
            btn.setMinimumSize(QSize(50, 25))
            btn.setMaximumSize(QSize(250, 100))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: #0f172a;
                    border-radius: 12px;
                    font-size: 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #e2e8f0;
                }
            """)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(50)
        button_layout.addWidget(button_cashier)
        button_layout.addWidget(button_admin)

        # Espaciadores dinámicos
        main_layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Pie de página y botón de agregar usuario
        footer_layout = QVBoxLayout()
        footer_layout.setSpacing(10)
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        add_user_button = QPushButton("➕ Agregar Usuario")
        add_user_button.setMinimumSize(QSize(200, 40))
        add_user_button.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: white;
                border: 1px solid white;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #334155;
            }
        """)



        footer_layout.addWidget(add_user_button)
        # Añadir todo al layout principal
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addLayout(button_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addLayout(footer_layout)

        self.setLayout(main_layout)
