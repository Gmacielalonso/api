from app.database import get_db

class Item:
    def __init__(self, id, nombre, precio, medidas, materiales, codigo, slide1, slide2, slide3):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.medidas = medidas
        self.materiales = materiales
        self.codigo = codigo
        self.slide1 = slide1
        self.slide2 = slide2
        self.slide3 = slide3

    # Método para guardar o actualizar
    def save(self):
        db = get_db()  # Obtener la conexión a la base de datos
        cursor = db.cursor()
        if self.id:
            # Si existe un ID, se actualiza su registro en la base de datos
            cursor.execute("""
                UPDATE items SET nombre = %s, precio = %s, medidas = %s, materiales = %s, codigo = %s, self.slide1 = %s, self.slide2 = %s, self.slide3 = %s
                WHERE id = %s
            """, (self.nombre, self.precio, self.medidas, self.materiales, self.codigo, self.slide1, self.slide2, self.slide3, self.id))
        else:
            # Si la película no tiene un ID, se inserta un nuevo registro en la base de datos
            cursor.execute("""
                INSERT INTO items (nombre, precio, medidas, materiales, codigo, slide1, slide2, slide3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (self.nombre, self.precio, self.medidas, self.materiales, self.codigo, self.slide1, self.slide2, self.slide3))
            self.id = cursor.lastrowid  # Obtener el ID asignado por la base de datos
        db.commit()  # Confirmar la transacción
        cursor.close()

    # Método estático para obtener todas las películas con sus reseñas de la base de datos
    @staticmethod
    def get_all():
        """
        Retorna un listado de OBJETOS Movie, cada uno con sus reseñas.
        """
        db = get_db()  # Obtener la conexión a la base de datos
        cursor = db.cursor()
        cursor.execute("""
            SELECT 
                i.id, i.nombre, i.precio, i.dimensiones, i.materiales, i.codigo, i.slide1, i.slide2, i.slide3
            FROM 
                items i
        """)  # Ejecutar la consulta para obtener todo
        rows = cursor.fetchall()  # Obtener todos los resultados
        
        items_dict = {}
        
        for row in rows:
            id = row[0]
            if id not in items_dict:
                items_dict[id] = Item(
                    id=row[0], nombre=row[1], precio=row[2], dimensiones=row[3], materiales=row[4], codigo=row[5], slide1=row[6], slide2=row[7], slide3=row[8]
                )

        cursor.close()
        return list(items_dict.values())  # Devolver la lista de items

    @staticmethod
    def get_by_id(id):
        db = get_db()
        cursor = db.cursor()

        # Ejecutar la consulta con JOIN 
        cursor.execute("""
            SELECT 
                i.id, i.nombre, i.precio, i.dimensiones, i.materiales, i.codigo, i.slide1, i.slide2, i.slide3
            FROM 
                items i
            WHERE 
                i.id = %s
        """, (id,))
        
        rows = cursor.fetchall()
        cursor.close()

        if rows:
            # Utilizamos un diccionario para mapear por su ID para evitar duplicados
            item_map = {}
            for row in rows:
                if row[0] not in item_map:
                    # Si no está en el mapeo, lo añadimos con sus datos básicos
                    item_map[row[0]] = Item(id=row[0], nombre=row[1], precio=row[2], dimensiones=row[3], materiales=row[4], codigo=row[5], slide1=row[6], slide2=row[7], slide3=row[8])

            # Devolver item encontrado por su ID
            return item_map[id]

        return None  # Si no se encontró, devolver None
    # Método para eliminar un item de la base de datos
    def delete(self):
        db = get_db()  # Obtener la conexión a la base de datos
        cursor = db.cursor()
        cursor.execute("DELETE FROM items WHERE id = %s", (self.id,))  # Ejecutar la consulta para eliminar
        db.commit()  # Confirmar la transacción
        cursor.close()

    # Método para serializar un objeto Movie a un diccionario
    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'medidas': self.medidas, 
            'materiales': self.materiales,
            'codigo': self.codigo,
            'slide1': self.slide1,
            'slide2': self.slide2,
            'slide3': self.slide3
        }

    def __str__(self):
        return f"Items: {self.id} - {self.nombre} - {self.precio}"
