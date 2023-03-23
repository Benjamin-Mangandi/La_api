from flask import Flask, Request, jsonify, request
import random
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

#STIKERS

#CARGAR STIKERS
@app.route('/stiker', methods=["POST"])
def cargar_stikers():
    stikers_por_cargar = request.get_json(True)
    if len(stikers)>0:
        for stiker in stikers_por_cargar:
            for stikercargados in stikers:
                if stiker["id_stiker"] == stikercargados["id_stiker"]:
                    stikers_por_cargar.remove(stiker)
    for stiker in stikers_por_cargar:
        stikers.append(stiker)
    respuesta = {
    "msg": "Stikers cargados con exito!",
    "status": 200
    }
    return jsonify(respuesta)

#OBTENER STIKER
@app.route('/stiker', methods=["GET"])
def buscar_stikers():
    nombre = request.args.get("name")
    apellido = request.args.get("lastname")
    coincidencias_stiker =[]
    for stiker in stikers:
        if stiker["stiker_player_name"]==nombre and stiker["stiker_player_lastname"]==apellido:
            coincidencias_stiker.append(stiker)
    return jsonify(coincidencias_stiker)

#ELIMINAR STIKER
@app.route('/stiker/<int:id>', methods=['DELETE'])
def eliminar_stiker(id):
    for stiker in stikers:
        if stiker["id_stiker"] == id:
            stikers.remove(stiker)
            respuesta = {
                "msg": "Stiker eliminado con exito.",
                "status": 200
            }
            return jsonify(respuesta)
    respuesta_negativa ={
        "msg": "No se encontró el Stiker, por favor verifique el ID.",
        "status": 404
    }
    return jsonify(respuesta_negativa)

#SOBRES
@app.route('/box/<user>', methods=['GET'])
def conseguir_stikers(user):
    for usuario in usuarios:
        if usuario["user_nickname"]==user:
            auxiliar_stikers =[]
            while len(auxiliar_stikers)<5:
                numero_random = random.randint(0, 1000)
                for stiker in stikers:
                    if stiker["id_stiker"]==numero_random:
                        auxiliar_stikers.append(stiker)
                        usuario["user_stikers"].append(stiker)
                        break
            return jsonify(auxiliar_stikers)
    respuesta_negativa ={
            "msg": "No se encontró el usuario, por favor verifique el Nickname",
            "status": 404
        }
    return jsonify(respuesta_negativa)

#INICIAR
if __name__ == ('__main__'):
    app.run(port=3050, debug=True)