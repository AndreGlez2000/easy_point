# EasyPoint - Sistema de Punto de Venta

Sistema simple de punto de venta desarrollado con PySide6.

## Requisitos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
```

2. Activar el entorno virtual:
- En Windows:
```bash
.\venv\Scripts\activate
```
- En Linux/Mac:
```bash
source venv/bin/activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecutar la aplicación

1. Con el entorno virtual activado, ejecutar:
```bash
python main_menu.py
```

## Funcionalidades
- Acceso para cajeros y administradores
- Sistema de autenticación con PIN
- Interfaz gráfica moderna y fácil de usar 

## Estructura del Sistema

### 1. Módulo de Login
- Acceso diferenciado para Cajeros y Administradores
- Sistema de autenticación mediante PIN
- Redirección automática según rol:
  - Cajeros: Módulo de Venta
  - Administradores: Módulo de Historial de Ventas

### 2. Módulo de Venta
- Interfaz intuitiva para proceso de venta
- Lectura de códigos de barras mediante webcam (usando OpenCV y pyzbar)
- Gestión de productos y cantidades
- Procesamiento de diferentes métodos de pago

### 3. Módulo de Administración
- Visualización completa del historial de ventas
- Gestión de inventario
- Administración de usuarios 