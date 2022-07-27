# Paso 1: Crear mi estructura del proyecto (carpetas y archivos)

    - proyecto
        - src
            app.py
            models.py
        - Pipfile
        - .gitignore
        
# Paso 2: Activar el entorno virtual (pipenv)

    $ pipenv shell

# Paso 3: Instalar los modulos requeridos en el proyecto

    $ pipenv install flask flask-migrate flask-sqlalchemy

# Paso 4: Configurar mi archivo principal (app.py)

    from flask import Flask

    app = Flask(__name__)


# Paso 5A: Configurar el inicio de la app en archivo y ejecutar con python el archivo

Agregamos esto al final de mi documento
    ...
    app.config['DEBUG'] = True
    app.config['ENV'] = 'development'

    if __name__ == '__main__':
        app.run()

Ejecutarmos en el terminal:    

    $ python src/app.py

# Paso 5B: Configurar el comando flask en el terminal

    $ export FLASK_APP=src/app.py
    $ export FLASK_DEBUG=True
    $ export FLASK_ENV=development
    $ flask run

# Paso 6: Crear los modelos de la aplicaciones

    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()

    class ModelName(db.Model):
        ....

# Paso 7: Vincular los models con la aplicacion principal

    ...
    from flask_migrate import Migrate
    from models import db
    ...
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    - A:
        app.condig['SQLALCHEMY_DATABASE_URI'] = 'dialect+driver://user:pass@host:port/dbname' # mysql, postgresql, oralcel etc 
    - B:
        app.condig['SQLALCHEMY_DATABASE_URI'] = 'dialect:///dbname' # sqlite
    
    db.init_app(app)
    Migrate(app, db) # db init, db migrate, db upgrade
