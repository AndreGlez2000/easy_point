from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                              QDateEdit, QComboBox, QTableWidget, QTableWidgetItem,
                              QPushButton, QLabel, QHeaderView, QDialog, QFrame,
                              QSpacerItem, QSizePolicy, QButtonGroup, QMessageBox, QApplication)
from PySide6.QtCore import Qt, QDate, QSize
from PySide6.QtGui import QIcon, QFont, QPalette, QColor
import sqlite3
from datetime import datetime, date # Ensure date is specifically imported from datetime

class SidebarButton(QPushButton):
    def __init__(self, text, icon_path=None, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(45)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(20, 20))
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding-left: 20px;
                border: none;
                background-color: transparent;
                color: #6c757d;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(0, 123, 255, 0.1);
                color: #007bff;
            }
            QPushButton:checked {
                background-color: rgba(0, 123, 255, 0.15);
                color: #007bff;
                border-left: 4px solid #007bff;
                padding-left: 16px;
            }
        """)
        self.setCheckable(True)

class DetallesVentaDialog(QDialog):
    def __init__(self, id_venta, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Detalles de Venta - {id_venta}")
        self.setMinimumSize(600, 400)
        self.setup_ui(id_venta)
        
    def setup_ui(self, id_venta):
        layout = QVBoxLayout(self)
        
        # Tabla de detalles
        self.tabla_detalles = QTableWidget()
        self.tabla_detalles.setColumnCount(5)
        self.tabla_detalles.setHorizontalHeaderLabels([
            "Producto", "Cantidad", "Precio Unitario", "Subtotal", "Código de Barras"
        ])
        self.tabla_detalles.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.tabla_detalles)
        
        # Cargar detalles
        self.cargar_detalles(id_venta)
        
        # Botón cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.close)
        layout.addWidget(btn_cerrar)
        
    def cargar_detalles(self, id_venta):
        conn = sqlite3.connect("easypoint.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT p.nombre_producto, p.codigo_barras, 
                       dv.cantidad, dv.precio_unitario_venta, dv.subtotal_linea
                FROM DetallesVenta dv
                JOIN Productos p ON dv.id_producto = p.id_producto
                WHERE dv.id_venta = ?
            """, (id_venta,))
            
            detalles = cursor.fetchall()
            self.tabla_detalles.setRowCount(len(detalles))
            
            for row, detalle in enumerate(detalles):
                self.tabla_detalles.setItem(row, 0, QTableWidgetItem(detalle['nombre_producto']))
                self.tabla_detalles.setItem(row, 1, QTableWidgetItem(str(detalle['cantidad'])))
                self.tabla_detalles.setItem(row, 2, QTableWidgetItem(f"${detalle['precio_unitario_venta']:.2f}"))
                self.tabla_detalles.setItem(row, 3, QTableWidgetItem(f"${detalle['subtotal_linea']:.2f}"))
                self.tabla_detalles.setItem(row, 4, QTableWidgetItem(detalle['codigo_barras']))
                
        finally:
            conn.close()

