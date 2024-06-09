from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
# from flask_gravatar import Gravatar
from flask_login import LoginManager

from config import Config
from database import db
from utils import gravatar_url


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)
    ckeditor = CKEditor()
    bootstrap5 = Bootstrap5()
    login_manager = LoginManager()

    login_manager.login_view = 'auth.login'
    login_manager.init_app(flask_app)
    ckeditor.init_app(flask_app)
    bootstrap5.init_app(flask_app)
    db.init_app(flask_app)

    flask_app.jinja_env.filters['gravatar'] = gravatar_url

    with flask_app.app_context():
        __import__('models')
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id: str):
        from models import User
        return User.query.filter_by(alternative_id=user_id).first()

    from controllers import register_blueprints
    register_blueprints(flask_app)

    return flask_app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=False)
