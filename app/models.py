from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from markdown import markdown
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db
from . import login_manager
import bleach

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    nickname = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    role = db.Column(db.Integer)
    confirmed = db.Column(db.Boolean, default=False)
    isdeleted = db.Column(db.Boolean, default=False)
    follow_num = db.Column(db.Integer, default=0)

    @property
    def password(self):
        raise AttributeError('密码不是一个可读属性')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            print('解码错误')
            return False
        if data.get('confirm') != self.id:
            print('用户id错误')
            return False
        self.confirmed = True
        db.session.add(self)
        print('激活成功')
        return True

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def __repr__(self):
        return '<User %r>' % self.username

class Boards(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    boardname = db.Column(db.String(64), unique=True, index=True)

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer)
    title = db.Column(db.String(64))
    content = db.Column(db.Text)
    content_html = db.Column(db.Text)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    follow_num = db.Column(db.Integer)
    good_num = db.Column(db.Integer)
    bad_num = db.Column(db.Integer)
    positive = db.Column(db.Integer)

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        target.content_html = markdown(value, output_format='html')


db.event.listen(Posts.content, 'set', Posts.on_changed_content)

class Follows(db.Model):
    __tablename__ = 'follows'
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer)
    content = db.Column(db.Text)

class Followers(db.Model):
    __tablename__ = 'followers'
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer)
    befollower_id = db.Column(db.Integer)

class Collections(db.Model):
    __tablename__ = "collection"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)

class Zans(db.Model):
    __tablename__ = "zan"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)