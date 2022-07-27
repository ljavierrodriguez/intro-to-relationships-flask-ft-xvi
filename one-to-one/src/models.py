from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile = db.relationship("Profile", backref="user", uselist=False) # <Profile 1>

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "profile": self.profile.serialize()
        }


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    biography = db.Column(db.Text(), default="")
    instagram = db.Column(db.String(100), default="")
    facebook = db.Column(db.String(100), default="")
    twitter = db.Column(db.String(100), default="")
    linkedin = db.Column(db.String(100), default="")
    github = db.Column(db.String(100), default="")
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    def serialize(self): 
        return {
            "id": self.id,
            "biography": self.biography,
            "instagram": self.instagram,
            "facebook": self.facebook,
            "twitter": self.twitter,
            "linkedin": self.linkedin,
            "github": self.github,
            "users_id": self.users_id,
            "username": self.user.username, # user es el backref hacia la tabla users
            "password": self.user.password
        }