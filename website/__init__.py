from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

mail = Mail()

db=SQLAlchemy()
migrate=Migrate()
load_dotenv()
secret_key=os.getenv('secret_key')
gmail_password=os.getenv('gmail_password')
database_uri=os.getenv('database_uri')

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']=secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'carolnjerikariuki94@gmail.com'
    app.config['MAIL_PASSWORD'] = gmail_password
    app.config['MAIL_DEFAULT_SENDER'] ='carolnjerikariuki94@gmail.com'

    upload_folder = os.path.join(app.root_path, 'static', 'image')
    app.config['UPLOAD_FOLDER'] = upload_folder
    
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    mail.init_app(app)
    db.init_app(app)

    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    from .models import User,Post,Comment
    from .forms  import SignupForm,LoginForm,UpdateProfileForm,AddPostForm,CommentForm
    migrate.init_app(app, db) 

    return app