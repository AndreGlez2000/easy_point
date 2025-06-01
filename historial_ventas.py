from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                              QDateEdit, QComboBox, QTableWidget, QTableWidgetItem,
                              QPushButton, QLabel, QHeaderView, QDialog, QFrame,
                              QSpacerItem, QSizePolicy, QButtonGroup)
from PySide6.QtCore import Qt, QDate, QSize
from PySide6.QtGui import QIcon, QFont, QPalette, QColor
import sqlite3
from datetime import datetime, timezone, timedelta

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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sistema de Inventario")
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
            }
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
        
        content_layout.addLayout(filter_layout)
        
        # Tabla de ventas
        self.tabla_ventas = QTableWidget()
        self.tabla_ventas.setColumnCount(6)
        self.tabla_ventas.setHorizontalHeaderLabels([
            "ID Venta", "Fecha", "Cajero", "Productos", "Total", "Acciones"
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
        
        # Cargar ventas iniciales
        self.cargar_ventas()
        
    def cargar_ventas(self):
        conn = sqlite3.connect("easypoint.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT v.id_venta, v.fecha_venta, u.nombre_usuario as cajero,
                       COUNT(dv.id_detalle_venta) as num_productos,
                       v.total_venta
                FROM Ventas v
                JOIN Usuarios u ON v.id_usuario_cajero = u.id_usuario
                JOIN DetallesVenta dv ON v.id_venta = dv.id_venta
                GROUP BY v.id_venta
                ORDER BY v.fecha_venta DESC
            """)
            
            ventas = cursor.fetchall()
            self.tabla_ventas.setRowCount(len(ventas))
            
            for row, venta in enumerate(ventas):
                # ID Venta (con formato V001, V002, etc.)
                id_venta_formatted = f"V{str(venta['id_venta']).zfill(4)}"
                item_id = QTableWidgetItem(id_venta_formatted)
                item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_ventas.setItem(row, 0, item_id)
                
                # Fecha - asumimos que la fecha está en hora local
                fecha = datetime.strptime(venta['fecha_venta'], '%Y-%m-%d %H:%M:%S')
                fecha_formatted = fecha.strftime('%d/%m/%Y %H:%M')
                item_fecha = QTableWidgetItem(fecha_formatted)
                item_fecha.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_ventas.setItem(row, 1, item_fecha)
                
                # Cajero
                item_cajero = QTableWidgetItem(venta['cajero'])
                item_cajero.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_ventas.setItem(row, 2, item_cajero)
                
                # Número de productos
                item_productos = QTableWidgetItem(str(venta['num_productos']))
                item_productos.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_ventas.setItem(row, 3, item_productos)
                
                # Total
                total_formatted = f"${venta['total_venta']:.2f}"
                item_total = QTableWidgetItem(total_formatted)
                item_total.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_ventas.setItem(row, 4, item_total)
                
                # Botón Ver Detalles
                btn_detalles = QPushButton("Ver Detalles")
                btn_detalles.setStyleSheet("""
                    QPushButton {
                        background-color: #28a745;
                        color: white;
                        border: none;
                        padding: 5px 10px;
                        border-radius: 4px;
                        font-size: 13px;
                        font-weight: 500;
                    }
                    QPushButton:hover {
                        background-color: #218838;
                    }
                """)
                btn_detalles.clicked.connect(lambda checked, v=venta['id_venta']: self.mostrar_detalles(v))
                self.tabla_ventas.setCellWidget(row, 5, btn_detalles)
                
        finally:
            conn.close()
            
    def filtrar_ventas(self):
        # Obtener valores de filtros
        busqueda = self.search_input.text().lower()
        fecha = self.date_filter.date().toPython()
        orden = "DESC" if self.sort_combo.currentText() == "Más recientes primero" else "ASC"
        
        conn = sqlite3.connect("easypoint.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            # Construir la consulta base
            query = """
                SELECT v.id_venta, v.fecha_venta, u.nombre_usuario as cajero,
                       COUNT(dv.id_detalle_venta) as num_productos,
                       v.total_venta
                FROM Ventas v
                JOIN Usuarios u ON v.id_usuario_cajero = u.id_usuario
                JOIN DetallesVenta dv ON v.id_venta = dv.id_venta
                WHERE DATE(v.fecha_venta) = DATE(?)
                AND (LOWER(u.nombre_usuario) LIKE ? OR v.id_venta LIKE ?)
                GROUP BY v.id_venta
                ORDER BY v.fecha_venta """ + orden
                
            cursor.execute(query, (fecha, f"%{busqueda}%", f"%{busqueda}%"))
            
            ventas = cursor.fetchall()
            self.tabla_ventas.setRowCount(len(ventas))
            
            for row, venta in enumerate(ventas):
                # Llenar la tabla igual que en cargar_ventas()
                id_venta_formatted = f"V{str(venta['id_venta']).zfill(4)}"
                item_id = QTableWidgetItem(id_venta_formatted)
                item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_ventas.setItem(row, 0, item_id)
                
                fecha = datetime.strptime(venta['fecha_venta'], '%Y-%m-%d %H:%M:%S')
                fecha_formatted = fecha.strftime('%d/%m/%Y %H:%M')
                item_fecha = QTableWidgetItem(fecha_formatted)
                item_fecha.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_ventas.setItem(row, 1, item_fecha)
                
                item_cajero = QTableWidgetItem(venta['cajero'])
                item_cajero.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_ventas.setItem(row, 2, item_cajero)
                
                item_productos = QTableWidgetItem(str(venta['num_productos']))
                item_productos.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_ventas.setItem(row, 3, item_productos)
                
                total_formatted = f"${venta['total_venta']:.2f}"
                item_total = QTableWidgetItem(total_formatted)
                item_total.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabla_ventas.setItem(row, 4, item_total)
                
                btn_detalles = QPushButton("Ver Detalles")
                btn_detalles.setStyleSheet("""
                    QPushButton {
                        background-color: #28a745;
                        color: white;
                        border: none;
                        padding: 5px 10px;
                        border-radius: 4px;
                        font-size: 13px;
                        font-weight: 500;
                    }
                    QPushButton:hover {
                        background-color: #218838;
                    }
                """)
                btn_detalles.clicked.connect(lambda checked, v=venta['id_venta']: self.mostrar_detalles(v))
                self.tabla_ventas.setCellWidget(row, 5, btn_detalles)
                
        finally:
            conn.close()
            
    def mostrar_detalles(self, id_venta):
        dialog = DetallesVentaDialog(id_venta, self)
        dialog.exec()

    def cerrar_sesion(self):
        from main_menu import MainMenu
        self.menu_principal = MainMenu()
        self.menu_principal.show()
        self.close()

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Establecer la fuente predeterminada
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    ventana = HistorialVentas()
    ventana.resize(1200, 800)
    ventana.show()
    
    sys.exit(app.exec()) 