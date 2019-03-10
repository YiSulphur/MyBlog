from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField,BooleanField, PasswordField
from wtforms.validators import DataRequired,Length,EqualTo

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

class CommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

class SignupForm(FlaskForm):
    username = username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    password_two = PasswordField('Repeat for confirmation', validators=[EqualTo('password',message="Don't Match!")])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign up')