from .conexion_db import ConexionDB
from tkinter import messagebox

def crear_tablas():
    conexion = ConexionDB()

    # Crear tabla de Clientes
    sql_clientes = '''
    CREATE TABLE IF NOT EXISTS clientes(
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(100),
        apellido VARCHAR(100),
        direccion VARCHAR(100),
        telefono VARCHAR(100),
        correo_electronico VARCHAR(100),
        fecha_registro DATE,
        informacion_adicional TEXT
    )'''
    conexion.cursor.execute(sql_clientes)

    # Crear tabla de Compras
    sql_compras = '''
    CREATE TABLE IF NOT EXISTS compras(
        id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        fecha_compra DATE,
        total_compra DECIMAL(10, 2),
        FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente)
    )'''
    conexion.cursor.execute(sql_compras)

    # Crear tabla de Productos
    sql_productos = '''
    CREATE TABLE IF NOT EXISTS productos(
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_producto VARCHAR(100),
        descripcion TEXT,
        precio DECIMAL(10, 2),
        stock_disponible INTEGER
    )'''
    conexion.cursor.execute(sql_productos)

    # Crear tabla de Detalles de Compra
    sql_detalles_compra = '''
    CREATE TABLE IF NOT EXISTS detalles_compra(
        id_detalle_compra INTEGER PRIMARY KEY AUTOINCREMENT,
        id_compra INTEGER,
        id_producto INTEGER,
        cantidad_comprada INTEGER,
        precio_unitario DECIMAL(10, 2),
        FOREIGN KEY (id_compra) REFERENCES compras (id_compra),
        FOREIGN KEY (id_producto) REFERENCES productos (id_producto)
    )'''
    conexion.cursor.execute(sql_detalles_compra)

    # Crear tabla de Garantías
    sql_garantias = '''
    CREATE TABLE IF NOT EXISTS garantias(
        id_garantia INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        id_producto INTEGER,
        fecha_inicio_garantia DATE,
        fecha_vencimiento_garantia DATE,
        descripcion_problema TEXT,
        estado_garantia VARCHAR(100),
        FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
        FOREIGN KEY (id_producto) REFERENCES productos (id_producto)
    )'''
    conexion.cursor.execute(sql_garantias)

    # Crear tabla de Contactos
    sql_contactos = '''
    CREATE TABLE IF NOT EXISTS contactos(
        id_contacto INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        fecha_contacto DATE,
        tipo_contacto VARCHAR(100),
        descripcion_contacto TEXT,
        seguimiento_requerido BOOLEAN,
        observaciones_adicionales TEXT,
        FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente)
    )'''
    conexion.cursor.execute(sql_contactos)

    conexion.cerrar()

    titulo = 'Crear Registro'
    mensaje = 'Se crearon las tablas en la base de datos'
    messagebox.showinfo(titulo, mensaje)


def borrar_tablas():
    conexion = ConexionDB()

    # Borrar tabla de Contactos
    sql_contactos = 'DROP TABLE IF EXISTS contactos'
    conexion.cursor.execute(sql_contactos)

    # Borrar tabla de Garantías
    sql_garantias = 'DROP TABLE IF EXISTS garantias'
    conexion.cursor.execute(sql_garantias)

    # Borrar tabla de Detalles de Compra
    sql_detalles_compra = 'DROP TABLE IF EXISTS detalles_compra'
    conexion.cursor.execute(sql_detalles_compra)

    # Borrar tabla de Productos
    sql_productos = 'DROP TABLE IF EXISTS productos'
    conexion.cursor.execute(sql_productos)

    # Borrar tabla de Compras
    sql_compras = 'DROP TABLE IF EXISTS compras'
    conexion.cursor.execute(sql_compras)

    # Borrar tabla de Clientes
    sql_clientes = 'DROP TABLE IF EXISTS clientes'
    conexion.cursor.execute(sql_clientes)

    conexion.cerrar()

    titulo = 'Borrar Registro'
    mensaje = 'Las tablas de la base de datos se borraron con éxito'
    messagebox.showinfo(titulo, mensaje)

class Cliente:
    def __init__(self, nombre, apellido, direccion, telefono, correo_electronico, fecha_registro, informacion_adicional):

        self.id_cliente = None
        self.nombre = nombre 
        self.apellido = apellido
        self.direccion = direccion 
        self.telefono = telefono
        self.correo_electronico = correo_electronico
        self.fecha_registro = fecha_registro
        self.informacion_adicional = informacion_adicional

    def __str__(self):
        return f'Cliente[{self.nombre}, {self.apellido}, {self.direccion}, {self.telefono}, {self.correo_electronico}, {self.fecha_registro}, {self.informacion_adicional}]'

