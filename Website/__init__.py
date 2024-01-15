from flask import Flask
from flask_sqlalchemy import SQLAlchemy                             #This is what we use for the database


#Creates a database
db= SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'DASDSJFJSAN FSDASAD'                #Secure the cookies of our data, this is the key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  #This means that the alchemy database is located at this location

    db.init_app(app)
    
    from .views import views
    from .auth import auth      #Imports the blueprints 

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')                    #/ means no prefix, if you put someething there it means that you want something specific
    
    #Checks if we have created the database yet
    with app.app_context():
        db.create_all()
    
    return app

   



