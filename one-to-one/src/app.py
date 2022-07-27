from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, User, Profile

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
Migrate(app, db) # db init, db migrate, db upgrade


@app.route('/', methods=['GET'])
def main():
    return jsonify({ 
        "msg": "API REST Flask",
        "users": "https://5000-ljavierrodr-introtorela-jkvlmtp2174.ws-us54.gitpod.io/api/users"
    }), 200

@app.route('/api/users', methods=['GET'])
def list_users():

    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))

    return jsonify(users), 200

@app.route('/api/users', methods=['POST'])
def create_user():

    username = request.json.get('username')
    password = request.json.get('password')

    biography = request.json.get('biography', "")
    instagram = request.json.get('instagram', "")
    facebook = request.json.get('facebook', "")
    twitter = request.json.get('twitter', "")
    linkedin = request.json.get('linkedin', "")
    github = request.json.get('github', "")

    """ 
    user = User()
    user.username = username
    user.password = password
    db.session.add(user)
    db.session.commit()

    profile = Profile()
    profile.biography = biography
    profile.facebook = facebook
    profile.instagram = instagram
    profile.twitter = twitter
    profile.linkedin = linkedin
    profile.github = github
    profile.users_id = user.id
    db.session.add(profile)
    db.session.commit() 
    """

    user = User()
    user.username = username
    user.password = password


    profile = Profile()
    profile.biography = biography
    profile.facebook = facebook
    profile.instagram = instagram
    profile.twitter = twitter
    profile.linkedin = linkedin
    profile.github = github
    
    user.profile = profile
    db.session.add(user)
    db.session.commit()

    return jsonify(user.serialize()), 201

@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):

    username = request.json.get('username')
    password = request.json.get('password')

    biography = request.json.get('biography', "")
    instagram = request.json.get('instagram', "")
    facebook = request.json.get('facebook', "")
    twitter = request.json.get('twitter', "")
    linkedin = request.json.get('linkedin', "")
    github = request.json.get('github', "")

    userFound = User.query.filter_by(username=username).first()

    if userFound: return jsonify({ "status": "failed", "code": 400, "message": "Username exists!", "data": None }), 400
    
    user = User.query.get(id) # SELECT * FROM users WHERE id = 1;

    if not user:  return jsonify({ "status": "failed", "code": 404, "message": "User not found", "data": None }), 404
    
    user.username = username if username is not None else user.username
    user.password = password 


    """ 
    profile = Profile.query.filter_by(users_id=user.id).first()
    profile.biography = biography
    profile.facebook = facebook
    profile.instagram = instagram
    profile.twitter = twitter
    profile.linkedin = linkedin
    profile.github = github 
    """


    user.profile.biography = biography
    user.profile.facebook = facebook
    user.profile.instagram = instagram
    user.profile.twitter = twitter
    user.profile.linkedin = linkedin
    user.profile.github = github


    db.session.commit()

    data = {
        "status": "success",
        "code": 200,
        "message": "User updated!",
        "data": user.serialize()
    }

    return jsonify(data), 200


@app.route('/api/profile/<int:id>', methods=['GET'])
def get_profile(id):
    profile = Profile.query.get(id)
    return jsonify(profile.serialize()), 200

@app.route('/api/profile/<int:id>', methods=['PUT'])
def update_profile(id):

    password = request.json.get('password')

    profile = Profile.query.get(id)
    profile.user.password = password if password is not None else profile.user.password
    
    return jsonify(profile.serialize()), 200

if __name__ == '__main__':
    app.run()