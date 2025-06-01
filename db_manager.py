# filepath: c:\\Users\\Andre\\Documents\\easy_point\\db_manager.py
import sqlite3
import hashlib # For PIN hashing (recommended)
from datetime import datetime

DATABASE_NAME = "easypoint.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row # Access columns by name
    conn.execute("PRAGMA foreign_keys = ON;") # Ensure foreign keys are enforced
    return conn

def create_initial_schema_if_needed():
    """
    Checks if tables exist and creates them using schema.sql if not.
    This is a basic check; a more robust migration system might be needed for complex apps.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if a key table (e.g., Usuarios) exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Usuarios';")
        if not cursor.fetchone():
            print("Database schema not found. Attempting to create from schema.sql...")
            try:
                with open("schema.sql", "r") as f:
                    sql_script = f.read()
                conn.executescript(sql_script)
                conn.commit()
                print("Database schema created successfully.")
            except sqlite3.Error as e:
                print(f"Error creating schema: {e}")
            except FileNotFoundError:
                print("ERROR: schema.sql not found. Please ensure it's in the same directory.")
    finally:
        conn.close()

# --- User Management ---

def _hash_pin(pin):
    """Hashes a PIN using SHA256. In a real app, use a stronger, salted hash."""
    # return hashlib.sha256(pin.encode()).hexdigest()
    return pin # Placeholder for now, as schema stores plain text

def add_user(nombre_usuario, pin, tipo_usuario):
    """Adds a new user to the Usuarios table."""
    # hashed_pin = _hash_pin(pin) # Use this once hashing is fully implemented in schema & login
    hashed_pin = pin 
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Usuarios (nombre_usuario, pin, tipo_usuario)
            VALUES (?, ?, ?)
        """, (nombre_usuario, hashed_pin, tipo_usuario))
        conn.commit()
        return True, "Usuario agregado exitosamente."
    except sqlite3.IntegrityError: # Handles UNIQUE constraint violation for nombre_usuario
        return False, "El nombre de usuario ya existe."
    except sqlite3.Error as e:
        return False, f"Error de base de datos: {e}"
    finally:
        conn.close()

def validate_user_pin(nombre_usuario, pin_ingresado):
    """
    Validates a user's PIN against their username (case-insensitive).
    Returns (is_valid, user_id, user_name, message).
    """
    # hashed_pin_ingresado = _hash_pin(pin_ingresado) # Use once hashing is implemented
    hashed_pin_ingresado = pin_ingresado
    conn = get_db_connection()
    cursor = conn.cursor()
    user_id = None
    user_name = None
    try:
        # Case-insensitive username check
        cursor.execute("""
            SELECT id_usuario, nombre_usuario, pin, tipo_usuario FROM Usuarios WHERE LOWER(nombre_usuario) = LOWER(?)
        """, (nombre_usuario,))
        
        user_record = cursor.fetchone()

        if user_record:
            if user_record['pin'] == hashed_pin_ingresado:
                user_id = user_record['id_usuario']
                user_name = user_record['nombre_usuario'] # Or a specific 'display_name' field if you add one
                # Optionally, you might want to return tipo_usuario as well if needed by the caller
                return True, user_id, user_name, "PIN válido."
            else:
                return False, None, None, "PIN incorrecto."
        else:
            return False, None, None, "Nombre de usuario no encontrado."
            
    except sqlite3.Error as e:
        return False, None, None, f"Error de base de datos: {e}"
    finally:
        conn.close()

# --- Product Management ---

def get_product_by_code_or_name(term):
    """Fetches products matching a barcode or name fragment."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Search by barcode OR by name (case-insensitive)
        cursor.execute("""
            SELECT id_producto, codigo_barras, nombre_producto, precio_venta, stock_actual 
            FROM Productos 
            WHERE codigo_barras LIKE ? OR nombre_producto LIKE ?
        """, (f'%{term}%', f'%{term}%'))
        products = cursor.fetchall()
        return products # Returns a list of Row objects
    except sqlite3.Error as e:
        print(f"Error al buscar productos: {e}")
        return []
    finally:
        conn.close()

def get_product_by_id(id_producto):
    """Fetches a single product by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id_producto, codigo_barras, nombre_producto, precio_venta, stock_actual 
            FROM Productos 
            WHERE id_producto = ?
        """, (id_producto,))
        product = cursor.fetchone()
        return product # Returns a Row object or None
    except sqlite3.Error as e:
        print(f"Error al obtener producto por ID: {e}")
        return None
    finally:
        conn.close()

# --- Sales Management ---

def record_sale(id_usuario_cajero, total_venta, metodo_pago, detalles_venta):
    """
    Records a sale and its details in the database.
    detalles_venta is a list of dictionaries:
    [{'id_producto': X, 'cantidad': Y, 'precio_unitario_venta': Z, 'subtotal_linea': W}, ...]
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 1. Insert into Ventas table with local time
        fecha_local = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            INSERT INTO Ventas (id_usuario_cajero, fecha_venta, total_venta, metodo_pago)
            VALUES (?, ?, ?, ?)
        """, (id_usuario_cajero, fecha_local, total_venta, metodo_pago))
        id_venta_nueva = cursor.lastrowid # Get the ID of the newly inserted sale

        if not id_venta_nueva:
            conn.rollback()
            return False, "No se pudo obtener el ID de la nueva venta."

        # 2. Insert into DetallesVenta table and update stock for each product
        for detalle in detalles_venta:
            cursor.execute("""
                INSERT INTO DetallesVenta (id_venta, id_producto, cantidad, precio_unitario_venta, subtotal_linea)
                VALUES (?, ?, ?, ?, ?)
            """, (id_venta_nueva, detalle['id_producto'], detalle['cantidad'], 
                  detalle['precio_unitario_venta'], detalle['subtotal_linea']))
            
            # 3. Update product stock
            cursor.execute("""
                UPDATE Productos SET stock_actual = stock_actual - ? 
                WHERE id_producto = ? AND stock_actual >= ?
            """, (detalle['cantidad'], detalle['id_producto'], detalle['cantidad']))
            
            if cursor.rowcount == 0:
                # This means stock was insufficient or product ID was wrong.
                # For simplicity, we roll back the entire transaction.
                # A more sophisticated approach might handle partial successes or specific errors.
                conn.rollback()
                return False, f"Stock insuficiente o error al actualizar producto ID: {detalle['id_producto']}."

        conn.commit()
        return True, "Venta registrada exitosamente."
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Error de base de datos al registrar la venta: {e}"
    finally:
        conn.close()

# Call this once at the start of your application (e.g., in main.py)
# create_initial_schema_if_needed()
