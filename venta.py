import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QSpacerItem, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QIntValidator

class VentanaPuntoDeVenta(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Punto de Venta")
        self.setGeometry(100, 100, 1200, 700)

        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout(widget_central)

        self.crear_barra_superior(layout_principal)

        layout_contenido = QHBoxLayout()
        layout_principal.addLayout(layout_contenido)

        # Cambiar el orden: primero panel derecho, luego izquierdo
        self.crear_panel_derecho(layout_contenido)
        self.crear_panel_izquierdo(layout_contenido)

        # Modificación clave: Estilos CSS más específicos para visibilidad
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0; /* Fondo gris claro para la ventana principal */
            }
            /* Estilos generales para todos los QLabel */
            QLabel {
                font-size: 14px;
                color: #333333; /* Color de texto oscuro para QLabel por defecto */
            }
            /* Estilos generales para todos los QPushButton */
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
            /* Estilos generales para todos los QLineEdit */
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                background-color: white; /* Asegura que el QLineEdit tenga fondo blanco */
                color: #333333; /* Color de texto oscuro para QLineEdit */
            }
            /* Estilos generales para QTableWidget */
            QTableWidget {
                font-size: 13px;
                border: 1px solid #ccc;
                background-color: white; /* Asegura que la tabla tenga fondo blanco */
                color: #333333; /* Color de texto oscuro para las celdas de la tabla */
            }
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 5px;
                border: 1px solid #ccc;
                font-size: 14px;
                font-weight: bold;
                color: #333333; /* Color de texto oscuro para la cabecera de la tabla */
            }
            /* Estilos generales para QComboBox */
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
                background-color: white; /* Asegura que el QComboBox tenga fondo blanco */
                color: #333333; /* Color de texto oscuro para QComboBox */
            }
            /* Estilo para los QFrame usados como separadores */
            QFrame[frameShape="4"], /* QFrame.HLine */
            QFrame[frameShape="5"]  /* QFrame.VLine */
            {
                border: none;
                background-color: #cccccc; /* Color del separador */
            }
            QFrame[frameShape="4"] { /* HLine */
                max-height: 1px;
                min-height: 1px;
            }
            QFrame[frameShape="5"] { /* VLine */
                max-width: 1px;
                min-width: 1px;
            }

            /* Estilos específicos para la barra superior */
            #barraSuperiorWidget { /* Usamos un objectName para mayor especificidad */
                background-color: #343a40;
                color: white; /* Asegura que el color de texto por defecto en este widget sea blanco */
                padding: 10px;
            }
            #barraSuperiorWidget QLabel { /* Estilo para los QLabel dentro de la barra superior */
                color: white;
            }
            #barraSuperiorWidget QPushButton {
                background-color: #6c757d;
                border-color: #6c757d;
                color: white; /* Asegura que el texto del botón sea blanco */
            }
            #barraSuperiorWidget QPushButton:hover {
                background-color: #5a6268;
            }
            #botonSalir { /* Estilo específico para el botón Salir */
                background-color: #dc3545;
                border-color: #dc3545;
            }
            #botonSalir:hover {
                background-color: #c82333;
            }

            /* Estilos para los paneles izquierdo y derecho */
            #panelIzquierdoWidget, #panelDerechoWidget { /* Usamos objectName */
                background-color: white;
                border-radius: 5px;
            }

            /* Estilo para el QLabel de "No hay productos" */
            #labelNoProductos {
                font-style: italic;
                color: #6c757d;
                margin-top: 20px;
                margin-bottom: 20px;
            }

            /* Estilo para el QLabel de instrucciones */
            #labelInstruccionesTexto {
                background-color: #e9ecef;
                padding: 10px;
                border-radius: 4px;
                margin-bottom: 10px;
                color: #333333; /* Color de texto oscuro para las instrucciones */
            }

            /* Estilo para el valor del cambio */
            #labelCambioValor {
                font-weight: bold;
                font-size: 16px;
                color: #28a745; /* Verde por defecto */
            }
            /* Estilo para el valor de cambio cuando hay faltante */
            #labelCambioValor[text^="Falta"] { /* Selecciona cuando el texto empieza con "Falta" */
                color: #dc3545; /* Rojo para faltante */
            }
            /* Estilo para el valor de cambio cuando es inválido */
            #labelCambioValor[text="Inválido"] {
                color: #ffc107; /* Naranja para inválido */
            }

            /* Estilos específicos para los botones de cantidad en la tabla */
            QTableWidget QPushButton {
                font-size: 16px; /* Aumenta el tamaño de la fuente */
                padding: 0px; /* Reduce el padding para que se ajusten mejor */
                background-color: #007bff; /* Color de fondo por defecto */
                color: white; /* Color de texto */
                border-radius: 3px; /* Bordes ligeramente redondeados */
                min-width: 25px; /* Asegura un ancho mínimo */
                max-width: 25px; /* Limita el ancho */
                min-height: 25px; /* Asegura una altura mínima */
                max-height: 25px; /* Limita la altura */
            }
            QTableWidget QPushButton:hover {
                background-color: #0056b3;
            }

        """)

    def crear_barra_superior(self, layout_principal):
        widget_barra_superior = QWidget()
        widget_barra_superior.setObjectName("barraSuperiorWidget") # Agregado objectName
        layout_barra_superior = QHBoxLayout(widget_barra_superior)
        layout_barra_superior.setContentsMargins(10, 0, 10, 0)

        titulo_app = QLabel("PuntoLite")
        titulo_app.setStyleSheet("font-size: 20px; font-weight: bold;") # El color blanco se hereda de #barraSuperiorWidget



        boton_salir = QPushButton("Salir")
        boton_salir.setFixedWidth(80)
        boton_salir.setObjectName("botonSalir") # Agregado objectName
        boton_salir.clicked.connect(self.close)

        layout_barra_superior.addWidget(titulo_app)
        layout_barra_superior.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        layout_barra_superior.addWidget(boton_salir)

        layout_principal.addWidget(widget_barra_superior)

    def crear_panel_izquierdo(self, layout_contenedor):
        widget_panel_izquierdo = QWidget()
        widget_panel_izquierdo.setObjectName("panelIzquierdoWidget") # Agregado objectName
        layout_panel_izquierdo = QVBoxLayout(widget_panel_izquierdo)
        layout_panel_izquierdo.setContentsMargins(15, 15, 15, 15)
        layout_panel_izquierdo.setSpacing(15)

        label_productos_venta = QLabel("Productos en Venta")
        label_productos_venta.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout_panel_izquierdo.addWidget(label_productos_venta)

        layout_busqueda = QHBoxLayout()
        self.input_codigo_barras = QLineEdit()
        self.input_codigo_barras.setPlaceholderText("Escanee código de barras o ingrese el código manualmente...")
        layout_busqueda.addWidget(self.input_codigo_barras, 4)

        self.boton_agregar_producto = QPushButton("Agregar")
        self.boton_agregar_producto.setFixedWidth(120)
        layout_busqueda.addWidget(self.boton_agregar_producto, 1)
        layout_panel_izquierdo.addLayout(layout_busqueda)

        self.tabla_productos = QTableWidget()
        self.tabla_productos.setColumnCount(5)
        self.tabla_productos.setHorizontalHeaderLabels(["Nombre", "Cantidad", "", "Precio", "Subtotal"])
        self.tabla_productos.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.tabla_productos.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.tabla_productos.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.tabla_productos.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)
        self.tabla_productos.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Interactive)
        self.tabla_productos.setColumnWidth(1, 80)
        self.tabla_productos.setColumnWidth(2, 70)
        self.tabla_productos.setColumnWidth(3, 100)
        self.tabla_productos.setColumnWidth(4, 100)
        self.tabla_productos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout_panel_izquierdo.addWidget(self.tabla_productos)

        self.label_no_productos = QLabel("No hay productos en la venta actual.")
        self.label_no_productos.setObjectName("labelNoProductos") # Agregado objectName
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
        self.label_iva_izq = self.crear_fila_resumen(layout_resumen_venta_1, "IVA (16%):", "$0.00")
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
        layout_botones_accion_1.addWidget(boton_finalizar_venta_1)
        layout_panel_izquierdo.addLayout(layout_botones_accion_1)

        layout_contenedor.addWidget(widget_panel_izquierdo, 2)
        self.actualizar_visibilidad_no_productos()


    def agregar_fila_producto(self, nombre, cantidad, precio):
        rowCount = self.tabla_productos.rowCount()
        self.tabla_productos.insertRow(rowCount)

        self.tabla_productos.setItem(rowCount, 0, QTableWidgetItem(nombre))

        input_cantidad_item_solo = QLineEdit(str(cantidad))
        input_cantidad_item_solo.setValidator(QIntValidator(1, 999))
        input_cantidad_item_solo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        input_cantidad_item_solo.textChanged.connect(lambda text, r=rowCount: self.actualizar_subtotal_fila(r))
        self.tabla_productos.setCellWidget(rowCount, 1, input_cantidad_item_solo)

        widget_botones_cant = QWidget()
        layout_botones_cant = QHBoxLayout(widget_botones_cant)
        layout_botones_cant.setContentsMargins(0,0,0,0)
        layout_botones_cant.setSpacing(2)
        boton_menos_sep = QPushButton("-")
        boton_menos_sep.setFixedSize(QSize(25,25)) # Mantener el tamaño fijo pero los estilos CSS mejoran el aspecto
        boton_menos_sep.clicked.connect(lambda _, r=rowCount: self.modificar_cantidad(r, -1))
        boton_mas_sep = QPushButton("+")
        boton_mas_sep.setFixedSize(QSize(25,25)) # Mantener el tamaño fijo
        boton_mas_sep.clicked.connect(lambda _, r=rowCount: self.modificar_cantidad(r, 1))
        layout_botones_cant.addWidget(boton_menos_sep)
        layout_botones_cant.addWidget(boton_mas_sep)
        layout_botones_cant.addStretch()
        self.tabla_productos.setCellWidget(rowCount, 2, widget_botones_cant)

        self.tabla_productos.setItem(rowCount, 3, QTableWidgetItem(f"${precio:.2f}"))
        subtotal = cantidad * precio
        self.tabla_productos.setItem(rowCount, 4, QTableWidgetItem(f"${subtotal:.2f}"))

        for col in [0, 3, 4]:
            item = self.tabla_productos.item(rowCount, col)
            if item:
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.actualizar_totales_venta()
        self.actualizar_visibilidad_no_productos()

    def modificar_cantidad(self, fila, delta):
        input_cantidad_widget = self.tabla_productos.cellWidget(fila, 1)
        if isinstance(input_cantidad_widget, QLineEdit):
            try:
                cantidad_actual = int(input_cantidad_widget.text())
                nueva_cantidad = max(1, cantidad_actual + delta)
                input_cantidad_widget.setText(str(nueva_cantidad))
            except ValueError:
                input_cantidad_widget.setText("1")

    def actualizar_subtotal_fila(self, fila):
        input_cantidad_widget = self.tabla_productos.cellWidget(fila, 1)
        item_precio = self.tabla_productos.item(fila, 3)

        if isinstance(input_cantidad_widget, QLineEdit) and item_precio:
            try:
                cantidad = int(input_cantidad_widget.text())
                precio_str = item_precio.text().replace('$', '')
                precio = float(precio_str)
                subtotal = cantidad * precio
                self.tabla_productos.setItem(fila, 4, QTableWidgetItem(f"${subtotal:.2f}"))
                item_subtotal = self.tabla_productos.item(fila,4)
                if item_subtotal:
                    item_subtotal.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            except ValueError:
                self.tabla_productos.setItem(fila, 4, QTableWidgetItem("$0.00"))
        self.actualizar_totales_venta()

    def actualizar_totales_venta(self):
        subtotal_general = 0.0
        for fila in range(self.tabla_productos.rowCount()):
            item_subtotal_fila = self.tabla_productos.item(fila, 4)
            if item_subtotal_fila:
                try:
                    subtotal_general += float(item_subtotal_fila.text().replace('$', ''))
                except ValueError:
                    pass

        iva = subtotal_general * 0.16
        total = subtotal_general + iva

        if hasattr(self, 'label_subtotal_izq'):
            self.label_subtotal_izq.setText(f"${subtotal_general:.2f}")
        if hasattr(self, 'label_iva_izq'):
            self.label_iva_izq.setText(f"${iva:.2f}")
        if hasattr(self, 'label_total_izq'):
            self.label_total_izq.setText(f"${total:.2f}")

        if hasattr(self, 'label_subtotal_der'):
            self.label_subtotal_der.setText(f"${subtotal_general:.2f}")
        if hasattr(self, 'label_iva_der'):
            self.label_iva_der.setText(f"${iva:.2f}")
        if hasattr(self, 'label_total_der_val'):
            self.label_total_der_val.setText(f"${total:.2f}")

        self.calcular_cambio() # Llama a calcular_cambio para que el cambio se actualice si el total cambia

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
        widget_panel_derecho.setObjectName("panelDerechoWidget") # Agregado objectName
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
        label_instrucciones_texto.setObjectName("labelInstruccionesTexto") # Agregado objectName
        label_instrucciones_texto.setWordWrap(True)
        layout_panel_derecho.addWidget(label_instrucciones_texto)

        linea_separadora_der = QFrame()
        linea_separadora_der.setFrameShape(QFrame.Shape.HLine)
        linea_separadora_der.setFrameShadow(QFrame.Shadow.Sunken)
        layout_panel_derecho.addWidget(linea_separadora_der)

        label_procesar_pago_titulo = QLabel("Procesar pago")
        label_procesar_pago_titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-top:10px; margin-bottom: 10px;")
        layout_panel_derecho.addWidget(label_procesar_pago_titulo)

        # Inicializar los valores a $0.00
        self.label_subtotal_der = self.crear_fila_resumen(layout_panel_derecho, "Subtotal:", "$0.00")
        self.label_iva_der = self.crear_fila_resumen(layout_panel_derecho, "IVA (16%):", "$0.00")
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
        self.label_cambio_valor.setObjectName("labelCambioValor") # Agregado objectName
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
            if not monto_recibido_str:
                self.label_cambio_valor.setText("$0.00")
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

