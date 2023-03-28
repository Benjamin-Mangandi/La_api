from flask import Flask, Request, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

#ARREGLOS

usuarios = []
stikers = []

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

#INICIAR SESION
@app.route('/user/login', methods=['POST'])
def logearse():
    datos_de_usuario = request.get_json(True)
    for usuario in usuarios:
        if datos_de_usuario["user_nickname"]==usuario["user_nickname"] and datos_de_usuario["user_password"]== usuario["user_password"]:
            return {
                "msg": "Sesión iniciada, Bienvenido",
                "autorizado":True,
                "status": 200,
                "id_user": usuario["id_user"]
            }
    return{
        "msg": "Datos Incorrectos, por favor verifique sus datos",
        "autorizado": False,
        "status": 404
    }

#ACTUALIZAR USUARIO
@app.route('/user/<id>', methods=['PUT'])
def modificar_usuario(id):
    for usuario in usuarios:
        if usuario["id_user"]==id:
            body_usuario= request.get_json(True)
            usuario["user_name"] = body_usuario.get("user_name")
            usuario["user_nickname"] = body_usuario.get("user_nickname")
            usuario["user_password"] = body_usuario.get("user_password")
            usuario["user_stikers"] = body_usuario.get("user_stikers")
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


#INICIAR
if __name__ == ('__main__'):
    app.run(port=3050, debug=True)
