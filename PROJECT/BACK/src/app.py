from flask import Flask, render_template, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os

from config.mongodb import mongo
from routes.todo import todo
from routes.users import user
from routes.students import student
from routes.borrows import borrow

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True, send_wildcard=True)  # Agrega send_wildcard=True

app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user', methods=['OPTIONS'])  # Agrega una ruta específica para OPTIONS en /user
def handle_options():
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')  # Configura el origen permitido para CORS
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response, 200

app.register_blueprint(todo, url_prefix='/todo')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(student, url_prefix='/student')
app.register_blueprint(borrow, url_prefix='/borrow')

if __name__ == '__main__':
    app.run(debug=True)
