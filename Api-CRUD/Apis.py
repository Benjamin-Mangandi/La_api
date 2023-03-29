from flask import Flask, Request, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)
CORS(app)

#ARREGLOS

usuarios = []


connection = None

try:
    connection = mysql.connector.connect(
        host='localhost',
        port=3306,
        database='Prueba',
        user='root',
        password='practicas'
    )

    if connection.is_connected():
        db_info = connection.get_server_info()
        print(f"Conectado a la base de datos MySQL {db_info}")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM No")
        resultado=cursor.fetchall()
        for row in resultado:
            print(row)

except Error as e:
    print(f"Error al conectarse a la base de datos: {e}")

finally:
    if connection is not None and connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión a la base de datos cerrada.")

#USUARIOS

#OBTENER USUARIO
@app.route('/user/<id>', methods=['GET'])
def ver_usuario(id):
    for usuario in usuarios:
        if usuario["ID"]==id:
            return jsonify(usuario)
    respuesta_negativa={
        "msg": "No se encontró el usuario, por favor verifique el ID",
        "status": 404
    }
    return jsonify(respuesta_negativa)

#ACTUALIZAR USUARIO
@app.route('/user/<id>', methods=['PUT'])
def modificar_usuario(id):
    for usuario in usuarios:
        if usuario["ID"]==id:
            body_usuario= request.get_json(True)
            usuario["nombre"] = body_usuario.get("nombre")
            usuario["carnet"] = body_usuario.get("carnet") 
            respuesta={
                "msg": "Usuario modificado con exito!",
                "status": 200
            }
            return jsonify(respuesta)
    respuesta_negativa={
        "msg": "No se encontró el usuario, por favor verifique el ID",
        "status": 404
    }
    return jsonify(respuesta_negativa)  
          
#CREAR USUARIO
@app.route('/user', methods=["POST"])
def crear_usuario():
    nuevo_usuario = request.get_json(True)
    for usuario in usuarios:
        if usuario["ID"] == nuevo_usuario.get("ID"):
            respuesta_negativa={
                "msg": "Un usuario ya existe con ese ID",
                "status": 400
            }
            return jsonify(respuesta_negativa)
    usuarios.append(nuevo_usuario)
    respuesta = {
    "msg": "Usuario creado con exito!",
    "status": 200
    }
    return jsonify(respuesta)

#ELIMINAR USUARIO
@app.route('/user/<id>', methods=["DELETE"])
def eliminar_usuario(id):
    for usuario in usuarios:
        if usuario["ID"]==id:
            usuarios.remove(usuario)
            respuesta={
                "msg": "Usuario eliminado con exito!",
                "status": 200
            }
            return jsonify(respuesta)
    respuesta_negativa={
        "msg": "No se encontró el usuario, por favor verifique el ID",
        "status": 404
    }
    return jsonify(respuesta_negativa)  

#INICIAR
if __name__ == ('__main__'):
    app.run(port=3050, debug=True)
