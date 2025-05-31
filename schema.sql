-- Esquema de Base de Datos para EasyPoint - SQLite3

-- Tabla de Usuarios
CREATE TABLE IF NOT EXISTS Usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario TEXT UNIQUE NOT NULL,
    pin TEXT NOT NULL, -- En una aplicación real, el PIN debería estar hasheado
    tipo_usuario TEXT NOT NULL CHECK(tipo_usuario IN ('Cajero', 'Administrador'))
);

-- Tabla de Productos
CREATE TABLE IF NOT EXISTS Productos (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_barras TEXT UNIQUE,
    nombre_producto TEXT NOT NULL,
    descripcion TEXT,
    precio_compra REAL, -- Opcional, para calcular ganancias
    precio_venta REAL NOT NULL,
    stock_actual INTEGER DEFAULT 0,
    id_proveedor INTEGER, -- Opcional, si se quiere manejar proveedores
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor) -- Si se añade tabla Proveedores
);

-- Tabla de Ventas
CREATE TABLE IF NOT EXISTS Ventas (
    id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario_cajero INTEGER NOT NULL,
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_venta REAL NOT NULL,
    metodo_pago TEXT, -- Ej: 'Efectivo', 'Tarjeta de Crédito', 'Tarjeta de Débito'
    FOREIGN KEY (id_usuario_cajero) REFERENCES Usuarios(id_usuario)
);

-- Tabla de Detalles de Venta (productos vendidos en cada venta)
CREATE TABLE IF NOT EXISTS DetallesVenta (
    id_detalle_venta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_venta INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario_venta REAL NOT NULL, -- Precio del producto al momento de la venta
    subtotal_linea REAL NOT NULL, -- cantidad * precio_unitario_venta
    FOREIGN KEY (id_venta) REFERENCES Ventas(id_venta),
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto)
);

-- Tabla de Historial de Stock (Opcional, para auditoría de inventario)
-- CREATE TABLE IF NOT EXISTS HistorialStock (
--     id_historial_stock INTEGER PRIMARY KEY AUTOINCREMENT,
--     id_producto INTEGER NOT NULL,
--     fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     tipo_movimiento TEXT NOT NULL CHECK(tipo_movimiento IN ('Entrada', 'Salida por Venta', 'Ajuste')),
--     cantidad_movida INTEGER NOT NULL,
--     stock_anterior INTEGER,
--     stock_nuevo INTEGER,
--     id_venta_asociada INTEGER, -- Para 'Salida por Venta'
--     notas TEXT,
--     FOREIGN KEY (id_producto) REFERENCES Productos(id_producto),
--     FOREIGN KEY (id_venta_asociada) REFERENCES Ventas(id_venta)
-- );

-- Tabla de Proveedores (Opcional)
-- CREATE TABLE IF NOT EXISTS Proveedores (
--     id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
--     nombre_proveedor TEXT NOT NULL,
--     contacto_nombre TEXT,
--     contacto_telefono TEXT,
--     contacto_email TEXT,
--     direccion TEXT
-- );


-- Inserciones de datos iniciales

-- Usuario Administrador por defecto
INSERT INTO Usuarios (nombre_usuario, pin, tipo_usuario) VALUES ('admin', '1234', 'Administrador');
-- Usuario Cajero por defecto
INSERT INTO Usuarios (nombre_usuario, pin, tipo_usuario) VALUES ('cajero1', '0000', 'Cajero');

-- Productos de ejemplo
INSERT INTO Productos (codigo_barras, nombre_producto, descripcion, precio_venta, stock_actual) VALUES
('750100000001', 'Refresco Cola 600ml', 'Bebida carbonatada sabor cola', 15.00, 100),
('750100000002', 'Papas Fritas Saladas 45g', 'Botana de papa con sal', 12.50, 150),
('750100000003', 'Galletas de Chocolate 60g', 'Galletas con chispas de chocolate', 10.00, 80),
('750100000004', 'Agua Embotellada 1L', 'Agua purificada sin gas', 10.00, 200),
('750100000005', 'Jabón de Tocador Neutro', 'Jabón para manos y cuerpo', 20.00, 50);

-- Ejemplo de una venta (para pruebas, si es necesario)
-- Supongamos que el usuario 'cajero1' (id_usuario=2) realiza una venta
-- INSERT INTO Ventas (id_usuario_cajero, total_venta, metodo_pago) VALUES (2, 37.50, 'Efectivo');
-- -- Obtener el id_venta de la venta recién insertada (SQLite specific)
-- -- SELECT last_insert_rowid(); -- Supongamos que devuelve 1
-- INSERT INTO DetallesVenta (id_venta, id_producto, cantidad, precio_unitario_venta, subtotal_linea) VALUES
-- (1, 1, 1, 15.00, 15.00), -- 1 Refresco Cola
-- (1, 2, 1, 12.50, 12.50); -- 1 Papas Fritas

PRAGMA foreign_keys = ON; -- Asegurar que las llaves foráneas estén activadas
