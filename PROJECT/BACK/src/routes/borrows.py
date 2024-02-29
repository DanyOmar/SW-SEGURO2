from flask import Blueprint

from services.borrows import create_borrow_service, get_borrows_service, get_borrow_service, update_borrow_service, delete_borrow_service

borrow = Blueprint('borrow', __name__)

@borrow.route('/', methods=['GET'])
def get_borrows():
    return get_borrows_service()

@borrow.route('/<id>', methods=['GET'])
def get_borrow(id):
    return get_borrow_service(id)

@borrow.route('/', methods=['POST'])
def create_borrow():
    return create_borrow_service()

@borrow.route('/<id>', methods=['PUT'])
def update_user(id):
    return update_borrow_service(id)

@borrow.route('/<id>', methods=['DELETE'])
def delete_user(id):
    return delete_borrow_service(id)
