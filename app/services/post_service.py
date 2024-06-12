from datetime import date

from flask_login import current_user

from database import db
from app.models import BlogPost, Comment
from app.utils import Response


class PostService:
    @staticmethod
    def get_all_posts() -> Response:
        return Response(db.session.execute(db.select(BlogPost)).scalars().all())

    @staticmethod
    def get_post_by_id(post_id: int) -> Response:
        try:
            return Response(db.get_or_404(BlogPost, post_id))
        except BaseException as exception:
            return Response(error_message=exception.args[0], error_category='danger')

    @staticmethod
    def create_post(title: str, subtitle: str, body: str, img_url: str) -> Response:
        try:
            new_post = BlogPost(
                title=title,
                subtitle=subtitle,
                body=body,
                img_url=img_url,
                author=current_user,
                date=date.today().strftime("%B %d, %Y")
            )
            db.session.add(new_post)
            db.session.commit()
            return Response(new_post)
        except BaseException as exception:
            return Response(error_message=exception.args[0], error_category='danger')

    @staticmethod
    def update_post(post: BlogPost, title: str, subtitle: str, img_url: str, body: str) -> Response:
        try:
            post.title = title
            post.subtitle = subtitle
            post.img_url = img_url
            post.author = current_user
            post.body = body
            db.session.commit()
            return Response(post)
        except BaseException as exception:
            return Response(error_message=exception.args[0], error_category='danger')

    @staticmethod
    def delete_post(post_id: int) -> Response:
        try:
            post_to_delete = db.get_or_404(BlogPost, post_id)
            db.session.delete(post_to_delete)
            db.session.commit()
            return Response()
        except BaseException as exception:
            return Response(error_message=exception.args[0], error_category='danger')

    @staticmethod
    def comment_on_post(post: BlogPost, comment: str) -> Response:
        try:
            comment = Comment(
                text=comment,
                author=current_user,
                parent_post=post,
            )
            db.session.add(comment)
            db.session.commit()
            return Response(comment)
        except BaseException as exception:
            return Response(error_message=exception.args[0], error_category='danger')

    @staticmethod
    def get_all_comments() -> Response:
        try:
            return Response(Comment.query.all())
        except BaseException as exception:
            return Response(error_message=exception.args[0], error_category='danger')


