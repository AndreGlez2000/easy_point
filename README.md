# 📊 EasyPoint - Sistema de Punto de Venta

**EasyPoint** es un sistema completo de punto de venta (POS) desarrollado en Python con interfaz gráfica moderna usando PySide6. Diseñado para pequeños y medianos comercios que necesitan una solución eficiente, intuitiva y confiable para gestionar sus ventas e inventario.

## 🎯 Características Principales

- ✅ **Interfaz Gráfica Moderna**: Diseño intuitivo y fácil de usar
- ✅ **Sistema de Usuarios**: Manejo de cajeros y administradores
- ✅ **Gestión de Ventas**: Proceso completo de ventas con múltiples métodos de pago
- ✅ **Historial Detallado**: Consulta y análisis de ventas realizadas
- ✅ **Gestión de Inventario**: Control de productos y stock
- ✅ **Base de Datos SQLite**: Sistema de almacenamiento robusto y confiable
- ✅ **Autocompletado Inteligente**: Búsqueda rápida de productos
- ✅ **Reportes de Ventas**: Filtrado por fecha, cajero y otros criterios

---

## 🔧 Requisitos del Sistema

### Requisitos Mínimos
- **Sistema Operativo**: Windows 7/8/10/11, macOS 10.12+, o Linux Ubuntu 16.04+
- **Python**: Versión 3.7 o superior
- **RAM**: Mínimo 2 GB
- **Espacio en Disco**: 100 MB libres
- **Resolución de Pantalla**: 1024x768 (Recomendado: 1366x768 o superior)

### Dependencias de Software
- Python 3.7+
- PySide6 6.5.0+
- SQLite3 (incluido con Python)

---

## 📦 Instalación

### Paso 1: Verificar Python
Primero, verifica que tienes Python instalado:

```bash
python --version
```

