from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class FollowsForm(Form):
    follow = StringField('回复', validators=[Required()])
    sub = SubmitField('评论')