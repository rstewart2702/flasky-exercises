# application package constructor:
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

from flask_login import LoginManager

login_manager = LoginManager()
# The following defines the endpoint for the login page.
# flask_login will redirect to login page when an anonymous user
# tries to access a protected page.
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()

db = SQLAlchemy()

# This is what Grinberg calls the "application factory function":
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    #
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # attach routes and custom error pages here.
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Attach the auth blueprint to the application:
    from .auth import auth as auth_blueprint
    # N.B. the url_prefix parameter means that all routes
    # defined in the auth blueprint will be registered with the
    # '/auth' prefix, in this case.
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    login_manager.init_app(app)

    return app
