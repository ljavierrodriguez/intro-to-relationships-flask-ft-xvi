from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    articles = db.relationship('Article', backref="user") # [<Article 1>, <Article 2>]

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
        }

    def serialize_with_articles(self):
        return {
            "id": self.id,
            "username": self.username,
            "articles": self.get_articles()
        }

    def get_articles(self):
        return list(map(lambda article: { "id": article.id, "title": article.title }, self.articles))

    
class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.now())
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    #user = db.relationship('User')

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "date": self.date,
            "user": self.user.username
        }

    def serialize_with_author(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "date": self.date,
            "user": self.user.username
        }