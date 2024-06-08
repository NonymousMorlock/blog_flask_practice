from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import current_user

from database import db
from forms import CreatePostForm, CommentForm
from models.blog_post import BlogPost
from services import PostService
from utils import Response
from utils.utils import admin_only

blog_post = Blueprint('post', __name__)


@blog_post.route('/')
def get_all_posts():
    response: Response = PostService.get_all_posts()
    return render_template("index.html", all_posts=response.data or [])


# TODO: Allow logged-in users to comment on posts
@blog_post.route("/post/<int:post_id>", methods=['GET', 'POST'])
def show_post(post_id):
    form = CommentForm(comment=session.get('new_comment'))
    response: Response = PostService.get_post_by_id(post_id)
    if response.error_message:
        flash(response.error_message, response.error_category)
        return redirect(url_for('post.get_all_posts'))

    if form.validate_on_submit():
        session['new_comment'] = form.comment.data
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login', next=url_for('post.show_post', post_id=post_id)))

        comment_response: Response = PostService.comment_on_post(post=response.data, comment=form.comment.data)
        if comment_response.error_message:
            flash(comment_response.error_message, comment_response.error_category)
            return redirect(url_for('post.show_post', post_id=post_id))

        session.pop('new_comment')

        # Bad practice, Here, I wanted to just use the render_template below instead of redirecting and causing
        # fetches, but the form gets preserved, I mean when user reloads page, it attempts to resubmit form
        # form = CommentForm(formdata=None)
        # response = PostService.get_post_by_id(post_id)
        # if response.error_message:
        #     flash(response.error_message, response.error_category)
        #     return redirect(url_for('post.get_all_posts'))

        return redirect(url_for('post.show_posts', post_id=post_id))
    return render_template("post.html", post=response.data, form=form)


@blog_post.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        response: Response = PostService.create_post(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data
        )
        if response.error_message:
            flash(response.error_message, response.error_category)
            return redirect(url_for('post.add_new_post'))
        return redirect(url_for("post.get_all_posts"))
    return render_template("make-post.html", form=form)


@blog_post.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    if edit_form.validate_on_submit():
        response: Response = PostService.update_post(
            post=post,
            title=edit_form.title,
            subtitle=edit_form.subtitle,
            img_url=edit_form.img_url,
            body=edit_form.body
        )
        if response.error_message:
            flash(response.error_message, response.error_category)
            return redirect(url_for('post.edit_post', post_id=post.id))
        return redirect(url_for("post.show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@blog_post.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    response: Response = PostService.delete_post(post_id)
    if response.error_message:
        flash(response.error_message, response.error_category)
    return redirect(url_for('post.get_all_posts'))
