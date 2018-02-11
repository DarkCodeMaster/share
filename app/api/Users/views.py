from __future__ import print_function, unicode_literals
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import user
from ...models import Users, Collections
from ...models import Posts, Followers
from ...email import send_email
from ... import db
from .forms import LoginForm, RegistrationForm, EditinfoForm
from ..main.forms import PostForm
import json
import requests

@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = Users.query.filter_by(email=form.email.data).first()
        if u is not None and u.verify_password(form.password.data):
            login_user(u, form.remember_me.data)
            return redirect(request.args.get(next) or url_for('main.index'))
        flash('用户名或密码错误')
    return render_template('user_login.html', form=form)

@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功登出')
    return redirect(url_for('main.index'))

@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        u = Users(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    role = 0)
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        send_email(u.email, '确认您的账户',
                   'confirm', u=u, token=token)
        flash('已发送确认邮件')
        return redirect(url_for('user.login'))
    return render_template('user_register.html', form=form)

@user.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('您激活了您的账户，感谢！')
    else:
        flash('确认链接无效或过期')
    return redirect(url_for('main.index'))


@user.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认您的账户',
               'confirm', u=current_user, token=token)
    flash('一封新的确认邮件已发送')
    return redirect(url_for('main.index'))
    
@user.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
            and request.endpoint[:5] != 'user.' \
            and request.endpoint != 'static':
            return redirect(url_for('user.unconfirmed'))


@user.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('unconfirmed.html')

@user.route('/info/<username>')
def info(username):
    u = Users.query.filter_by(username=username).first()
    if u is None:
        abort(404)
    fer = Followers.query.filter_by(
            follower_id=current_user.id, befollower_id=u.id).first()
    if fer is None:
        isFollowed = False
    else:
        isFollowed = True
    #collect = Collections.query.filter_by(author_id=current_user.id)
    collect = db.session.query(Collections, Posts).join(Posts, Collections.post_id==Posts.id).filter(Collections.author_id==current_user.id)
    #follow = Followers.query.filter_by(follower_id=current_user.id)
    follow = db.session.query(Followers, Users).join(Users, Followers.befollower_id==Users.id).filter(Followers.follower_id==current_user.id)
    return render_template('user_info.html', u=u, isFollowed=isFollowed, follow=follow, collect=collect)

@user.route('/info/edit', methods=['GET', 'POST'])
@login_required
def edit_info():
    form = EditinfoForm()
    if form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('你的资料更新了')
        return redirect(url_for('user.info', username=current_user.username))
    form.nickname.data = current_user.nickname
    form.about_me.data = current_user.about_me
    return render_template('edit_info.html', form=form) 

@user.route('/push', methods=['GET', 'POST'])
@login_required
def push():
    form = PostForm()
    if form.validate_on_submit():
        SENTIMENT_URL = 'http://api.bosonnlp.com/sentiment/analysis'
        headers = {'X-Token': 'Zq-KVR6G.21993.5oAc9MpLgq2m'}
        s = []
        s.append(form.content.data)
        data = json.dumps(s)
        resp = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))
        result = resp.json()
        print('积极概率：' + str(result[0][0] * 100) + '%')
        print('消极概率：' + str(result[0][1] * 100) + '%')
        p = int(result[0][0] * 100)
        post = Posts(board_id=int(form.board_id.data[0]),
                     title=form.title.data,
                     content=form.content.data,
                     author_id=current_user.id,
                     follow_num=0,
                     good_num=0,
                     bad_num=0,
                     positive=p)
        print(form.board_id.data)
        print(current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('user_push.html', form=form)

@user.route('/follow/<int:id>')
def follow(id):
    befer = Users.query.get_or_404(id) 
    fer = Followers.query.filter_by(follower_id=current_user.id, befollower_id=befer.id).first()
    if fer is None:
        fer = Followers(follower_id=current_user.id, befollower_id=befer.id)
        db.session.add(fer)
        befer.follow_num += 1
        db.session.commit()
        flash('您已经成功关注了“'+befer.username+'”')
    else:
        db.session.delete(fer)
        befer.follow_num -= 1
        db.session.commit()
        flash('您已经取消了对"' + befer.username+'的关注"')
    return redirect(url_for('user.info', username=befer.username))
