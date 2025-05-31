from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
                               QSpacerItem, QSizePolicy, QDialog, QLineEdit, QMessageBox) # Added QMessageBox
from PySide6.QtGui import QFont, Qt 
from PySide6.QtCore import QSize, QTimer 
from nuevo_usuario import NuevoUsuarioDialog
from venta import VentanaPuntoDeVenta
import db_manager # <<<--- IMPORT DB MANAGER


class PinDialog(QDialog):
    def __init__(self, user_type, parent=None): # user_type is now more of a title hint
        super().__init__(parent)
        self.setWindowTitle(f"Acceso {user_type}") # Changed title
        self.setModal(True)
        self.setFixedSize(480, 360) # Aumentado el alto
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border-radius: 10px;
            }
            QLabel {
                font-size: 18px;
                color: #343a40;
                margin-bottom: 8px; /* Adjusted margin */
            }
            QLineEdit {
                font-size: 18px; /* Adjusted font size */
                padding: 10px;
                border: 1px solid #007bff;
                border-radius: 8px;
                background: white;
                color: #333333;
                /* alignment: AlignCenter; Removed for username */
            }
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                padding: 10px 15px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 8px;
                min-height: 40px; 
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15) 
        layout.setContentsMargins(30, 25, 30, 25)

        # Username field
        self.username_label = QLabel("Nombre de Usuario:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingrese su usuario")
        
        # PIN field
        self.pin_label = QLabel(f"PIN de {user_type}:") # Still use user_type for PIN label context
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setMaxLength(8) 
        self.pin_input.setPlaceholderText("Ingrese su PIN")
        


        self.ok_button = QPushButton("Aceptar")
        self.ok_button.clicked.connect(self.accept)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addSpacerItem(QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)) # Smaller spacer
        layout.addWidget(self.pin_label)
        layout.addWidget(self.pin_input)
        layout.addSpacerItem(QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)) # Adjusted spacer
        layout.addWidget(self.ok_button)

    def get_credentials(self):
        return self.username_input.text().strip(), self.pin_input.text()


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Principal")
        self.setMinimumSize(900,600) 
        self.ventana_venta_instancia = None 
        self.current_user_id = None 
        self.current_user_name = None # <<<--- STORE LOGGED IN USER NAME
        
        # Stylesheet from user context, potentially with global font
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                /* font-family: "Lora"; /* Example if Lora font is loaded globally */
            }
            QLabel {
                font-size: 16px;
                color: #333333;
            }
            #titleLabel {
                font-size: 80px; 
                font-weight: bold;
                color: #343a40;
            }
            #subtitleLabel {
                font-size: 18px;
                color: #6c757d;
            }
            QPushButton { /* General buttons in MainMenu */
                font-size: 20px;
                font-weight: bold;
                padding: 15px 25px; 
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 12px;
                min-height: 60px;
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
                padding: 10px 15px;
                min-height: 45px;
            }
            #addUserButton:hover {
                background-color: #334155;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 30, 50, 50) 
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("PuntoLite")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Seleccione el modo de acceso")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button_cashier = QPushButton("🛒 Modo Cajero")
        button_admin = QPushButton("⚙️ Modo Admin")
        
        button_width = 320
        
        for btn in (button_cashier, button_admin):
            btn.setFixedWidth(button_width)

        button_cashier.clicked.connect(lambda: self.show_pin_dialog("Cajero"))
        button_admin.clicked.connect(lambda: self.show_pin_dialog("Administrador"))

        button_layout = QHBoxLayout()
        button_layout.setSpacing(50)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(button_cashier)
        button_layout.addWidget(button_admin)
        
        main_layout.addSpacerItem(QSpacerItem(20, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)) 
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)) 
        main_layout.addLayout(button_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)) 

        footer_layout = QVBoxLayout()
        footer_layout.setSpacing(10)
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        add_user_button = QPushButton("➕ Agregar Usuario")
        add_user_button.setObjectName("addUserButton")
        add_user_button.setFixedWidth(int(button_width * 0.8))
        add_user_button.clicked.connect(self.open_add_user_dialog)

        footer_layout.addWidget(add_user_button)
        main_layout.addLayout(footer_layout)
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)) 

        self.setLayout(main_layout)

    def show_pin_dialog(self, user_type_access_request): # user_type_access_request is "Cajero" or "Administrador"
        dialog = PinDialog(user_type_access_request, self) # Pass the access type for dialog title/label
        if dialog.exec() == QDialog.DialogCode.Accepted:
            nombre_usuario_ingresado, pin_ingresado = dialog.get_credentials()

            if not nombre_usuario_ingresado or not pin_ingresado:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Datos Incompletos")
                msg_box.setText("Debe ingresar nombre de usuario y PIN.")
                msg_box.setIcon(QMessageBox.Icon.Warning)
                msg_box.setStyleSheet("""QMessageBox { background-color: white; color: black; min-width: 300px;} 
                                     QPushButton { background-color: #007bff; color: white; padding: 5px 15px; min-width: 80px;} """)
                msg_box.exec()
                return

            is_valid, user_id, user_name, message = db_manager.validate_user_pin(nombre_usuario_ingresado, pin_ingresado)
            
            if is_valid:
                self.current_user_id = user_id
                self.current_user_name = user_name 
                
                # Here, you might want to check if the user_record['tipo_usuario'] matches user_type_access_request
                # For now, we assume if PIN is valid, access is granted to the mode they clicked.
                # A more robust check would involve getting tipo_usuario from validate_user_pin and comparing.
                # For example, if db_manager.validate_user_pin returned (is_valid, user_id, user_name, user_type_from_db, message)
                # you could do: if user_type_from_db.lower() != user_type_access_request.lower(): ... show error ...

                if user_type_access_request == "Cajero":
                    print(f"Acceso Cajero: {self.current_user_name} (ID: {self.current_user_id}). Abriendo módulo de venta.")
                    if self.ventana_venta_instancia is None:
                        self.ventana_venta_instancia = VentanaPuntoDeVenta(
                            parent_menu=self, 
                            id_usuario_cajero=self.current_user_id,
                            nombre_cajero=self.current_user_name # Pass user name
                        )
                    else:
                        self.ventana_venta_instancia.id_usuario_cajero = self.current_user_id
                        self.ventana_venta_instancia.nombre_cajero = self.current_user_name # Update if instance exists
                        self.ventana_venta_instancia.actualizar_display_cajero() 
                    
                    self.ventana_venta_instancia.showMaximized()
                    self.ventana_venta_instancia.activateWindow()
                    self.hide()
                
                elif user_type_access_request == "Administrador":
                    # Similar logic for admin panel if it existed
                    msg_box_info = QMessageBox(self)
                    msg_box_info.setWindowTitle("Acceso Administrador")
                    msg_box_info.setText(f"Acceso concedido a {self.current_user_name} (ID: {self.current_user_id}). Funcionalidad de admin pendiente.")
                    msg_box_info.setIcon(QMessageBox.Icon.Information)
                    msg_box_info.setStyleSheet("""QMessageBox { background-color: white; color: black; min-width: 300px;} 
                                             QPushButton { background-color: #007bff; color: white; padding: 5px 15px; min-width: 80px;} """)
                    msg_box_info.exec()
                    print(f"Acceso Administrador: {self.current_user_name} (ID: {self.current_user_id}). Panel de Admin pendiente.")
            
            else: # Login failed
                msg_box_warn = QMessageBox(self)
                msg_box_warn.setWindowTitle("Acceso Denegado")
                msg_box_warn.setText(message) # Display message from db_manager
                msg_box_warn.setIcon(QMessageBox.Icon.Warning)
                msg_box_warn.setStyleSheet("""QMessageBox { background-color: white; color: black; min-width: 300px;} 
                                         QPushButton { background-color: #007bff; color: white; padding: 5px 15px; min-width: 80px;} """)
                msg_box_warn.exec()
                print(f"Intento de acceso {user_type_access_request} con Usuario: {nombre_usuario_ingresado}, PIN: {pin_ingresado}. Error: {message}")
            
    def open_add_user_dialog(self):
        dialog = NuevoUsuarioDialog(self)
        # The dialog now handles its own database interaction and messaging for success/failure
        dialog.exec() # No need to check QDialog.DialogCode.Accepted here if dialog handles it

