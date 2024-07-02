import os, time

from flask import Flask, jsonify, request

from flask_cors import CORS

"""
Para trabajar con archivos asegurar que un nombre de archivo 
proporcionado por el usuario sea seguro para guardarlo en el sistema de archivos.
"""

from werkzeug.utils import secure_filename
from app.models.item import Item
from app.database import init_app, init_db

"""
Crear las dependencias
pip freeze > requirements.txt

Instalar todas las dependencias
pip install -r requirements.txt

"""
d = os.path.dirname(__file__)
os.chdir(d)

ruta_destino = 'static/img/'


app = Flask(__name__)
CORS(app)

# Inicializar la base de datos con la aplicación Flask
init_app(app)

@app.route('/init-db')
def init_db_route():
    init_db()
    return "Base de datos inicializada correctamente."

@app.route('/')
def principal():
    return "."

@app.route('/items', methods=['POST'])
def create_item():
    # data = request.json
    data = request.form
    print("que hay en data ", data)
    archivo=request.files['slide1']
    print(archivo)
    # Trabajamos con la imagen
    # Utilizamos la función `secure_filename` para obtener un nombre de archivo seguro para la imagen cargada. 
    # Esta función elimina caracteres especiales que podrían causar problemas de seguridad.
    nombre_imagen = secure_filename(archivo.filename)

    print(">>>>>>>>>", nombre_imagen)

    # Separamos el nombre base del archivo y su extensión utilizando `os.path.splitext`.
    # Esto nos permite trabajar con el nombre y la extensión por separado.
    nombre_base, extension = os.path.splitext(nombre_imagen)

    # Generamos un nuevo nombre para el archivo utilizando el nombre base original y 
    # agregando un timestamp para asegurarnos de que el nombre del archivo sea único.
    # Concatenamos el nombre base, un guion bajo, el timestamp actual y la extensión.
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"

    # Guardamos el archivo en la ruta de destino utilizando el nuevo nombre generado.
    # `os.path.join` se asegura de que la ruta sea correcta, sin importar el sistema operativo.
    archivo.save(os.path.join(ruta_destino, nombre_imagen))



    nuevo_item = Item(nombre=data['nombre'], precio=data['precio'], medidas=data['medidas'], materiales=data['materiales'], codigo=data['codigo'], slide1=nombre_imagen)
    nuevo_item.save()
    return jsonify({'message': 'Item creado correctamente'}), 201


@app.route('/items', methods=['GET'])
def get_all_items():
    items = Item.get_all()
    items_json=[]
    for i in items:
        items_json.append(i.serialize())
    return items_json
    # Manera resumida:
    # return jsonify([movie.serialize() for movie in movies])


@app.route('/items/<int:id>', methods=['GET'])
def get_by_id(id):
    item = Item.get_by_id(id)
    if item:
        return jsonify(item.serialize())
    else:
        return jsonify({'message': 'Item no encontrado'}), 404

@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.get_by_id(id)
    if not item:
        return jsonify({'message': 'Item no encontrado'}), 404
    item.delete()
    return jsonify({'message': 'Item borrado'})

@app.route('/items/<int:id>', methods=['PUT'])
def update_movie(id):
    item = Item.get_by_id(id)
    if not item:
        return jsonify({'message': 'Item no encontrado'}), 404
    data = request.form
    item.nombre = data.get('nombre', item.nombre)
    item.precio = data.get('precio', item.precio)
    item.dimensiones = data.get('dimensiones', item.dimensiones)
    item.materiales = data.get('materiales', item.materiales)
    item.codigo = data.get('codigo', item.codigo)
    # item.slide1 = data.get('slide1', item.slide1)
    item.save()
    return jsonify({'message': 'Item actualizado correctamente'})


if __name__ == '__main__':
    app.run(debug=True)