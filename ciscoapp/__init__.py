from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from ciscoapp.config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from ciscoapp.users.routes import users
from ciscoapp.network_automation.routes import network_automation
from ciscoapp.main.routes import main
from ciscoapp.base_config.routes import base_config


app.register_blueprint(users)
app.register_blueprint(network_automation)
app.register_blueprint(main)
app.register_blueprint(base_config)



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    from ciscoapp.users.routes import users
    from ciscoapp.network_automation.routes import network_automation
    from ciscoapp.main.routes import main
    from ciscoapp.base_config.routes import base_config
    
    app.register_blueprint(users)
    app.register_blueprint(network_automation)
    app.register_blueprint(main)
    app.register_blueprint(base_config)
    
    return app
    
    