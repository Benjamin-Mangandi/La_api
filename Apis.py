from flask import Flask, Request, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

#ARREGLOS

usuarios = []

#USUARIOS

#OBTENER USUARIO
@app.route('/user/<id>', methods=['GET'])
def ver_usuario(id):
    for usuario in usuarios:
        if usuario["id_user"]==id:
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
        if usuario["id_user"]==id:
            body_usuario= request.get_json(True)
            usuario["user_name"] = body_usuario.get("user_name")
            usuario["user_password"] = body_usuario.get("user_password") 
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
        if usuario["id_user"] == nuevo_usuario.get("id_user"):
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
        if usuario["id_user"]==id:
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
