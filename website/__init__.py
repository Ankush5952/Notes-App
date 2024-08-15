from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def createApp():
    app:Flask = Flask(__name__)  #create the app
    app.config['SECRET_KEY'] = 'secretkey'   #setting a secret key to encrypt cookies and session data
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    
    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix = "/")
    app.register_blueprint(auth,url_prefix = "/")
    
    from .models import User,Note
    createDatabase(app)
    
    loginManager = LoginManager()
    loginManager.login_view = "auth.login"
    loginManager.init_app(app)
    
    @loginManager.user_loader
    def loadUser(id):
        return User.query.get(int(id))
    
    return app

def createDatabase(app:Flask):
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()