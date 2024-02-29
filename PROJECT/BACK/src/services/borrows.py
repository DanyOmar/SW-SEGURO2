from flask import request, Response
from bson import json_util, ObjectId
from datetime import datetime, timedelta

from config.mongodb import mongo

BOOKID_FIELD = 'book_id'
STUDENTID_FIELD = 'student_id'
BORROWDATE_FIELD = 'borrow_date'
RETURNDATE_FIELD = 'return_date'
BOOKNAME_FIELD = 'book_name'
STUDENTNAME_FIELD = 'student_name'

ERROR_MISSING_FIELDS = 'Faltan campos obligatorios: {}.'

def create_borrow_service():
    data = request.get_json()
    book_id = data.get(BOOKID_FIELD, None)
    student_id = data.get(STUDENTID_FIELD, None)
    borrow_date = data.get(BORROWDATE_FIELD, None)
    
    # Validación de campos obligatorios
    if not book_id or not student_id or not borrow_date:
        return {'error': ERROR_MISSING_FIELDS.format(','.join([BOOKID_FIELD, STUDENTID_FIELD, BORROWDATE_FIELD]))}, 400

    # Verificar si el libro y el estudiante existen
    book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    student = mongo.db.students.find_one({'_id': ObjectId(student_id)})
    if not book or not student:
        return {'error': 'Libro o estudiante no encontrado'}, 404

    # Obtener el nombre del libro y del estudiante
    book_name = book.get('title')
    student_name = f"{student.get('student_name')} {student.get('student_lastname')}"
    
    # Validación de fecha de préstamo
    try:
        borrow_date = datetime.strptime(borrow_date, "%Y-%m-%d")
    except ValueError:
        return {'error': 'Formato de fecha de préstamo inválido. Use el formato AAAA-MM-DD'}, 400

    # Fecha de devolución por defecto (7 días después de la fecha de préstamo)
    return_date = borrow_date + timedelta(days=7)

    borrow = {
        BOOKID_FIELD: book_id,
        STUDENTID_FIELD: student_id,
        BOOKNAME_FIELD: book_name,
        STUDENTNAME_FIELD: student_name,
        BORROWDATE_FIELD: borrow_date,
        RETURNDATE_FIELD: return_date
    }

    # Insertar préstamo en la base de datos
    mongo.db.borrows.insert_one(borrow)

    return {'message': 'Préstamo registrado exitosamente'}

def get_borrows_service():
    borrows = mongo.db.borrows.find()
    result = json_util.dumps(borrows)
    return Response(result, mimetype='application/json')

def get_borrow_service(id):
    borrow = mongo.db.borrows.find_one({'_id': ObjectId(id)})
    result = json_util.dumps(borrow)
    return Response(result, mimetype='application/json')

def update_borrow_service(id):
    data = request.get_json()
    updates = {}

    book_id = data[BOOKID_FIELD]
    book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    if not book:
        return {'error': 'Libro no encontrado'}, 404
    updates[BOOKID_FIELD] = book_id
    updates[BOOKNAME_FIELD] = book.get('title')

    student_id = data[STUDENTID_FIELD] 
    student = mongo.db.students.find_one({'_id': ObjectId(student_id)})
    if not student:
        return {'error': 'Estudiante no encontrado'}, 404
    updates[STUDENTID_FIELD] = student_id
    updates[STUDENTNAME_FIELD] = f"{student.get('student_name')} {student.get('student_lastname')}"

    try:
        updates[BORROWDATE_FIELD] = datetime.strptime(data[BORROWDATE_FIELD], "%Y-%m-%d")
    except ValueError:
        return {'error': 'Formato de fecha de préstamo inválido. Use el formato AAAA-MM-DD'}, 400

    # Actualizar el préstamo en la base de datos
    response = mongo.db.borrows.update_one({'_id': ObjectId(id)}, {'$set': updates})

    if response.modified_count > 0:
        return {'message': 'Préstamo actualizado exitosamente'}
    else:
        return {'error': 'No se encontró el préstamo'}, 404

def delete_borrow_service(id):
    # Eliminar el préstamo de la base de datos
    response = mongo.db.borrows.delete_one({'_id': ObjectId(id)})

    if response.deleted_count > 0:
        return {'message': 'Préstamo eliminado exitosamente'}
    else:
        return {'error': 'No se encontró el préstamo'}, 404
