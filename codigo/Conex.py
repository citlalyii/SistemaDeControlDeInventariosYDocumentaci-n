import sqlite3

def crearbd_tablas():
    """Funcion que verifica si las tablas existen en la base de datos en caso de que no, las crea."""
    try:
        conexion = sqlite3.connect('scrnissan.db')
        cursor = conexion.cursor()

        # Verificar si las tablas existen
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('usuarios', 'directorio','toner', 'inventario_computo','salida_toner','toner_modelo','toner_tipo','toner_color')")
        existentes = cursor.fetchall()

        # Tabla 'usuarios'
        if ('usuarios',) not in existentes:
            cursor.execute("""
                CREATE TABLE `usuarios` (
                  `idusuarios` INTEGER PRIMARY KEY AUTOINCREMENT,
                  `nombre` TEXT,
                  `usuario` TEXT,
                  `contraseña` TEXT,
                  `confirmarC` TEXT,
                  `estado` INTEGER DEFAULT 1,
                  `puesto` TEXT,
                  `tipo` TEXT        
                )
            """)
            print("Tabla 'usuarios' creada")

            # Insertar un usuario por defecto
            contraseña="03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"
            confirmar="03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"
            cursor.execute("""
                INSERT INTO usuarios (nombre, usuario, contraseña, confirmarC, estado, puesto, tipo)
                VALUES (?, ?, ?, ?, ?, ?,?)
            """, ('admin', 'admin', contraseña, confirmar, 1, 'Administrador', 'Administrador'))
            print("Usuario por defecto creado")

        if ('directorio',) not in existentes:
            cursor.execute("""
                CREATE TABLE `directorio` (
                  `iddirect` INTEGER PRIMARY KEY AUTOINCREMENT,
                  `extencion` INTEGER DEFAULT '0',
                  `nombre` TEXT NOT NULL,
                  `puesto` TEXT NOT NULL,
                  `correo` TEXT NOT NULL,
                  `celular` INTEGER NOT NULL DEFAULT '0',
                  `empresa` INTEGER NOT NULL DEFAULT '0',
                  `ldirect` INTEGER NOT NULL DEFAULT '0'
                )
            """)
            print("Tabla 'directorio' creada")

        if ('toner',) not in existentes:
            cursor.execute("""
                CREATE TABLE `toner` (
                  `idtoner` INTEGER PRIMARY KEY AUTOINCREMENT,
                  `cantidad` INTEGER,
                  `tipo` TEXT,
                  `modelo` TEXT,
                  `color` TEXT
                )
            """)
            print("Tabla 'toner' creada")
        
        if ('salida_toner',) not in existentes:
            cursor.execute("""
            CREATE TABLE `salida_toner`(
                `idsalida` INTEGER PRIMARY KEY AUTOINCREMENT,
                `Nombre` TEXT,
                `Area` TEXT,
                `Firma` BLOB,
                `autoriza` BLOB,
                `Producto` TEXT,
                `fecha` TEXT,      
                `hora` TEXT,      
                `folio` INTEGER     
                )
            """)
            print("Tabla de salidas de toner creada")

        if ('inventario_computo',) not in existentes:
            cursor.execute("""
                 CREATE TABLE `inventario_computo` (
                  `idComputo` INTEGER PRIMARY KEY AUTOINCREMENT,
                  `responsable` TEXT,
                  `area` TEXT,
                  `articulo` TEXT,
                  `marcaModelo` TEXT DEFAULT 'Sin Marca o Modelo',
                  `serie` TEXT DEFAULT 'Sin Número de serie',
                  `descripcion` TEXT DEFAULT 'Sin descripción',
                  `estado` TEXT,
                  `observ` TEXT DEFAULT 'Sin observaciones',
                  `manten` TEXT DEFAULT 'No Realizado',
                  `imagen` BLOB DEFAULT 'Sin imagen',
                  `nombre_img` TEXT DEFAULT 'Sin imagen'
                )
            """)
            print("Tabla 'Inventario_computo' creada")

        if ('toner_modelo',) not in existentes:
            cursor.execute("""
                 CREATE TABLE `toner_modelo` (
                  `idopcion` INTEGER PRIMARY KEY AUTOINCREMENT,
                  `nombre` TEXT
                )
            """)
            print("Tabla 'toner_modelo' creada")

        if ('toner_tipo',) not in existentes:
            cursor.execute("""
                 CREATE TABLE `toner_tipo` (
                  `idopcion` INTEGER PRIMARY KEY AUTOINCREMENT,
                  `nombre` TEXT
                )
            """)
            print("Tabla 'toner_tipo' creada")

        if ('toner_color',) not in existentes:
            cursor.execute("""
                 CREATE TABLE `toner_color` (
                  `idopcion` INTEGER PRIMARY KEY AUTOINCREMENT,
                  `nombre` TEXT
                )
            """)
            print("Tabla 'toner_color' creada")
        conexion.commit()
        print("¡Las tablas ya se han creado!")

    except sqlite3.Error as error:
        print("Error al crear las tablas:", error)

    finally:
        if conexion:
            conexion.close()

# Llamar a la función para crear las tablas
crearbd_tablas()
