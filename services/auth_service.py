import uuid

from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from database import db
from models import User
from utils import Response


class AuthService:
    @staticmethod
    def register_user(name: str, email: str, password: str) -> Response:
        user = User(
            name=name,
            passwordHash=generate_password_hash(password=password),
            email=email,
            alternative_id=str(uuid.uuid4())
        )
        try:
            db.session.add(user)
            db.session.commit()
            return Response(data=user)
        except IntegrityError as e:
            if any('user.email' in arg for arg in e.args):
                return Response(
                    redirect_url='auth.login',
                    error_message='Email already in use',
                    error_category='danger'
                )
            return Response(error_message='Something went wrong', error_category='danger')

    @staticmethod
    def authenticate_user(email: str, password: str) -> Response:
        user: User = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if not user or not check_password_hash(pwhash=user.passwordHash, password=password):
            return Response(error_message='Invalid Credentials!', error_category='danger')
        return Response(user)
