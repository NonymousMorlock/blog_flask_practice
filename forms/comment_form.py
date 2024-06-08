from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    comment = CKEditorField('Comment', validators=[DataRequired()])
    submit = SubmitField('SUBMIT COMMENT')
