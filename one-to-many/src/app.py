from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, User, Article

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'

db.init_app(app)
Migrate(app, db)

@app.route('/api/articles', methods=['GET', 'POST'])
def list_and_create_post():

    if request.method == 'GET':
        articles = Article.query.all()
        articles = list(map(lambda article: article.serialize(), articles))

        return jsonify(articles), 200

    
    if request.method == 'POST':
        
        data = request.get_json()

        article = Article()
        article.title = data['title']
        article.body = data['body']
        article.users_id = data['users_id']

        db.session.add(article)
        db.session.commit()

        return jsonify(article.serialize()), 201



@app.route('/api/users/<int:id>/articles', methods=['GET'])
def get_user_articles(id):
    user = User.query.get(id)
    return jsonify(user.serialize_with_articles()), 200


@app.route('/api/users/<int:id>/articles/<int:articles_id>', methods=['DELETE'])
def delete_user_articles(id, articles_id):
    user = User.query.get(id)
    article = Article.query.get(articles_id)
    #db.session.delete(article)
    #db.session.commit()
    user.articles.remove(article)

    return jsonify(user.serialize_with_articles()), 200


if __name__ == '__main__':
    app.run()