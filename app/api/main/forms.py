from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, SubmitField, TextAreaField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ...models import Users

class PostForm(Form):
    board_id = SelectField('分类', choices=[
        ('1', '出行'),
        ('2', '美食'),
        ('3', '趣闻'),
        ('4','奇珍')], validators=[Required()])
    title = StringField('标题' ,validators=[Required(), Length(1, 64)])
    content = PageDownField('正文', validators=[Required()])
    submit = SubmitField('提交')