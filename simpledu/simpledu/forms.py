from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, Required
from simpledu.models import db, User
from wtforms import ValidationError
import re

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[Required('请输入用户名'), Length(3, 24)])
    email = StringField('Email', validators=[Required('请输入youx'), Email()])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('Password again', validators=[Required(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已注册。')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册。')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user


class LoginForm(FlaskForm):
    #email = StringField('Email', validators=[Required(), Email()])
    
    
    username = StringField('Username',validators=[Required()])
    password = PasswordField('Password', validators=[Required(), Length(3, 24)])
    remember_me = BooleanField('Remember me')
    def validate_username(self, field):
        if field.data and not User.query.filter_by(username=field.data).first():
            raise ValidationError('username not register')

    # def validate_email(self, field):
    #     if field.data and not User.query.filter_by(email=field.data).first():
    #         raise ValidationError('email not register')

    def validate_password(self, field):
        #user = User.query.filter_by(email=self.email.data).first()
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('Password error')
    submit = SubmitField('Submit')
