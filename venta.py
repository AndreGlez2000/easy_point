import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QSpacerItem, QSizePolicy, QFrame,
    QCompleter, QMessageBox # <<<--- ADDED QCompleter, QMessageBox
)
from PySide6.QtCore import Qt, QSize, QStringListModel # <<<--- ADDED QStringListModel
from PySide6.QtGui import QIcon, QIntValidator
import db_manager # <<<--- IMPORT DB MANAGER

class VentanaPuntoDeVenta(QMainWindow):
    def __init__(self, parent_menu=None, id_usuario_cajero=None, nombre_cajero=None): # Added nombre_cajero
        super().__init__()
        self.parent_menu = parent_menu 
        self.id_usuario_cajero = id_usuario_cajero
        self.nombre_cajero = nombre_cajero # <<<--- STORE CASHIER NAME
        self.setWindowTitle("Punto de Venta")
        self.product_suggestions_map = {} # <<<--- INITIALIZE ATTRIBUTE HERE
        # self.setGeometry(100, 100, 1200, 700) # Maximized will handle size

        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout(widget_central)

        self.crear_barra_superior(layout_principal)

        layout_contenido = QHBoxLayout()
        layout_principal.addLayout(layout_contenido)

        self.crear_panel_derecho(layout_contenido)
        self.crear_panel_izquierdo(layout_contenido)

        self.productos_en_tabla = {} # To keep track of product_id and row index
        self.setup_product_completer() # <<<--- CALL COMPLETER SETUP

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
            }
            QPushButton {
                font-size: 14px;
                padding: 8px 15px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                background-color: white;
                color: #333333;
            }
            QTableWidget {
                font-size: 13px;
                border: 1px solid #ccc;
                background-color: white;
                color: #333333;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 5px;
                border: 1px solid #ccc;
                font-size: 14px;
                font-weight: bold;
                color: #333333;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                background-color: white;
                color: #333333;
            }
            QFrame[frameShape="4"], /* QFrame.HLine */
            QFrame[frameShape="5"]  /* QFrame.VLine */
            {
                border: none;
                background-color: #cccccc;
            }
            QFrame[frameShape="4"] { max-height: 1px; min-height: 1px; }
            QFrame[frameShape="5"] { max-width: 1px; min-width: 1px; }

            #barraSuperiorWidget {
                background-color: #343a40;
                color: white;
                padding: 10px;
            }
            #barraSuperiorWidget QLabel { color: white; }
            #barraSuperiorWidget QPushButton {
                background-color: #6c757d;
                border-color: #6c757d;
                color: white;
            }
            #barraSuperiorWidget QPushButton:hover { background-color: #5a6268; }
            
            #botonRegresar { /* Style for the new return button */
                background-color: #17a2b8; /* Info color (teal) */
                border-color: #17a2b8;
                margin-right: 10px; /* Space before Salir button */
            }
            #botonRegresar:hover {
                background-color: #138496;
            }
            #botonSalir {
                background-color: #dc3545;
                border-color: #dc3545;
            }
            #botonSalir:hover { background-color: #c82333; }

            #panelIzquierdoWidget, #panelDerechoWidget {
                background-color: white;
                border-radius: 5px;
            }
            #labelNoProductos {
                font-style: italic;
                color: #6c757d;
                margin-top: 20px;
                margin-bottom: 20px;
            }
            #labelInstruccionesTexto {
                background-color: #e9ecef;
                padding: 10px;
                border-radius: 4px;
                margin-bottom: 10px;
                color: #333333;
            }
            #labelCambioValor {
                font-weight: bold;
                font-size: 16px;
                color: #28a745;
            }
            #labelCambioValor[text^="Falta"] { color: #dc3545; }
            #labelCambioValor[text="Inválido"] { color: #ffc107; }
            QTableWidget QPushButton {
                font-size: 16px;
                padding: 0px;
                background-color: #007bff;
                color: white;
                border-radius: 3px;
                min-width: 25px; max-width: 25px;
                min-height: 25px; max-height: 25px;
            }
            QTableWidget QPushButton:hover { background-color: #0056b3; }

            /* Styling for QCompleter popup */
            QCompleter QAbstractItemView {
                background-color: white;
                color: black; /* Text color for items */
                border: 1px solid #ccc; /* Optional: border for the popup */
                selection-background-color: #007bff; /* Background for selected item */
                selection-color: white; /* Text color for selected item */
                font-size: 13px; /* Match other font sizes */
            }
            QCompleter QAbstractItemView::item {
                padding: 4px 8px; /* Padding for each item */
            }
        """)

    def crear_barra_superior(self, layout_principal):
        widget_barra_superior = QWidget()
        widget_barra_superior.setObjectName("barraSuperiorWidget")
        layout_barra_superior = QHBoxLayout(widget_barra_superior)
        layout_barra_superior.setContentsMargins(10, 0, 10, 0)

        titulo_app = QLabel("PuntoLite")
        titulo_app.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.label_cajero_actual = QLabel(f"Cajero: {self.nombre_cajero if self.nombre_cajero else 'N/A'}") # <<<--- CAJERO LABEL
        self.label_cajero_actual.setStyleSheet("font-size: 14px; margin-left: 20px;")

        boton_regresar = QPushButton("❮ Regresar al Menú")
        boton_regresar.setObjectName("botonRegresar")
        boton_regresar.clicked.connect(self.regresar_al_menu)

        boton_salir = QPushButton("Salir")
        boton_salir.setFixedWidth(80)
        boton_salir.setObjectName("botonSalir")
        boton_salir.clicked.connect(self.close) # Close app or just window? For now, window.

        layout_barra_superior.addWidget(titulo_app)
        layout_barra_superior.addWidget(self.label_cajero_actual) # <<<--- ADD CAJERO LABEL TO BAR
        layout_barra_superior.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout_barra_superior.addWidget(boton_regresar)
        layout_barra_superior.addWidget(boton_salir)

        layout_principal.addWidget(widget_barra_superior)

    def actualizar_display_cajero(self):
        """Updates the cashier name display if the window is reused."""
        if hasattr(self, 'label_cajero_actual'):
            self.label_cajero_actual.setText(f"Cajero: {self.nombre_cajero if self.nombre_cajero else 'N/A'}")

    def regresar_al_menu(self): # New method to handle return
        self.close()
        if self.parent_menu:
            self.parent_menu.show() # <<<--- ENSURE IT'S VISIBLE FIRST
            self.parent_menu.setWindowState(Qt.WindowState.WindowMaximized) # <<<--- THEN SET STATE TO MAXIMIZED
            self.parent_menu.activateWindow() # <<<--- BRING TO FOREGROUND

    def crear_panel_izquierdo(self, layout_contenedor):
        widget_panel_izquierdo = QWidget()
        widget_panel_izquierdo.setObjectName("panelIzquierdoWidget")
        layout_panel_izquierdo = QVBoxLayout(widget_panel_izquierdo)
        layout_panel_izquierdo.setContentsMargins(15, 15, 15, 15)
        layout_panel_izquierdo.setSpacing(15)

        label_productos_venta = QLabel("Productos en Venta")
        label_productos_venta.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout_panel_izquierdo.addWidget(label_productos_venta)

        layout_busqueda = QHBoxLayout()
        self.input_codigo_barras = QLineEdit()
        self.input_codigo_barras.setPlaceholderText("Buscar por código o nombre...")
        self.input_codigo_barras.returnPressed.connect(self.procesar_enter_en_busqueda_producto) # Connect Enter key
        layout_busqueda.addWidget(self.input_codigo_barras, 4)

        self.boton_agregar_producto = QPushButton("➕ Agregar") # Changed icon/text
        self.boton_agregar_producto.setFixedWidth(120)
        self.boton_agregar_producto.clicked.connect(self.buscar_y_agregar_producto_click) # Connect button click
        layout_busqueda.addWidget(self.boton_agregar_producto, 1)
        layout_panel_izquierdo.addLayout(layout_busqueda)

        self.tabla_productos = QTableWidget()
        self.tabla_productos.setColumnCount(7) # <<<--- INCREASED COLUMN COUNT FOR DELETE BUTTON
        self.tabla_productos.setHorizontalHeaderLabels(["ID", "Nombre", "Cantidad", "", "Precio", "Subtotal", "Acción"]) # Added "Acción" header
        self.tabla_productos.setColumnHidden(0, True) # Hide ID column
        self.tabla_productos.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch) # Nombre
        self.tabla_productos.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive) # Cantidad
        self.tabla_productos.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed) # Botones +/- 
        self.tabla_productos.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Interactive) # Precio
        self.tabla_productos.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Interactive) # Subtotal
        self.tabla_productos.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed) # Acción (Delete button)
        self.tabla_productos.setColumnWidth(2, 80) # Cantidad
        self.tabla_productos.setColumnWidth(3, 70) # Botones +/-
        self.tabla_productos.setColumnWidth(4, 100) # Precio
        self.tabla_productos.setColumnWidth(5, 100) # Subtotal
        self.tabla_productos.setColumnWidth(6, 80) # Acción (Delete button)
        self.tabla_productos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout_panel_izquierdo.addWidget(self.tabla_productos)

        self.label_no_productos = QLabel("No hay productos en la venta actual.")
        self.label_no_productos.setObjectName("labelNoProductos")
        self.label_no_productos.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_panel_izquierdo.addWidget(self.label_no_productos)

        linea_separadora_izq_1 = QFrame()
        linea_separadora_izq_1.setFrameShape(QFrame.Shape.HLine)
        linea_separadora_izq_1.setFrameShadow(QFrame.Shadow.Sunken)
        layout_panel_izquierdo.addWidget(linea_separadora_izq_1)

        layout_resumen_venta_1 = QVBoxLayout()
        layout_resumen_venta_1.setSpacing(5)

        # Inicializar los valores a $0.00
        self.label_subtotal_izq = self.crear_fila_resumen(layout_resumen_venta_1, "Subtotal:", "$0.00")
        # self.label_iva_izq = self.crear_fila_resumen(layout_resumen_venta_1, "IVA (16%):", "$0.00") # IVA REMOVED
        self.label_total_izq = self.crear_fila_resumen(layout_resumen_venta_1, "Total:", "$0.00", bold=True)

        layout_panel_izquierdo.addLayout(layout_resumen_venta_1)
        layout_panel_izquierdo.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        layout_botones_accion_1 = QHBoxLayout()
        layout_botones_accion_1.setSpacing(10)

        boton_cancelar_venta_1 = QPushButton("Cancelar Venta")
        boton_cancelar_venta_1.setStyleSheet("""
            QPushButton { background-color: #ffc107; color: black; border-color: #ffc107; }
            QPushButton:hover { background-color: #e0a800; }
        """)
        layout_botones_accion_1.addWidget(boton_cancelar_venta_1)

        boton_finalizar_venta_1 = QPushButton("Finalizar Venta")
        boton_finalizar_venta_1.setStyleSheet("""
            QPushButton { background-color: #28a745; border-color: #28a745; }
            QPushButton:hover { background-color: #218838; }
        """)
        boton_finalizar_venta_1.clicked.connect(self.finalizar_venta) # <<<--- CONNECT TO finalizar_venta
        layout_botones_accion_1.addWidget(boton_finalizar_venta_1)
        layout_panel_izquierdo.addLayout(layout_botones_accion_1)

        layout_contenedor.addWidget(widget_panel_izquierdo, 2)
        self.actualizar_visibilidad_no_productos()

    def agregar_fila_producto(self, id_producto, nombre, cantidad, precio):
        # Check if product already in table
        if id_producto in self.productos_en_tabla:
            fila_existente = self.productos_en_tabla[id_producto]
            input_cantidad_widget = self.tabla_productos.cellWidget(fila_existente, 2) # Column index for Cantidad
            if isinstance(input_cantidad_widget, QLineEdit):
                try:
                    cantidad_actual = int(input_cantidad_widget.text())
                    # Check stock before increasing quantity (optional, but good practice)
                    # producto_db = db_manager.get_product_by_id(id_producto)
                    # if producto_db and (cantidad_actual + cantidad) > producto_db['stock_actual']:
                    #     self.show_styled_message_box("Stock Insuficiente", f"No hay suficiente stock para agregar más unidades de {nombre}. Stock actual: {producto_db['stock_actual']}", QMessageBox.Icon.Warning)
                    #     return
                    nueva_cantidad = cantidad_actual + cantidad # Add to existing quantity
                    input_cantidad_widget.setText(str(nueva_cantidad))
                    self.actualizar_subtotal_fila(fila_existente)
                except ValueError:
                    pass # Should not happen if validator is set
            return # Product already exists, quantity updated

        # Check stock before adding new product row
        producto_db = db_manager.get_product_by_id(id_producto)
        if not producto_db or cantidad > producto_db['stock_actual']:
            stock_disponible = producto_db['stock_actual'] if producto_db else 0
            self.show_styled_message_box("Stock Insuficiente", f"No hay suficiente stock para '{nombre}'. Stock disponible: {stock_disponible}", QMessageBox.Icon.Warning)
            return

        rowCount = self.tabla_productos.rowCount()
        self.tabla_productos.insertRow(rowCount)

        # Store product ID in hidden column 0
        id_item = QTableWidgetItem(str(id_producto))
        self.tabla_productos.setItem(rowCount, 0, id_item)

        self.tabla_productos.setItem(rowCount, 1, QTableWidgetItem(nombre)) # Nombre in column 1

        input_cantidad_item_solo = QLineEdit(str(cantidad))
        input_cantidad_item_solo.setValidator(QIntValidator(1, 999))
        input_cantidad_item_solo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_cantidad_item_solo.textChanged.connect(lambda text, r=rowCount, prod_id=id_producto: self.actualizar_subtotal_fila(r, prod_id))
        self.tabla_productos.setCellWidget(rowCount, 2, input_cantidad_item_solo) # Cantidad in column 2

        widget_botones_cant = QWidget()
        layout_botones_cant = QHBoxLayout(widget_botones_cant)
        layout_botones_cant.setContentsMargins(0,0,0,0)
        layout_botones_cant.setSpacing(2)
        boton_menos_sep = QPushButton("-")
        boton_menos_sep.setFixedSize(QSize(25,25)) 
        boton_menos_sep.clicked.connect(lambda _, r=rowCount, prod_id=id_producto: self.modificar_cantidad(r, -1, prod_id))
        boton_mas_sep = QPushButton("+")
        boton_mas_sep.setFixedSize(QSize(25,25)) 
        boton_mas_sep.clicked.connect(lambda _, r=rowCount, prod_id=id_producto: self.modificar_cantidad(r, 1, prod_id))
        layout_botones_cant.addWidget(boton_menos_sep)
        layout_botones_cant.addWidget(boton_mas_sep)
        layout_botones_cant.addStretch()
        self.tabla_productos.setCellWidget(rowCount, 3, widget_botones_cant) # +/- buttons in column 3

        self.tabla_productos.setItem(rowCount, 4, QTableWidgetItem(f"${precio:.2f}")) # Precio in column 4
        subtotal = cantidad * precio
        self.tabla_productos.setItem(rowCount, 5, QTableWidgetItem(f"${subtotal:.2f}")) # Subtotal in column 5

        # Add Delete button to column 6
        boton_eliminar_producto = QPushButton("🗑️") # Delete icon
        boton_eliminar_producto.setToolTip("Eliminar producto de la venta")
        boton_eliminar_producto.setStyleSheet("background-color: #dc3545; font-size: 14px; padding: 3px;")
        boton_eliminar_producto.clicked.connect(lambda _, r=rowCount, prod_id=id_producto: self.eliminar_producto_de_venta(r, prod_id))
        self.tabla_productos.setCellWidget(rowCount, 6, boton_eliminar_producto)

        for col in [1, 4, 5]: # Align text for visible columns
            item = self.tabla_productos.item(rowCount, col)
            if item:
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.productos_en_tabla[id_producto] = rowCount # Track product by ID and its row

        self.actualizar_totales_venta()
        self.actualizar_visibilidad_no_productos()

    def modificar_cantidad(self, fila, delta, id_producto):
        input_cantidad_widget = self.tabla_productos.cellWidget(fila, 2) # Cantidad column is 2
        if isinstance(input_cantidad_widget, QLineEdit):
            try:
                cantidad_actual = int(input_cantidad_widget.text())
                nueva_cantidad = max(1, cantidad_actual + delta)

                # Check stock before increasing quantity
                if delta > 0:
                    producto_db = db_manager.get_product_by_id(id_producto)
                    if producto_db and nueva_cantidad > producto_db['stock_actual']:
                        self.show_styled_message_box("Stock Insuficiente", f"No hay suficiente stock para '{producto_db['nombre_producto']}'. Stock disponible: {producto_db['stock_actual']}", QMessageBox.Icon.Warning)
                        return # Don't change quantity if not enough stock

                input_cantidad_widget.setText(str(nueva_cantidad))
                # self.actualizar_subtotal_fila(fila, id_producto) # Already connected via textChanged
            except ValueError:
                input_cantidad_widget.setText("1")

    def actualizar_subtotal_fila(self, fila, id_producto=None): # id_producto for stock check if needed
        input_cantidad_widget = self.tabla_productos.cellWidget(fila, 2) # Cantidad column is 2
        item_precio = self.tabla_productos.item(fila, 4) # Precio column is 4

        if isinstance(input_cantidad_widget, QLineEdit) and item_precio:
            try:
                cantidad = int(input_cantidad_widget.text())
                # Optional: Stock check when quantity is manually typed
                if id_producto:
                    producto_db = db_manager.get_product_by_id(id_producto)
                    if producto_db and cantidad > producto_db['stock_actual']:
                        self.show_styled_message_box(
                            "Stock Insuficiente", 
                            f"Cantidad excede stock para '{producto_db['nombre_producto']}' (Stock: {producto_db['stock_actual']}). Ajustando a máximo disponible.", 
                            QMessageBox.Icon.Warning
                        )
                        cantidad = producto_db['stock_actual']
                        input_cantidad_widget.setText(str(cantidad)) # Auto-adjust to max stock
                        if cantidad == 0: # If max stock is 0, effectively removes or prevents adding
                            # self.eliminar_producto_de_venta(fila, id_producto) # Could auto-remove
                            # For now, just sets subtotal to 0 and relies on user to remove if needed
                            self.tabla_productos.setItem(fila, 5, QTableWidgetItem("$0.00"))
                            self.actualizar_totales_venta()
                            return

                precio_str = item_precio.text().replace('$', '')
                precio = float(precio_str)
                subtotal = cantidad * precio
                self.tabla_productos.setItem(fila, 5, QTableWidgetItem(f"${subtotal:.2f}")) # Subtotal column is 5
                item_subtotal = self.tabla_productos.item(fila,5)
                if item_subtotal:
                    item_subtotal.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            except ValueError:
                self.tabla_productos.setItem(fila, 5, QTableWidgetItem("$0.00"))
        self.actualizar_totales_venta()
    
    def actualizar_totales_venta(self):
        subtotal_general = 0.0
        for fila in range(self.tabla_productos.rowCount()):
            item_subtotal_fila = self.tabla_productos.item(fila, 5) # Subtotal column is 5
            if item_subtotal_fila:
                try:
                    subtotal_general += float(item_subtotal_fila.text().replace('$', ''))
                except ValueError:
                    pass

        # iva = subtotal_general * 0.16 # IVA REMOVED
        total = subtotal_general # Total is now just subtotal

        if hasattr(self, 'label_subtotal_izq'):
            self.label_subtotal_izq.setText(f"${subtotal_general:.2f}")
        # if hasattr(self, 'label_iva_izq'): # IVA REMOVED
        #     self.label_iva_izq.setText(f"${iva:.2f}")
        if hasattr(self, 'label_total_izq'):
            self.label_total_izq.setText(f"${total:.2f}")

        if hasattr(self, 'label_subtotal_der'):
            self.label_subtotal_der.setText(f"${subtotal_general:.2f}")
        # if hasattr(self, 'label_iva_der'): # IVA REMOVED
        #     self.label_iva_der.setText(f"${iva:.2f}")
        if hasattr(self, 'label_total_der_val'):
            self.label_total_der_val.setText(f"${total:.2f}")

        self.calcular_cambio()

    def actualizar_visibilidad_no_productos(self):
        if self.tabla_productos.rowCount() == 0:
            self.label_no_productos.show()
            self.tabla_productos.hide()
        else:
            self.label_no_productos.hide()
            self.tabla_productos.show()

    def crear_fila_resumen(self, layout_contenedor, etiqueta_texto, valor_inicial_texto, bold=False):
        layout_fila = QHBoxLayout()
        label_etiqueta = QLabel(etiqueta_texto)
        if bold:
            label_etiqueta.setStyleSheet("font-weight: bold;")

        label_valor = QLabel(valor_inicial_texto)
        label_valor.setAlignment(Qt.AlignmentFlag.AlignRight)
        if bold:
            label_valor.setStyleSheet("font-weight: bold; font-size: 16px;")

        layout_fila.addWidget(label_etiqueta)
        layout_fila.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout_fila.addWidget(label_valor)
        layout_contenedor.addLayout(layout_fila)
        return label_valor

    def crear_panel_derecho(self, layout_contenedor):
        widget_panel_derecho = QWidget()
        widget_panel_derecho.setObjectName("panelDerechoWidget")
        layout_panel_derecho = QVBoxLayout(widget_panel_derecho)
        layout_panel_derecho.setContentsMargins(15, 15, 15, 15)
        layout_panel_derecho.setSpacing(20)

        label_instrucciones_titulo = QLabel("Instrucciones")
        label_instrucciones_titulo.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 5px;")
        layout_panel_derecho.addWidget(label_instrucciones_titulo)

        texto_instrucciones = """
1. Escanee el código de barras o ingrese el código manualmente.
2. Ajuste las cantidades según sea necesario.
3. Haga clic en "Finalizar Venta" cuando termine.
4. Seleccione el método de pago y complete la transacción.
        """
        label_instrucciones_texto = QLabel(texto_instrucciones)
        label_instrucciones_texto.setObjectName("labelInstruccionesTexto") 
        label_instrucciones_texto.setWordWrap(True)
        layout_panel_derecho.addWidget(label_instrucciones_texto)

        linea_separadora_der = QFrame()
        linea_separadora_der.setFrameShape(QFrame.Shape.HLine)
        linea_separadora_der.setFrameShadow(QFrame.Shadow.Sunken)
        layout_panel_derecho.addWidget(linea_separadora_der)
        
        label_procesar_pago_titulo = QLabel("Procesar pago")
        label_procesar_pago_titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-top:10px; margin-bottom: 10px;")
        layout_panel_derecho.addWidget(label_procesar_pago_titulo)

        self.label_subtotal_der = self.crear_fila_resumen(layout_panel_derecho, "Subtotal:", "$0.00")
        # self.label_iva_der = self.crear_fila_resumen(layout_panel_derecho, "IVA (16%):", "$0.00") # IVA REMOVED
        self.label_total_der_val = self.crear_fila_resumen(layout_panel_derecho, "Total:", "$0.00", bold=True)

        layout_metodo_pago = QHBoxLayout()
        label_metodo_pago = QLabel("Método de pago:")
        self.combo_metodo_pago = QComboBox()
        self.combo_metodo_pago.addItems(["Efectivo", "Tarjeta de Crédito", "Tarjeta de Débito", "Transferencia"])
        layout_metodo_pago.addWidget(label_metodo_pago)
        layout_metodo_pago.addWidget(self.combo_metodo_pago)
        layout_panel_derecho.addLayout(layout_metodo_pago)

        layout_monto_recibido = QHBoxLayout()
        label_monto_recibido = QLabel("Monto recibido:")
        self.input_monto_recibido = QLineEdit()
        self.input_monto_recibido.setPlaceholderText("$0.00")
        self.input_monto_recibido.textChanged.connect(self.calcular_cambio)
        layout_monto_recibido.addWidget(label_monto_recibido)
        layout_monto_recibido.addWidget(self.input_monto_recibido)
        layout_panel_derecho.addLayout(layout_monto_recibido)

        layout_cambio = QHBoxLayout()
        label_cambio_etiqueta = QLabel("Cambio:")
        label_cambio_etiqueta.setStyleSheet("font-weight: bold;")
        self.label_cambio_valor = QLabel("$0.00")
        self.label_cambio_valor.setObjectName("labelCambioValor") 
        self.label_cambio_valor.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout_cambio.addWidget(label_cambio_etiqueta)
        layout_cambio.addSpacerItem(QSpacerItem(40,20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout_cambio.addWidget(self.label_cambio_valor)
        layout_panel_derecho.addLayout(layout_cambio)
        
        layout_panel_derecho.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout_contenedor.addWidget(widget_panel_derecho, 1)

    def calcular_cambio(self):
        try:
            total_str = self.label_total_der_val.text().replace('$', '')
            total_venta = float(total_str) if total_str else 0.0

            monto_recibido_str = self.input_monto_recibido.text().replace('$', '')
            if not monto_recibido_str: # If monto recibido is empty, show $0.00 change
                self.label_cambio_valor.setText("$0.00")
                # Reset property to ensure correct color if it was previously "Falta" or "Inválido"
                self.label_cambio_valor.setProperty("text", "$0.00") 
                self.style().unpolish(self.label_cambio_valor)
                self.style().polish(self.label_cambio_valor)
                return

            monto_recibido = float(monto_recibido_str)

            if monto_recibido >= total_venta:
                cambio = monto_recibido - total_venta
                self.label_cambio_valor.setText(f"${cambio:.2f}")
            else:
                faltante = total_venta - monto_recibido
                self.label_cambio_valor.setText(f"Falta: ${faltante:.2f}")
        except ValueError:
            self.label_cambio_valor.setText("Inválido")
        
        # Ensure dynamic stylesheet properties are reapplied for labelCambioValor
        self.label_cambio_valor.style().unpolish(self.label_cambio_valor)
        self.label_cambio_valor.style().polish(self.label_cambio_valor)

    def procesar_enter_en_busqueda_producto(self):
        """Handles Enter key press in the product search input."""
        current_text_in_line_edit = self.input_codigo_barras.text().strip()

        # If the completer's popup is visible and there's a current completion
        # (highlighted item), it means the user is likely pressing Enter to select it.
        # The QCompleter.activated signal is the most reliable way to get this exact selection.
        if self.product_completer.popup().isVisible() and self.product_completer.currentCompletion():
            # Let the QCompleter.activated signal handle this.
            # It will call self.producto_seleccionado_del_completer with the chosen string.
            # We explicitly trigger the activated signal with the current completion if needed,
            # though typically Enter on a QLineEdit with an active completer does this.
            # However, to be safe, we can try to activate it.
            # self.product_completer.activated.emit(self.product_completer.currentCompletion()) # This might be too aggressive or cause double calls.
            # For now, simply returning and relying on Qt's default behavior is safer.
            return

        # If popup is not visible or no current completion, proceed with current text.
        if not current_text_in_line_edit:
            return

        # Check if the current text (which might have been typed or pasted)
        # is a key in our current suggestions map.
        # This map should be up-to-date from the last call to update_product_completer_list
        if current_text_in_line_edit in self.product_suggestions_map:
            self.producto_seleccionado_del_completer(current_text_in_line_edit)
        else:
            # If not a direct match from the map (e.g., partial input, or map is outdated/empty),
            # fall back to the general search logic. This handles cases where the user types
            # a code/name and hits Enter without interacting with the completer popup.
            self.buscar_y_agregar_producto_click()

    def setup_product_completer(self):
        """Sets up QCompleter for product search input."""
        self.product_completer_model = QStringListModel()
        self.product_completer = QCompleter(self.product_completer_model, self)
        self.product_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.product_completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.input_codigo_barras.setCompleter(self.product_completer)
        self.input_codigo_barras.textChanged.connect(self.update_product_completer_list)
        self.product_completer.activated.connect(self.producto_seleccionado_del_completer) # When an item is selected

    def update_product_completer_list(self, text):
        """Updates the completer list based on input text."""
        
        # If the current text in the QLineEdit is already a full suggestion string
        # that exists as a key in our map, it means the completer might have just
        # set this text (e.g., user clicked an item, or tabbed).
        # We should not re-query or clear the map in this specific case,
        # as the map is still valid for the prefix that generated these suggestions.
        if text in self.product_suggestions_map and self.product_completer_model.stringList().count(text) > 0:
            # If the completer popup is not visible but should be (e.g. user backspaced then retyped to a full suggestion)
            if self.product_completer_model.rowCount() > 0 and not self.product_completer.popup().isVisible() and self.input_codigo_barras.hasFocus():
                 self.product_completer.complete()
            return 

        # User is typing a new prefix, or the text is not a full suggestion from the current map.
        if len(text) < 1: # Start searching after 1 character
            self.product_completer_model.setStringList([])
            self.product_suggestions_map = {} # Clear map for short/empty prefix
            return
        
        # Fetch new suggestions based on the current prefix 'text'
        products_db = db_manager.get_product_by_code_or_name(text)
        
        suggestions = []
        # Build a fresh map for this specific prefix 'text'.
        # This ensures that product_suggestions_map is always in sync with what is being displayed.
        current_prefix_map = {} 
        for prod in products_db:
            suggestion_str = f"""{prod['nombre_producto']} ({prod['codigo_barras']}) - ${prod['precio_venta']:.2f}"""
            suggestions.append(suggestion_str)
            current_prefix_map[suggestion_str] = prod 
        
        self.product_completer_model.setStringList(suggestions)
        # Atomically update the main map with the suggestions for the current prefix 'text'.
        self.product_suggestions_map = current_prefix_map 

        # Show popup if there are suggestions and the input has focus.
        # This is important if the user types quickly or if the list updates.
        if suggestions and self.input_codigo_barras.hasFocus():
            self.product_completer.complete()
        elif not suggestions:
             self.product_completer.popup().hide()


    def producto_seleccionado_del_completer(self, selected_suggestion_str):
        """Handles product selection from completer (called by QCompleter.activated)."""
        if selected_suggestion_str in self.product_suggestions_map:
            product_data = self.product_suggestions_map[selected_suggestion_str]
            # Add product to table with quantity 1
            self.agregar_fila_producto(
                id_producto=product_data['id_producto'], 
                nombre=product_data['nombre_producto'], 
                cantidad=1, 
                precio=product_data['precio_venta']
            )
            self.input_codigo_barras.clear() # Clear input after adding
            self.input_codigo_barras.setFocus()
        else: # Fallback if somehow the selected string is not in our map
            self.show_styled_message_box("Error", "Producto seleccionado no encontrado en la lista de sugerencias.", QMessageBox.Icon.Warning)

    def buscar_y_agregar_producto_click(self):
        """Handles adding product via button click, typically after manual code entry or if completer not used."""
        term = self.input_codigo_barras.text().strip()
        if not term:
            self.show_styled_message_box("Entrada Vacía", "Ingrese un código o nombre de producto.", QMessageBox.Icon.Warning)
            return

        products_db = db_manager.get_product_by_code_or_name(term)

        if not products_db:
            self.show_styled_message_box("No Encontrado", f"No se encontró producto con: {term}", QMessageBox.Icon.Information)
            return
        
        if len(products_db) == 1:
            # If exact match or single result, add it directly
            prod = products_db[0]
            self.agregar_fila_producto(prod['id_producto'], prod['nombre_producto'], 1, prod['precio_venta'])
            self.input_codigo_barras.clear()
        else:
            # If multiple matches, user should ideally pick from completer.
            # For now, we can inform them or pick the first one as an example.
            # Or, better, rely on the completer's activated signal for selection.
            self.show_styled_message_box("Múltiples Coincidencias", 
                                  "Se encontraron varios productos. Por favor, seleccione uno de la lista desplegable.",
                                  QMessageBox.Icon.Information)
            # Optionally, populate completer if not already done by textChanged
            self.update_product_completer_list(term) 

    def finalizar_venta(self):
        if self.tabla_productos.rowCount() == 0:
            self.show_styled_message_box("Venta Vacía", "No hay productos en la venta para finalizar.", QMessageBox.Icon.Warning)
            return

        if not self.id_usuario_cajero:
            self.show_styled_message_box("Error de Usuario", "No se ha identificado al cajero. No se puede registrar la venta.", QMessageBox.Icon.Critical)
            return

        total_venta_str = self.label_total_izq.text().replace('$', '')
        try:
            total_venta = float(total_venta_str)
        except ValueError:
            self.show_styled_message_box("Error de Cálculo", "No se pudo determinar el total de la venta.", QMessageBox.Icon.Critical)
            return

        metodo_pago = self.combo_metodo_pago.currentText()
        # Consider validating monto_recibido and cambio here if strict checks are needed before saving

        detalles_venta_list = []
        for fila in range(self.tabla_productos.rowCount()):
            try:
                id_item = self.tabla_productos.item(fila, 0) # Hidden ID column
                if not id_item:
                    self.show_styled_message_box("Error en Datos de Tabla", f"Falta ID de producto en fila {fila+1}.", QMessageBox.Icon.Critical)
                    return
                id_producto = int(id_item.text())
                
                cantidad_widget = self.tabla_productos.cellWidget(fila, 2) # Cantidad QLineEdit
                if not isinstance(cantidad_widget, QLineEdit):
                    self.show_styled_message_box("Error en Datos de Tabla", f"Widget de cantidad no es QLineEdit en fila {fila+1}.", QMessageBox.Icon.Critical)
                    return
                cantidad = int(cantidad_widget.text())
                
                precio_item = self.tabla_productos.item(fila, 4) # Precio column
                if not precio_item:
                    self.show_styled_message_box("Error en Datos de Tabla", f"Falta precio de producto en fila {fila+1}.", QMessageBox.Icon.Critical)
                    return
                precio_str = precio_item.text().replace('$', '')
                precio_unitario = float(precio_str)
                
                subtotal_item = self.tabla_productos.item(fila, 5) # Subtotal column
                if not subtotal_item:
                    self.show_styled_message_box("Error en Datos de Tabla", f"Falta subtotal de producto en fila {fila+1}.", QMessageBox.Icon.Critical)
                    return
                subtotal_str = subtotal_item.text().replace('$', '')
                subtotal_linea = float(subtotal_str)

                if cantidad <= 0:
                    self.show_styled_message_box("Cantidad Inválida", f"El producto en la fila {fila+1} tiene cantidad cero o negativa.", QMessageBox.Icon.Warning)
                    return

                detalles_venta_list.append({
                    'id_producto': id_producto,
                    'cantidad': cantidad,
                    'precio_unitario_venta': precio_unitario,
                    'subtotal_linea': subtotal_linea
                })
            except Exception as e:
                self.show_styled_message_box("Error en Datos de Tabla", f"Error procesando producto en fila {fila+1}: {e}", QMessageBox.Icon.Critical)
                return

        success, message = db_manager.record_sale(self.id_usuario_cajero, total_venta, metodo_pago, detalles_venta_list)

        if success:
            # Original success message from db_manager
            db_message = message 

            # Get change text
            cambio_str = self.label_cambio_valor.text()
            
            # Prepare the main part of the message using HTML
            final_message_html = f"{db_message}<br>"

            # Add bolded change information if applicable
            if cambio_str.startswith("$") and cambio_str != "$0.00": # Only if actual change > 0
                final_message_html += f"<b>Favor de regresar {cambio_str}</b><br>"
            
            final_message_html += "El módulo de venta se ha reiniciado y está listo para una nueva transacción."
            
            self.show_styled_message_box("Venta Finalizada", 
                                         final_message_html, 
                                         QMessageBox.Icon.Information,
                                         rich_text=True) # Pass rich_text=True
            self.limpiar_interfaz_venta()
        else:
            self.show_styled_message_box("Error al Guardar Venta", message, QMessageBox.Icon.Critical)

    def limpiar_interfaz_venta(self):
        """Limpia la tabla de productos y los totales para una nueva venta."""
        self.tabla_productos.setRowCount(0)
        self.productos_en_tabla.clear()
        self.actualizar_totales_venta() # This will reset labels like total, subtotal
        self.input_codigo_barras.clear()
        self.input_monto_recibido.clear()
        # self.label_cambio_valor.setText("$0.00") # calcular_cambio should handle this if monto_recibido is cleared
        self.actualizar_visibilidad_no_productos()
        self.input_codigo_barras.setFocus()

    def eliminar_producto_de_venta(self, fila, id_producto):
        """Removes a product from the sales table."""
        if id_producto in self.productos_en_tabla:
            del self.productos_en_tabla[id_producto]
        
        self.tabla_productos.removeRow(fila)
        # After removing a row, row indices of subsequent items change.
        # We need to update self.productos_en_tabla to reflect new row indices.
        # This is a bit complex if rows are deleted from the middle.
        # A simpler way for now is to rebuild it, or be careful if deleting often mid-list or this simple update is okay.
        # For now, let's assume deletion isn't super frequent mid-list or this simple update is okay.
        # Rebuild self.productos_en_tabla to ensure correct row indices
        temp_productos_en_tabla = {}
        for r in range(self.tabla_productos.rowCount()):
            id_item_widget = self.tabla_productos.item(r, 0)
            if id_item_widget:
                prod_id_in_row = int(id_item_widget.text())
                temp_productos_en_tabla[prod_id_in_row] = r
        self.productos_en_tabla = temp_productos_en_tabla

        self.actualizar_totales_venta()
        self.actualizar_visibilidad_no_productos()
        self.input_codigo_barras.setFocus()

    def show_styled_message_box(self, title, text, icon=QMessageBox.Icon.Information, rich_text=False):
        """Displays a QMessageBox with a white background and black text."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        
        if rich_text:
            msg_box.setTextFormat(Qt.TextFormat.RichText)
        else:
            msg_box.setTextFormat(Qt.TextFormat.PlainText) # Default or explicit plain

        msg_box.setText(text)
        msg_box.setIcon(icon)
        # Apply standard styling
        # Stylesheet might be more extensive based on previous versions
        msg_box.setStyleSheet("""
            QMessageBox { 
                background-color: white; 
                color: black; 
                min-width: 320px;
                font-size: 14px;
            }
            QLabel#qt_msgbox_label { /* Target the text label for text() */
                font-size: 14px;
            }
            QLabel#qt_msgbox_informativelabel { /* Target for informativeText() if used */
                font-size: 13px;
            }
            QPushButton { 
                background-color: #007bff; 
                color: white; 
                padding: 8px 18px;
                min-width: 90px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        
        # Ensure an OK button if no standard buttons are added by default based on icon
        if not msg_box.buttons():
            msg_box.addButton(QMessageBox.StandardButton.Ok)
            
        msg_box.exec()

