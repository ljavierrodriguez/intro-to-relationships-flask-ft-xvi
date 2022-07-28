from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Role

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'secre-key'

db.init_app(app)
Migrate(app, db)
jwt = JWTManager(app)

@app.route('/')
def main():
    return jsonify({ "msg": "API REST FLASK" }), 200


@app.route('/api/register', methods=['POST'])
def register():

    username = request.json.get('username')
    password = request.json.get('password')
    roles = request.json.get('roles')

    user = User()
    user.username = username
    user.password = generate_password_hash(password)

    if roles:
        for roles_id in roles:
            role = Role.query.get(roles_id)
            user.roles.append(role)

    user.save()

    return jsonify(user.serialize()), 200


@app.route('/api/register/<int:id>', methods=['PUT'])
def register_update(id):

    username = request.json.get('username')
    password = request.json.get('password')
    roles_update = request.json.get('roles')

    user = User.query.get(id)
    #user.username = username
    #user.password = generate_password_hash(password)

    if roles_update:
        for role in user.roles:
            if not role.id in roles_update:
                user.roles.remove(role)

        for role_id in roles_update:
            new_role = Role.query.get(role_id)
            if not new_role in user.roles:
                user.roles.append(new_role)

    user.update()

    return jsonify(user.serialize()), 200



if __name__ == '__main__':
    app.run()