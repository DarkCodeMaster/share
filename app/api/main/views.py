from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import main
from ...models import Posts
from ...models import Users
from ... import db
from .forms import PostForm


@main.route('/')
def welcome():
    return render_template('welcome.html')

@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    #pagination = Posts.query.order_by(Posts.created_at.desc()).paginate(page, per_page=4, error_out=False)
    pagination = db.session.query(Posts, Users).join(Users, Posts.author_id == Users.id).order_by(Posts.created_at.desc()).paginate(page, per_page=4, error_out=False)
    posts = pagination.items
    return render_template('app_index.html', posts=posts, pagination=pagination)

@main.route('/admin/userinfo')
def admin_userinfo():
    data = Users.query.all()
    for row in data:
        print(row.email)
    return render_template('admin_userinfo.html', data=data)

@main.route('/admin/postinfo')
def admin_postinfo():
    data = Posts.query.all()
    return render_template('admin_postinfo.html', data=data)

@main.route('/admin/data')
def admin_data():
    values = []
    for x in range(1, 5):
        values.append(Posts.query.filter_by(board_id=x).count())
    user_values = []
    user_values.append(Users.query.filter_by(confirmed=True).count())
    user_values.append(Users.query.filter_by(confirmed=False).count())
    return render_template('admin_base.html', values=values, user_values=user_values)

@main.route('/admin/deleteuser/<int:id>')
def delete_user(id):
    u = Users.query.get(id)
    u.isdeleted = True
    db.session.commit()
    flash('用户信息删除成功')
    return redirect(url_for('main.admin_userinfo'))

@main.route('/admin/deletepost/<int:id>')
def delete_post(id):
    p = Posts.query.get(id)
    db.session.delete(p)
    db.session.commit()
    flash('文章信息删除成功')
    return redirect(url_for('main.admin_postinfo'))
