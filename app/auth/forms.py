from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User

class RegistrationForm(FlaskForm):
  email = StringField('email', validators=[DataRequired(), Length(1, 64), Email()])
  username = StringField('Username', validators=[DataRequired(), Length(1,64),
                                                  Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                                         'Usernames must have only letters,numbers,dots or ''underscores')])
  password = PasswordField('password', validators=[DataRequired(), EqualTo('password2', message ='password must match with confirm password')])
  password2 = PasswordField('Confirm Password', validators= [DataRequired(), EqualTo('password',message = 'confirm password must match with password')])

  def validate_email(self,field):
    if User.query.filter_by(email=field.data).first():
      raise ValidationError('email already registered.')
  def validate_username(self,field):
      if User.query.filter_by(username = field.data).first():
        raise ValidationError("Username is already taken.Kindly select another username")
  submit = SubmitField('Sign Up')
      

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('password', validators=[DataRequired()])  # Corrected this line
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('Log In')
