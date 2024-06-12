from hashlib import sha256
from typing import Callable
from urllib.parse import urlencode

from flask_login import current_user, login_required
from flask import abort


def gravatar_url(email, size=100, rating='g', default='retro', force_default=False, ):
    hash_value = sha256(email.lower().encode('utf-8')).hexdigest()
    query_params = urlencode({'d': default, 's': str(size), 'r': rating, 'f': force_default})
    return f"https://www.gravatar.com/avatar/{hash_value}?{query_params}"


def admin_only(func: Callable) -> Callable:

    @login_required
    def closure(*args, **kwargs):
        if current_user.id == 1:
            return func(*args, **kwargs)
        return abort(403)

    closure.__name__ = func.__name__
    return closure
