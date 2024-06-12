from typing import List, TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import db

if TYPE_CHECKING:
    from app.models import BlogPost
    from app.models import Comment


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    passwordHash: Mapped[str] = mapped_column(String(250), nullable=False)
    alternative_id: Mapped[str] = mapped_column(String(100), nullable=False)
    posts: Mapped[List["BlogPost"]] = relationship(back_populates="author")
    comments: Mapped[List['Comment']] = relationship(back_populates='author')

    def get_id(self):
        return self.alternative_id
