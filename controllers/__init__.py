from flask import Flask

from .auth_controller import auth
from .info_controller import info
from .post_controller import blog_post

__all__ = ['auth', 'info', 'blog_post', 'register_blueprints']


def register_blueprints(app: Flask):
    app.register_blueprint(auth)
    app.register_blueprint(info)
    app.register_blueprint(blog_post)