def guadar_cliente(cliente):
    conexion = ConexionDB()

    sql = f"""INSERT INTO clientes (nombre, apellido, direccion, telefono, correo_electronico, fecha_registro, informacion_adicional) VALUES('{cliente.nombre}', '{cliente.apellido}', '{cliente.direccion}', '{cliente.telefono}', '{cliente.correo_electronico}', '{cliente.fecha_registro}', '{cliente.informacion_adicional}')"""

    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        titulo = 'Conexion al Registro'
        mensaje = 'REGISTRADO CORRECTAMENTE'
        messagebox.showerror(titulo, mensaje)
    except:
        titulo = 'Conexion al Registro'
        mensaje = 'ERROR AL TRY REGISTRO'
        messagebox.showerror(titulo, mensaje)

def listar():
    conexion = ConexionDB()

    lista_clientes = []
    sql = 'SELECT * FROM clientes'

    try: 
        conexion.cursor.execute(sql)
        lista_clientes = conexion.cursor.fetchall()
        conexion.cerrar()
    except:
        titulo = 'Conexion al Registro '
        mensaje = 'Crea la tabla en la Base de datos'
        messagebox.showwarning(titulo, mensaje)

    return lista_clientes

def editar(cliente, id_cliente):
    conexion = ConexionDB()

    sql = f"""UPDATE clientes 
    SET nombre = '{cliente.nombre}', direccion = '{cliente.direccion}',
    telefono = '{cliente.telefono}'
    WHERE id_cliente = {id_cliente}"""

    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()

    except:
        titulo = 'Edición de datos'
        mensaje = 'No se apodido editar este registro'
        messagebox.showerror(titulo, mensaje)

def listar_busqueda(cliente):
    conexion = ConexionDB()

    lista_clientes = []
    sql = f"""SELECT * FROM clientes WHERE nombre = '{cliente.nombre}'"""

    try: 
        conexion.cursor.execute(sql)
        lista_clientes = conexion.cursor.fetchall()
        conexion.cerrar()
    except:
        titulo = 'Conexion al Registro '
        mensaje = 'Ha ocurrido un ERROR al buscar'
        messagebox.showwarning(titulo, mensaje)

    return lista_clientes

def eliminar(id_cliente):
    conexion = ConexionDB()
    sql = f'DELETE FROM clientes WHERE id_cliente = {id_cliente}'

    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
    except:
        titulo = 'Eliminar Datos'
        mensaje = 'No se pudo eliminar el registro'
        messagebox.showerror(titulo, mensaje)


class Usuario:
    def __init__(self, usuario, contraseña, nivel_acceso):
        self.id_usuario = None
        self.usuario = usuario
        self.contraseña = contraseña
        self.nivel_acceso = nivel_acceso

    def __str__(self):
        return f'Estudiante[{self.nombre}, {self.cedula}, {self.correo}]'

def crear_tabla_usuarios():
    conexion = ConexionDB()

    sql = '''
    CREATE TABLE usuarios(
        id_usuario INTEGER,
        usuario VARCHAR(100) NOT NULL,
        contraseña VARCHAR(100)NOT NULL,
        nivel_acceso VARCHAR(20)NOT NULL, 
        PRIMARY KEY(id_usuario AUTOINCREMENT),
        UNIQUE(usuario),
        CHECK(nivel_acceso == "bajo" OR nivel_acceso == "medio" OR nivel_acceso == "alto")

    )'''
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        titulo = 'Crear Registro'
        mensaje = 'Se creo la tabla en la base datos'
        messagebox.showinfo(titulo, mensaje)
    except:
        titulo = 'Crear Registro'
        mensaje = 'La tabla ya esta creada'
        messagebox.showwarning(titulo, mensaje)

def guadar_usuario(usuario):
    conexion = ConexionDB()

    sql = f"""INSERT INTO usuarios (usuario, contraseña, nivel_acceso)
    VALUES('{usuario.usuario}', '{usuario.contraseña}', '{usuario.nivel_acceso}')"""

    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()

    except:
        titulo = 'Conexion al Registro'
        mensaje = 'La tabla usuario no esta creada en la base de datos'
        messagebox.showerror(titulo, mensaje)

def listar_usuarios():
    conexion = ConexionDB()

    lista_usuarios = []
    sql = 'SELECT * FROM usuarios'

    try: 
        conexion.cursor.execute(sql)
        lista_usuarios = conexion.cursor.fetchall()
        conexion.cerrar()
    except:
        titulo = 'Conexion al Registro '
        mensaje = 'error usuarios'
        messagebox.showwarning(titulo, mensaje)

    return lista_usuarios

def listar_busqueda_usuarios(usuario):
    conexion = ConexionDB()

    lista_usuarios = []
    sql = f"""SELECT * FROM usuarios WHERE usuario = '{usuario.usuario}'"""

    try: 
        conexion.cursor.execute(sql)
        lista_usuarios = conexion.cursor.fetchall()
        conexion.cerrar()
    except:
        titulo = 'Conexion al Registro '
        mensaje = 'Ha ocurrido un ERROR al buscar'
        messagebox.showwarning(titulo, mensaje)

    return lista_usuarios