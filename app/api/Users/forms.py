from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ...models import Users

class LoginForm(Form):
    email = StringField('电子邮件', validators=[Required(), Length(1,64), Email('无效的电子邮件地址')])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegistrationForm(Form):
    email = StringField('电子邮件', validators=[Required(), Length(1, 64),
                                             Email('无效的电子邮件地址')])
    username = StringField('用户名', validators=[
        Required(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               '用户名必须是字母，数字，符号或下划线的组合')])
    password = PasswordField('密码', validators=[
        Required(), EqualTo('password2', message='密码必须一致')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件地址已存在')

    def validate_username(self, field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

class EditinfoForm(Form):
    nickname = StringField('昵称', validators=[Required()])
    about_me = TextAreaField('个人签名')
    submit = SubmitField('提交')

