from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RGBTextForm(FlaskForm):
    text_content = StringField('Text Content', validators=[DataRequired(), Length(max=100)])
    font_size = IntegerField('Font Size', validators=[DataRequired()])
    animation_speed = FloatField('Animation Speed', validators=[DataRequired()])
    glow_intensity = IntegerField('Glow Intensity', validators=[DataRequired()])
    color_1 = StringField('Color 1', validators=[DataRequired()])
    color_2 = StringField('Color 2', validators=[DataRequired()])
    color_3 = StringField('Color 3', validators=[DataRequired()])
    font_weight = IntegerField('Font Weight', validators=[DataRequired()])
    letter_spacing = IntegerField('Letter Spacing', validators=[DataRequired()])
    shadow_color = StringField('Shadow Color', validators=[DataRequired()])
    submit = SubmitField('Save to Profile')
