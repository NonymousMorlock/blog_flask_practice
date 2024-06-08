from database import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import User
    from models import BlogPost


class Comment(db.Model):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    author: Mapped['User'] = relationship(back_populates='comments')
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    parent_post: Mapped['BlogPost'] = relationship(back_populates='comments')