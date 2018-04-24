from flask import Flask, render_template
from flask_migrate import Migrate
from simpledu.config import configs
from simpledu.models import db,Course
from flask_login import LoginManager
from simpledu.models import User
from .handlers import front,course,admin,user,live,ws
from flask_sockets import Sockets

a = '1233'

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
    app.register_blueprint(live)

def register_extensions(app):
    db.init_app(app)
    Migrate(app,db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    sockets = Sockets(app)
    sockets.register_blueprint(ws)
    

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)
    
    login_manager.login_view = 'front.login'
    login_manager.login_message = '请先登录'
    login_manager.login_message_category = 'danger'
