from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Integer, String(size), Text, DateTime, Float, Boolean, PickleType, LargeBinary

roles_users = db.Table('roles_users',
   db.Column('roles_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
   db.Column('users_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    users = db.relationship('User', secondary=roles_users)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_active": self.is_active    
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    roles = db.relationship('Role', secondary="roles_users") # [<Role 1>, <Role 2>]

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "is_active": self.is_active,
            "roles": self.get_roles()    
        }

    def get_roles(self):
        return list(map(lambda role: role.serialize(), self.roles)) # []

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


""" class RoleUser(db.Model):
    __tablename__ = 'roles_users'
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True) """