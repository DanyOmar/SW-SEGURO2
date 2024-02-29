from flask import request, Response
from bson import json_util, ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

from config.mongodb import mongo

STUDENTNAME_FIELD = 'student_name'
STUDENTLASTNAME_FIELD = 'student_lastname'

EMAIL_FIELD = 'email'
CAREER_FIELD = 'career'
ERROR_MISSING_FIELDS = 'Faltan campos obligatorios: {}.'
ERROR_INVALID_CREDENTIALS = 'Credenciales inválidas.'
ERROR_USER_EXISTS = 'Estudiante ya existe.'
ERROR_USER_NOT_FOUND = 'Estudiante no encontrado.'

def create_student_service():
    data = request.get_json()
    student_name = data.get(STUDENTNAME_FIELD, None)
    student_lastname = data.get(STUDENTLASTNAME_FIELD, None)
    email = data.get(EMAIL_FIELD, None)
    career = data.get(CAREER_FIELD, None)
    
    if not student_name or not student_lastname or not career or not email:
        return {'error': ERROR_MISSING_FIELDS.format(', '.join([STUDENTNAME_FIELD, STUDENTLASTNAME_FIELD, EMAIL_FIELD, CAREER_FIELD ]))}, 400

    usuario = {
        STUDENTNAME_FIELD: student_name,
        STUDENTLASTNAME_FIELD: student_lastname,
        EMAIL_FIELD: email,
        CAREER_FIELD: career,
        #PASSWORD_FIELD: pass_hash
    }

    # Verificar si el usuario ya existe
    if mongo.db.students.find_one({EMAIL_FIELD: email}):
        return {'error': ERROR_USER_EXISTS}, 400

    mongo.db.students.insert_one(usuario)
    return {'mensaje': 'Estudiante creado exitosamente'}, 201
    
def get_students_service():
    students = mongo.db.students.find()
    result = json_util.dumps(students)
    return Response(result, mimetype='application/json')

def get_student_service(id):
    student = mongo.db.students.find_one({'_id': ObjectId(id)})
    result = json_util.dumps(student)
    return Response(result, mimetype='application/json')

def update_student_service(id):
    student = request.get_json()
    student_name_up = student.get(STUDENTNAME_FIELD, None)
    student_lastname_up = student.get(STUDENTLASTNAME_FIELD, None)
    new_data = {}
    if student_name_up and student_lastname_up:
        # Validar la complejidad de la nueva contraseña
        #pass_hash = generate_password_hash(passwordUP, method="pbkdf2:sha256")
        new_data[STUDENTNAME_FIELD] = student_name_up
        new_data[STUDENTLASTNAME_FIELD] = student_lastname_up
    else:
        return {'error': ERROR_MISSING_FIELDS.format(', '.join([STUDENTNAME_FIELD, STUDENTLASTNAME_FIELD]))}, 400

    actual_user = mongo.db.students.find_one({'_id': ObjectId(id)})
    if not actual_user:
        return {'error': ERROR_USER_NOT_FOUND}, 404
    
    
    

    response = mongo.db.students.update_one({'_id': ObjectId(id)}, {'$set': new_data})

    if response.modified_count > 0:
        return {'message': 'Estudiante actualizado exitosamente'}
    else:
        return {'error': 'No se encontró el estudiante'}, 400
    
def delete_student_service(id):
    response = mongo.db.students.delete_one({'_id': ObjectId(id)})
    if response.deleted_count > 0:
        return {'message': 'Estudiante eliminado exitosamente'}
    else:
        return {'error': 'No se encontró el estudiante'}, 400