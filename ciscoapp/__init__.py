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
from ciscoapp.net.routes import net
from ciscoapp.main.routes import main
from ciscoapp.gen.routes import gen


app.register_blueprint(users)
app.register_blueprint(net)
app.register_blueprint(main)
app.register_blueprint(gen)



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    from ciscoapp.users.routes import users
    from ciscoapp.net.routes import net
    from ciscoapp.main.routes import main
    from ciscoapp.gen.routes import gen
    
    app.register_blueprint(users)
    app.register_blueprint(net)
    app.register_blueprint(main)
    app.register_blueprint(gen)
    
    return app
    
    