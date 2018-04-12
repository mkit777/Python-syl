from flask import Flask, render_template
from flask_migrate import Migrate
from simpledu.config import configs
from simpledu.models import db,Course
from flask_login import LoginManager
from simpledu.models import User
from .handlers import front,course,admin,user

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_extensions(app)
    register_blueprints(app)
    return app


def register_blueprints(app):  
    app.register_blueprint(front)
    app.register_blueprint(course)
    app.register_blueprint(admin)
    app.register_blueprint(user)

def register_extensions(app):
    db.init_app(app)
    Migrate(app,db)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)
    
    login_manager.login_view = 'front.login'