Si no tienes Python, descárgalo desde [python.org](https://www.python.org/downloads/)

### Paso 2: Descargar EasyPoint
Clona o descarga el repositorio:

```bash
git clone [URL_DEL_REPOSITORIO]
cd easy_point
```

### Paso 3: Crear Entorno Virtual (Recomendado)
```bash
python -m venv venv
```

### Paso 4: Activar Entorno Virtual
**Windows:**
```bash
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Paso 5: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 6: Ejecutar la Aplicación
```bash
python run_app.py
```

---

## 🚀 Manual de Usuario

### Inicio de la Aplicación

1. **Ejecutar EasyPoint**
   ```bash
   python run_app.py
   ```

2. **Pantalla de Inicio**
   - La aplicación iniciará mostrando el menú principal
   - Desde aquí puedes acceder a las diferentes funcionalidades

### 👥 Sistema de Usuarios

EasyPoint maneja dos tipos de usuarios:

#### 🔐 Usuarios Predeterminados

| Usuario | PIN | Tipo | Acceso |
|---------|-----|------|--------|
| admin | 1234 | Administrador | Historial de ventas, gestión completa |
| cajero1 | 0000 | Cajero | Módulo de ventas |
| cajero2 | 1111 | Cajero | Módulo de ventas |
| cajero3 | 2222 | Cajero | Módulo de ventas |

#### Tipos de Usuario

**🛡️ Administrador:**
- Acceso completo al sistema
- Visualización del historial de ventas
- Gestión de usuarios
- Reportes y análisis
- Configuración del sistema

**👤 Cajero:**
- Acceso al módulo de ventas
- Procesamiento de transacciones
- Consulta de productos
- Generación de tickets de venta

### 💰 Módulo de Ventas

#### Acceso al Módulo
1. Inicia sesión como cajero o selecciona "Venta" desde el menú principal
2. Aparecerá la interfaz principal de ventas

#### Interfaz de Ventas

**Panel Izquierdo - Lista de Productos:**
- 📋 **Tabla de productos**: Muestra productos agregados a la venta
- 🏷️ **Columnas**: Producto, Cantidad, Precio Unitario, Subtotal, Acciones
- ➕ **Botones de cantidad**: Incrementar/decrementar cantidades
- 🗑️ **Eliminar productos**: Botón para quitar productos de la venta

**Panel Derecho - Información y Control:**
- 🔍 **Búsqueda de productos**: Campo con autocompletado inteligente
- 💵 **Resumen de venta**: Subtotal, impuestos, total
- 💳 **Método de pago**: Efectivo, tarjeta de crédito, tarjeta de débito
- 💰 **Cálculo de cambio**: Automático al ingresar efectivo recibido
- ✅ **Finalizar venta**: Procesar la transacción

#### Proceso de Venta Paso a Paso

1. **Buscar Producto**
   - Escribe el nombre o código de barras en el campo de búsqueda
   - Selecciona el producto del autocompletado
   - Presiona Enter o clic en "Agregar"

2. **Gestionar Cantidades**
   - Usa los botones + y - para ajustar cantidades
   - Las cantidades se actualizan automáticamente
   - El stock se verifica en tiempo real

3. **Seleccionar Método de Pago**
   - Elige entre: Efectivo, Tarjeta de Crédito, Tarjeta de Débito
   - Para efectivo: ingresa la cantidad recibida
   - El sistema calcula automáticamente el cambio

4. **Finalizar Venta**
   - Verifica el total y productos
   - Clic en "Finalizar Venta"
   - El sistema registra la transacción y actualiza el inventario

#### Funcionalidades Avanzadas

**🔍 Autocompletado Inteligente:**
- Búsqueda por nombre parcial del producto
- Búsqueda por código de barras
- Sugerencias en tiempo real

**📊 Cálculos Automáticos:**
- Subtotales por línea
- Total general de la venta
- Cálculo de cambio para efectivo
- Validación de stock disponible

**⚠️ Validaciones:**
- Verificación de stock suficiente
- Validación de cantidades positivas
- Control de productos duplicados
- Verificación de métodos de pago

### 📋 Módulo de Historial de Ventas (Solo Administradores)

#### Acceso al Historial
1. Inicia sesión como administrador
2. El sistema te dirigirá automáticamente al historial de ventas

#### Interfaz del Historial

**🎛️ Barra Lateral de Navegación:**
- 📊 Dashboard
- 📦 Inventario
- 📈 Historial de Ventas (actual)
- 📊 Análisis de Ventas
- 💾 Copias de Seguridad
- ⚙️ Configuración

**🔍 Filtros y Búsqueda:**
- **Búsqueda por texto**: Buscar por ID de venta o nombre de cajero
- **Filtro de fecha**: Seleccionar fecha específica para consultar
- **Ordenamiento**: Más recientes primero / Más antiguos primero

**📊 Tabla de Ventas:**
| Columna | Descripción |
|---------|-------------|
| ID Venta | Identificador único (formato V0001, V0002, etc.) |
| Fecha | Fecha y hora de la transacción |
| Cajero | Usuario que procesó la venta |
| Productos | Cantidad de productos vendidos |
| Total | Monto total de la venta |
| Acciones | Botón "Ver Detalles" |

#### Funcionalidades del Historial

**🔍 Filtrado Avanzado:**
- Búsqueda en tiempo real mientras escribes
- Filtrado por fecha específica
- Ordenamiento ascendente/descendente por fecha

**📋 Detalles de Venta:**
- Clic en "Ver Detalles" para abrir ventana emergente
- Muestra productos individuales de la transacción
- Información detallada: cantidad, precio unitario, subtotal, código de barras

**📊 Información Mostrada:**
- Historial completo de todas las transacciones
- Identificación del cajero responsable
- Fecha y hora exacta de cada venta
- Desglose completo de productos vendidos

### 🏪 Productos Disponibles (Catálogo Inicial)

| Código de Barras | Producto | Precio | Stock Inicial |
|------------------|----------|--------|---------------|
| 750100000001 | Refresco Cola 600ml | $15.00 | 100 unidades |
| 750100000002 | Papas Fritas Saladas 45g | $12.50 | 150 unidades |
| 750100000003 | Galletas de Chocolate 60g | $10.00 | 80 unidades |
| 750100000004 | Agua Embotellada 1L | $10.00 | 200 unidades |
| 750100000005 | Jabón de Tocador Neutro | $20.00 | 50 unidades |

---

## 🗃️ Estructura de la Base de Datos

### Tablas Principales

**👥 Usuarios**
- Gestión de cajeros y administradores
- Autenticación por PIN
- Control de permisos por tipo de usuario

**📦 Productos**
- Catálogo completo de productos
- Códigos de barras únicos
- Control de precios y stock
- Historial de actualizaciones

**💰 Ventas**
- Registro de todas las transacciones
- Vinculación con usuario cajero
- Métodos de pago
- Timestamp de cada venta

**📋 Detalles de Venta**
- Productos específicos de cada venta
- Cantidades y precios al momento de venta
- Subtotales por línea
- Trazabilidad completa

---

## 🔧 Configuración Avanzada

### Personalización de la Interfaz
La aplicación usa estilos CSS para Qt, permitiendo personalización de:
- Colores de la interfaz
- Fuentes y tamaños
- Espaciado y márgenes
- Iconos y elementos visuales

### Configuración de Base de Datos
- La base de datos se crea automáticamente al primer uso
- Archivo: `easypoint.db`
- Formato: SQLite3
- Respaldo recomendado: Copia periódica del archivo .db

### Agregar Nuevos Productos
Los productos se pueden agregar directamente en la base de datos:
```sql
INSERT INTO Productos (codigo_barras, nombre_producto, precio_venta, stock_actual) 
VALUES ('nuevo_codigo', 'Nombre del Producto', 25.00, 100);
```

---

## 🐛 Solución de Problemas

### Problemas Comunes

**❌ Error: "No se puede conectar a la base de datos"**
- **Solución**: Verifica que el archivo `easypoint.db` esté en el directorio de la aplicación
- **Alternativa**: Elimina el archivo .db para crear uno nuevo con datos iniciales

**❌ Error: "ModuleNotFoundError: No module named 'PySide6'"**
- **Solución**: Instala las dependencias con `pip install -r requirements.txt`
- **Verificación**: Activa el entorno virtual antes de ejecutar

**❌ La aplicación se cierra inesperadamente**
- **Solución**: Ejecuta desde terminal para ver errores detallados
- **Comando**: `python run_app.py` en la terminal

**❌ Los productos no aparecen en la búsqueda**
- **Solución**: Verifica que los productos estén en la base de datos
- **Verificación**: Revisa el archivo `schema.sql` para productos iniciales

**❌ Error de permisos al escribir en la base de datos**
- **Solución**: Verifica permisos de escritura en el directorio
- **Windows**: Ejecuta como administrador si es necesario

### Logs y Depuración
- Los errores se muestran en la consola al ejecutar `python run_app.py`
- Para depuración avanzada, revisa el código en los archivos .py
- La base de datos se puede inspeccionar con herramientas SQLite

---

## 📁 Estructura del Proyecto

```
easy_point/
├── 📄 run_app.py              # Punto de entrada principal
├── 📄 main_menu.py            # Menú principal del sistema
├── 📄 login.py                # Sistema de autenticación
├── 📄 venta.py                # Módulo de ventas para cajeros
├── 📄 historial_ventas.py     # Historial para administradores
├── 📄 nuevo_usuario.py        # Gestión de usuarios
├── 📄 db_manager.py           # Gestión de base de datos
├── 📄 schema.sql              # Esquema y datos iniciales
├── 📄 easypoint.db            # Base de datos SQLite
├── 📄 requirements.txt        # Dependencias de Python
├── 📄 .gitignore              # Archivos excluidos de Git
├── 📁 icons/                  # Iconos de la interfaz
│   ├── 🎨 dashboard.svg
│   ├── 🎨 inventory.svg
│   ├── 🎨 history.svg
│   ├── 🎨 analysis.svg
│   ├── 🎨 backup.svg
│   └── 🎨 settings.svg
└── 📁 venv/                   # Entorno virtual (si está configurado)
```

---

## 🤝 Soporte y Contribuciones

### Reportar Problemas
Si encuentras algún problema o tienes sugerencias:
1. Verifica que el problema no esté en la sección de "Solución de Problemas"
2. Crea un issue detallado con pasos para reproducir el error
3. Incluye información del sistema operativo y versión de Python

### Contribuciones
Las contribuciones son bienvenidas. Para contribuir:
1. Fork del repositorio
2. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit de tus cambios: `git commit -m 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear un Pull Request

---

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

## 🏷️ Versión

**Versión Actual**: 1.0.0  
**Fecha de Lanzamiento**: 2024  
**Desarrollado con**: Python 3.8+, PySide6, SQLite3

---

*EasyPoint - Simplificando la gestión de ventas para tu negocio* 🚀 