class HistorialVentas(QWidget):
    def __init__(self, parent=None, main_menu_ref=None):
        super().__init__(parent)
        self.setWindowTitle("Historial de Ventas")
        self.main_menu_ref = main_menu_ref
        print(f"HistorialVentas __init__: Received main_menu_ref: {main_menu_ref}, self.main_menu_ref set to: {self.main_menu_ref}") # DEBUG
        self.setup_ui()
        
    def setup_ui(self):
        # Layout principal
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Barra lateral
        sidebar = QFrame()
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-right: 1px solid #dee2e6;
            }
        """)
        sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Título del sistema
        sistema_label = QLabel("Sistema de Inventario")
        sistema_label.setStyleSheet("""
            QLabel {
                padding: 20px;
                font-size: 18px;
                font-weight: bold;
                color: #343a40;
                border-bottom: 1px solid #dee2e6;
                background-color: white;
            }
        """)
        sidebar_layout.addWidget(sistema_label)
        
        # Grupo de botones para asegurar selección única
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        
        # Botones de la barra lateral
        btn_dashboard = SidebarButton("Dashboard", "icons/dashboard.svg")
        btn_inventario = SidebarButton("Inventario", "icons/inventory.svg")
        btn_historial = SidebarButton("Historial de Ventas", "icons/history.svg")
        btn_analisis = SidebarButton("Análisis de Ventas", "icons/analysis.svg")
        btn_copias = SidebarButton("Copias de seguridad", "icons/backup.svg")
        btn_config = SidebarButton("Configuración", "icons/settings.svg")
        
        # Agregar botones al grupo
        self.button_group.addButton(btn_dashboard)
        self.button_group.addButton(btn_inventario)
        self.button_group.addButton(btn_historial)
        self.button_group.addButton(btn_analisis)
        self.button_group.addButton(btn_copias)
        self.button_group.addButton(btn_config)
        
        # Marcar el botón activo
        btn_historial.setChecked(True)
        
        sidebar_layout.addWidget(btn_dashboard)
        sidebar_layout.addWidget(btn_inventario)
        sidebar_layout.addWidget(btn_historial)
        sidebar_layout.addWidget(btn_analisis)
        sidebar_layout.addWidget(btn_copias)
        sidebar_layout.addWidget(btn_config)
        
        # Espaciador para empujar el botón de cerrar sesión hacia abajo
        sidebar_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # Botón de cerrar sesión
        btn_cerrar_sesion = QPushButton("Cerrar Sesión")
        btn_cerrar_sesion.setStyleSheet("""
            QPushButton {
                margin: 15px;
                padding: 10px;
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        btn_cerrar_sesion.clicked.connect(self.cerrar_sesion)
        sidebar_layout.addWidget(btn_cerrar_sesion)
        
        # Contenido principal
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: white;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)
        
        # Título de la página y rol
        title_layout = QHBoxLayout()
        
        # Contenedor izquierdo para el título
        title_container = QWidget()
        title_container_layout = QVBoxLayout(title_container)
        title_container_layout.setContentsMargins(0, 0, 0, 0)
        title_container_layout.setSpacing(5)
        
        page_title = QLabel("Historial de Ventas")
        page_title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #343a40;
            }
        """)
        
        # Etiqueta de Administrador
        admin_label = QLabel("Administrador")
        admin_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 14px;
            }
        """)
        
        title_container_layout.addWidget(page_title)
        title_container_layout.addWidget(admin_label)
        
        title_layout.addWidget(title_container)
        title_layout.addStretch()
        
        content_layout.addLayout(title_layout)
        
        # Barra de filtros
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)
        
        # Búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por cajero o ID...")
        self.search_input.textChanged.connect(self.filtrar_ventas)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                min-width: 250px;
                font-size: 14px;
                color: #495057; /* Added text color */
            }
            QLineEdit:focus {
                border-color: #80bdff;
                outline: 0;
                box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
            }
        """)
        
        # Filtro de fecha
        self.date_filter = QDateEdit()
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.dateChanged.connect(self.filtrar_ventas)
        self.date_filter.setStyleSheet("""
            QDateEdit {
                padding: 8px 12px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                min-width: 150px;
                font-size: 14px;
                color: #495057; /* Added text color */
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #ced4da;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QDateEdit::down-arrow {
                image: url(icons/dropdown.svg); /* Ensure you have a dropdown icon */
                width: 10px;
                height: 10px;
            }
            QCalendarWidget QWidget { /* Calendar background */
                alternate-background-color: #f8f9fa;
                background-color: white;
                color: #212529;
            }
            QCalendarWidget QAbstractItemView:enabled { /* Calendar day numbers */
                color: #212529;
                selection-background-color: #007bff;
                selection-color: white;
            }
            QCalendarWidget QToolButton { /* Calendar month/year buttons */
                color: #212529;
                background-color: transparent;
                border: none;
                margin: 5px;
                padding: 5px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #e9ecef;
            }
            QCalendarWidget QSpinBox { /* Calendar year spinbox */
                color: #212529;
                background-color: white;
                border: 1px solid #ced4da;
                padding: 2px;
            }
            QCalendarWidget QSpinBox::up-button, QCalendarWidget QSpinBox::down-button {
                 subcontrol-origin: border;
                 width: 16px;
                 border-width: 1px;
            }
            QCalendarWidget QAbstractItemView:disabled { color: #adb5bd; } /* Disabled dates */
            QCalendarWidget QHeaderView { background-color: #e9ecef; } /* Day names header */
        """)
        
        # Ordenamiento
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Más recientes primero", "Más antiguos primero"])
        self.sort_combo.currentTextChanged.connect(self.filtrar_ventas)
        self.sort_combo.setStyleSheet("""
            QComboBox {
                padding: 8px 12px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                min-width: 180px;
                font-size: 14px;
                color: #495057; /* Added text color */
                background-color: white; /* Added background color */
            }
            QComboBox QAbstractItemView { /* Dropdown list items */
                color: #212529;
                background-color: white;
                selection-background-color: #007bff;
                selection-color: white;
                border: 1px solid #ced4da;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(icons/dropdown.svg);
                width: 12px;
                height: 12px;
            }
        """)
        
        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(self.date_filter)
        filter_layout.addWidget(self.sort_combo)
        filter_layout.addStretch()

        # Botón para resetear filtros
        self.reset_filters_button = QPushButton("Resetear Filtros")
        self.reset_filters_button.clicked.connect(self.reset_filters_and_reload)
        self.reset_filters_button.setStyleSheet("""
            QPushButton {
                padding: 8px 12px;
                border: 1px solid #6c757d;
                border-radius: 4px;
                font-size: 14px;
                color: #495057;
                background-color: #f8f9fa;
            }
            QPushButton:hover {
                background-color: #e2e6ea;
                border-color: #545b62;
            }
        """)
        filter_layout.addWidget(self.reset_filters_button)
        
        content_layout.addLayout(filter_layout)
        
        # Tabla de ventas
        self.tabla_ventas = QTableWidget()
        self.tabla_ventas.setColumnCount(5)
        self.tabla_ventas.setHorizontalHeaderLabels([
            "ID Venta", "Fecha", "Cajero", "Productos", "Total"
        ])
        self.tabla_ventas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_ventas.verticalHeader().setVisible(False)
        self.tabla_ventas.setStyleSheet("""
            QTableWidget {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
                gridline-color: #dee2e6;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #dee2e6;
                color: #212529; /* Explicitly set text color for items */
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 12px 8px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
                color: #495057;
                font-size: 14px;
            }
            QTableWidget::item:selected {
                background-color: #e8f0fe;
                color: #000;
            }
        """)
        
        content_layout.addWidget(self.tabla_ventas)
        
        # Agregar sidebar y contenido al layout principal
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_widget)

        # Botón de Regreso al Menú Principal
        self.back_to_main_menu_button = QPushButton("← Volver al Menú Principal")
        self.back_to_main_menu_button.clicked.connect(self.go_to_main_menu)
        self.back_to_main_menu_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                font-weight: 500;
                padding: 10px 15px;
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        content_layout.addWidget(self.back_to_main_menu_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        # Cargar ventas iniciales
        self.cargar_ventas() # This should call filtrar_ventas with default/initial filter settings
        
    def cargar_ventas(self):
        # Load all sales from all dates, sorted by most recent, on initial load.
        self.filtrar_ventas(show_all_dates=True)
            
    def filtrar_ventas(self, show_all_dates=False): # Added show_all_dates parameter
        busqueda = self.search_input.text().lower()
        q_date_obj = self.date_filter.date()
        
        fecha_dt_obj = None
        fecha_str = None
        if not show_all_dates: # Only prepare date string if not showing all dates
            if q_date_obj.isValid():
                fecha_dt_obj = date(q_date_obj.year(), q_date_obj.month(), q_date_obj.day())
            else:
                fecha_dt_obj = date.today() 
            fecha_str = fecha_dt_obj.strftime('%Y-%m-%d')
        
        orden = "DESC" if self.sort_combo.currentText() == "Más recientes primero" else "ASC"
        
        conn = None 
        try:
            conn = sqlite3.connect("easypoint.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query_parts = [
                "SELECT v.id_venta, v.fecha_venta, u.nombre_usuario as cajero,",
                "COUNT(dv.id_detalle_venta) as num_productos,",
                "v.total_venta",
                "FROM Ventas v",
                "JOIN Usuarios u ON v.id_usuario_cajero = u.id_usuario",
                "JOIN DetallesVenta dv ON v.id_venta = dv.id_venta"
            ]
            
            conditions = []
            params = []

            if not show_all_dates and fecha_str:
                conditions.append("DATE(v.fecha_venta) = ?")
                params.append(fecha_str)

            if busqueda: 
                conditions.append("(LOWER(u.nombre_usuario) LIKE ? OR LOWER(CAST(v.id_venta AS TEXT)) LIKE ?)")
                params.append(f"%{busqueda}%") 
                params.append(f"%{busqueda}%")
            
            if conditions:
                query_parts.append("WHERE " + " AND ".join(conditions))
            
            query_parts.append("GROUP BY v.id_venta")
            query_parts.append(f"ORDER BY v.fecha_venta {orden}")
            
            final_query = " ".join(query_parts)
            
            cursor.execute(final_query, tuple(params))
            ventas = cursor.fetchall()
            
            self.tabla_ventas.setRowCount(0) 
            self.tabla_ventas.setRowCount(len(ventas))
            
            # Ensure the loop for populating self.tabla_ventas does not attempt to add a 6th column (actions)
            for row, venta_data in enumerate(ventas):
                # ID Venta
                id_venta_formatted = f"V{str(venta_data['id_venta']).zfill(4)}"
                item_id = QTableWidgetItem(id_venta_formatted)
                item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_ventas.setItem(row, 0, item_id)
                
                # Fecha
                fecha_db_dt = datetime.strptime(venta_data['fecha_venta'], '%Y-%m-%d %H:%M:%S')
                fecha_formatted = fecha_db_dt.strftime('%d/%m/%Y %H:%M')
                item_fecha = QTableWidgetItem(fecha_formatted)
                item_fecha.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_ventas.setItem(row, 1, item_fecha)
                
                # Cajero
                item_cajero = QTableWidgetItem(venta_data['cajero'])
                item_cajero.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_ventas.setItem(row, 2, item_cajero)
                
                # Número de productos
                item_productos = QTableWidgetItem(str(venta_data['num_productos']))
                item_productos.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_ventas.setItem(row, 3, item_productos)
                
                # Total
                total_formatted = f"${venta_data['total_venta']:.2f}"
                item_total = QTableWidgetItem(total_formatted)
                item_total.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_ventas.setItem(row, 4, item_total)
        finally:
            if conn:
                conn.close()

    def mostrar_detalles(self, id_venta):
        dialog = DetallesVentaDialog(id_venta, self)
        dialog.exec()

    def reset_filters_and_reload(self):
        self.search_input.clear()
        self.date_filter.setDate(QDate.currentDate()) # Visually reset, but will be ignored by query
        self.sort_combo.setCurrentIndex(0) # "Más recientes primero"
        self.filtrar_ventas(show_all_dates=True) # Reload data showing all dates

    def go_to_main_menu(self):
        print(f"HistorialVentas go_to_main_menu: Current self.main_menu_ref: {self.main_menu_ref}") # DEBUG
        if self.main_menu_ref:
            self.main_menu_ref.show()
            # Ensure the main menu is maximized and activated
            try:
                # Qt.WindowState.WindowMaximized is preferred for PySide6
                maximized_state = Qt.WindowState.WindowMaximized if hasattr(Qt.WindowState, 'WindowMaximized') else Qt.WindowMaximized
                self.main_menu_ref.setWindowState(maximized_state)
            except AttributeError:
                print("Warning: main_menu_ref does not have setWindowState method or Qt.WindowState is not fully available.")
            
            try:
                self.main_menu_ref.activateWindow()
            except AttributeError:
                print("Warning: main_menu_ref does not have activateWindow method.")

            self.close()
        else:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Error de Navegación")
            msg_box.setText("No se pudo volver al menú principal. Referencia no encontrada.")
            msg_box.exec()

    def cerrar_sesion(self):
        current_window = self.window()
        if current_window:
            current_window.close()