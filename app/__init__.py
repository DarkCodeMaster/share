from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_login import login_required
from flask_pagedown import PageDown

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'user.login'
login_manager.login_message = '请先进行登录'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    from .api.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .api.Users import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')
    from .api.Posts import post as post_blueprint
    app.register_blueprint(post_blueprint, url_prefix='/post')

    @app.route('/secret', methods=['GET', 'POST'])
    @login_required
    def secret():
        return '只有已登录用户才能查看'


    return app