from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,IntegerField
from wtforms.validators import Length, Email, EqualTo, Required,URL,NumberRange
from simpledu.models import db, User,Course,Live
from wtforms import ValidationError
import re
from flask import flash

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[Required('请输入用户名'), Length(3, 24)])
    email = StringField('Email', validators=[Required('请输入邮箱'), Email()])
    password = PasswordField('Password', validators=[Required('请输入密码'), Length(6, 24)])
    repeat_password = PasswordField('Password again', validators=[Required('请确保两次密码输入相同'), EqualTo('password')])
    submit = SubmitField('提交')

    def validate_username(self, field):
        if not field.data.isalnum():
            flash('username not all num','danger')
            raise ValidationError()
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
    
    
    username = StringField('Username',validators=[Required('请输入用户名')])
    password = PasswordField('Password', validators=[Required('请输入密码'), Length(3, 24)])
    remember_me = BooleanField('下次自动登录')
    def validate_username(self, field):
        if field.data and not User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名未被注册')

    # def validate_email(self, field):
    #     if field.data and not User.query.filter_by(email=field.data).first():
    #         raise ValidationError('email not register')

    def validate_password(self, field):
        #user = User.query.filter_by(email=self.email.data).first()
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')
    submit = SubmitField('提交')

class CourseForm(FlaskForm):
    name = StringField('课程名称', validators=[Required(), Length(5,32)])
    description = TextAreaField('课程简介',validators=[Required(), Length(20, 256)])
    image_url = StringField('封面副片', validators=[Required(), URL()])
    author_id = IntegerField('作者ID', validators=[Required(), NumberRange(min=1, message='无效的用户ID')])
    submit = SubmitField('提交')

    def validate_author_id(self, field):
        if not User.query.get(field.data):
            raise ValidationError('用户不存在')
    
    def create_course(self):
        course = Course()
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course
    
    def update_course(self, course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

class UserForm(FlaskForm):
    username = StringField('用户名', validators=[Required(),Length(3, 24)])
    email = StringField('邮箱', validators=[Required(), Email()])
    role = IntegerField('角色', validators=[Required(), NumberRange(0,30)])
    password = PasswordField('密码',validators=[Required()])
    job = StringField('工作', validators=[Required()])
    submit = SubmitField('提交')    
    
    def add_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user

    def update_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user
    
class LiveForm(FlaskForm):
    id = IntegerField('ID',validators=[Required()])
    name = StringField('Live Name',validators=[Required(),Length(3,24)])
    liver_name = StringField('Liver',validators=[Required()])
    sumbit = SubmitField('提交')

    def validate_liver_name(self,field):
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError('用户不存在')

    def create_live(self):
        live = Live()
        self.populate_obj(live)
        live.liver_id= User.query.filter_by(username=self.liver_name.data).first().id
        db.session.add(live)
        db.session.commit()
        return live
class MessageForm(FlaskForm):
    text = TextAreaField('', validators=[Required()])
    submit = SubmitField('发送')