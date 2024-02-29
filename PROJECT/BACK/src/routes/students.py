from flask import Blueprint

from services.students import create_student_service, get_students_service, get_student_service, update_student_service, delete_student_service

student = Blueprint('student', __name__)

@student.route('/', methods=['GET'])
def get_students():
    return get_students_service()

@student.route('/<id>', methods=['GET'])
def get_student(id):
    return get_student_service(id)

@student.route('/', methods=['POST'])
def create_student():
    return create_student_service()

@student.route('/<id>', methods=['PUT'])
def update_student(id):
    return update_student_service(id)

@student.route('/<id>', methods=['DELETE'])
def delete_student(id):
    return delete_student_service(id)
