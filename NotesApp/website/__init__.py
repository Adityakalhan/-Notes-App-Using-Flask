from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app() :
    app = Flask(__name__) #initialising of the flask app
    app.config['SECRET_KEY'] = 'secret_key_for_app' #used for session information
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #if user is not logged in, they will be directed to this page
    login_manager.init_app(app) #to let the login manager know about which app is being used
    
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix = '/')
    app.register_blueprint(auth,url_prefix = '/')
    
    from .models import User, Note

    with app.app_context() :
        db.create_all()
        print("DataBase Created!")

    @login_manager.user_loader #for loading the user
    def load_user(id) :
        return User.query.get(int(id))
    return app

