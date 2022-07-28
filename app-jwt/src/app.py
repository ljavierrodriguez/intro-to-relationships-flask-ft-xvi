from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['JWT_SECRET_KEY'] = '33b9b3de94a42d19f47df7021954eaa8' 

db.init_app(app)
Migrate(app, db)
jwt = JWTManager(app)

@app.route('/')
def main():
    return jsonify({ "msg": "API REST FLASK" }), 200


@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username: return jsonify({ "msg": "Username is required" }), 400
    if not password: return jsonify({ "msg": "Password is required" }), 400

    userFound = User.query.filter_by(username=username, is_active=True).first()

    if not userFound: return jsonify({ "status":"failed", "message": "Username/Password are incorrect" }), 401
    if not check_password_hash(userFound.password, password): return jsonify({ "status":"failed", "message": "Username/Password are incorrect" }), 401

    expires = datetime.timedelta(minutes=5)
    access_token = create_access_token(identity=userFound.id, expires_delta=expires)

    data = {
        "access_token": access_token,
        "user": userFound.serialize()
    }

    return jsonify({ "status": "success", "message": "Login successfully", "data": data }), 200



@app.route('/api/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username: return jsonify({ "msg": "Username is required" }), 400
    if not password: return jsonify({ "msg": "Password is required" }), 400
    
    user = User()
    user.username = username
    user.password = generate_password_hash(password)
    user.save()

    if user:
        return jsonify({ "status": "success", "message": "Registro exitoso"}), 200
    else: 
        return jsonify({ "status": "faild", "message": "Registro no exitoso, por favor intente de nuevo"}), 200


@app.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
    id = get_jwt_identity()
    current_user = User.query.get(id)

    return jsonify(current_user.serialize()), 200


@app.route('/api/contact', methods=['GET'])
@jwt_required()
def contact():
    id = get_jwt_identity()
    current_user = User.query.get(id)

    return jsonify(current_user.serialize()), 200

if __name__ == '__main__':
    app.run()
