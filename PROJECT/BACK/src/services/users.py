from flask import request, Response
from bson import json_util, ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

from config.mongodb import mongo

USERNAME_FIELD = 'user_name'
PASSWORD_FIELD = 'password'
EMAIL_FIELD = 'email'
ERROR_MISSING_FIELDS = 'Faltan campos obligatorios: {}.'
ERROR_INVALID_CREDENTIALS = 'Credenciales inválidas.'
ERROR_USER_EXISTS = 'Usuario ya existe.'
ERROR_USER_NOT_FOUND = 'Usuario no encontrado.'

def create_user_service():
    data = request.get_json()
    user_name = data.get(USERNAME_FIELD, None)
    email = data.get(EMAIL_FIELD, None)
    password = data.get(PASSWORD_FIELD, None)
    
    if not user_name or not email or not password:
        return {'error': ERROR_MISSING_FIELDS.format(', '.join([USERNAME_FIELD, PASSWORD_FIELD, EMAIL_FIELD]))}, 400

    pass_hash = generate_password_hash(password, method="pbkdf2:sha256")

    usuario = {
        USERNAME_FIELD: user_name,
        EMAIL_FIELD: email,
        PASSWORD_FIELD: pass_hash
        
    }

    # Verificar si el usuario ya existe
    if mongo.db.users.find_one({EMAIL_FIELD: email}):
        return {'error': ERROR_USER_EXISTS}, 400

    mongo.db.users.insert_one(usuario)
    return {'mensaje': 'Usuario creado exitosamente'}, 201
    
def get_users_service():
    users = mongo.db.users.find()
    result = json_util.dumps(users)
    return Response(result, mimetype='application/json')

def get_user_service(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    result = json_util.dumps(user)
    return Response(result, mimetype='application/json')

def update_user_service(id):
    user = request.get_json()
    user_name_up = user.get(USERNAME_FIELD, None)
    password_up = user.get(PASSWORD_FIELD, None)	

    if password_up and user_name_up:
        # Validar la complejidad de la nueva contraseña
        pass_hash = generate_password_hash(password_up, method="pbkdf2:sha256")
    else:
        return {'error': ERROR_MISSING_FIELDS.format(', '.join([USERNAME_FIELD, PASSWORD_FIELD]))}, 400

    actual_user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if not actual_user:
        return {'error': ERROR_USER_NOT_FOUND}, 404
    
    new_data = {}
    new_data[USERNAME_FIELD] = user_name_up
    new_data[PASSWORD_FIELD] = pass_hash

    response = mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': new_data})

    if response.modified_count > 0:
        return {'message': 'Usuario actualizado exitosamente'}
    else:
        return {'error': 'No se encontró el usuario'}, 400
    
def delete_user_service(id):
    response = mongo.db.users.delete_one({'_id': ObjectId(id)})
    if response.deleted_count > 0:
        return {'message': 'Usuario eliminado exitosamente'}
    else:
        return {'error': 'No se encontró el libro'}, 400