from flask import render_template, redirect, request, url_for, flash, Request
from flask_login import login_user, logout_user, login_required, current_user
from . import post
from ...models import Collections, Zans, Posts, Users, Follows, Followers
from ... import db
from .forms import FollowsForm
import re

@post.route('/trip')
@login_required
def trip():
    page = request.args.get('page', 1, type=int)
    #pagination = Posts.query.filter_by(board_id=1).order_by(Posts.created_at.desc()).paginate(page, per_page=4, error_out=False)
    pagination = db.session.query(Posts, Users).join(Users, Posts.author_id == Users.id).filter(Posts.board_id==1).order_by(
        Posts.created_at.desc()).paginate(page, per_page=4, error_out=False)
    posts = pagination.items
    return render_template('trip.html', posts=posts, pagination=pagination)

@post.route('/food')
@login_required
def food():
    page = request.args.get('page', 1, type=int)
    #pagination = Posts.query.filter_by(board_id=2).order_by(Posts.created_at.desc()).paginate(page, per_page=4, error_out=False)
    pagination = db.session.query(Posts, Users).join(Users, Posts.author_id == Users.id).filter(Posts.board_id==2).order_by(
        Posts.created_at.desc()).paginate(page, per_page=4, error_out=False)
    posts = pagination.items
    return render_template('food.html', posts=posts, pagination=pagination)

@post.route('/news')
@login_required
def news():
    page = request.args.get('page', 1, type=int)
    #pagination = Posts.query.filter_by(board_id=3).order_by(Posts.created_at.desc()).paginate(page, per_page=4, error_out=False)
    pagination = db.session.query(Posts, Users).join(Users, Posts.author_id == Users.id).filter(Posts.board_id==3).order_by(
        Posts.created_at.desc()).paginate(page, per_page=4, error_out=False)
    posts = pagination.items
    return render_template('news.html', posts=posts, pagination=pagination)

@post.route('/things')
@login_required
def things():
    page = request.args.get('page', 1, type=int)
    #pagination = Posts.query.filter_by(board_id=4).order_by(Posts.created_at.desc()).paginate(page, per_page=4, error_out=False)
    pagination = db.session.query(Posts, Users).join(Users, Posts.author_id == Users.id).filter(Posts.board_id==4).order_by(
        Posts.created_at.desc()).paginate(page, per_page=4, error_out=False)
    posts = pagination.items
    return render_template('things.html', posts=posts, pagination=pagination)

@post.route('/search')
@login_required
def search():
    s = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    #pagination = Posts.query.filter(Posts.title.like('%'+s+'%')).paginate(page, per_page=4, error_out=False)
    pagination = db.session.query(Posts, Users).join(Users, Posts.author_id == Users.id).filter(Posts.title.like('%' + s + '%')).order_by(
        Posts.created_at.desc()).paginate(page, per_page=4, error_out=False)
    posts = pagination.items
    return render_template('search.html', posts=posts, pagination=pagination)


@post.route('/<int:id>', methods=['GET', 'POST'])
def postpage(id):
    form = FollowsForm()
    #print('1')
    page = request.args.get('page', 1, type=int)
    pattern = re.compile(r'\d+')
    result = re.search(pattern, request.path).group()
    if form.validate_on_submit():
        #print('2')
        follow = Follows(
            content_id = int(result),
            author_id = current_user.id,
            content = form.follow.data )
        db.session.add(follow)
        db.session.commit()
        #print('评论成功')
        flash("评论成功")
        return redirect(url_for('post.postpage', id=int(result)))
    #post = Posts.query.get_or_404(id)
    post = db.session.query(Posts, Users).join(Users, Posts.author_id == Users.id).filter(Posts.id==id)
    pagination = db.session.query(Follows, Users).join(
        Users, Follows.author_id == Users.id).filter(Follows.content_id == id).paginate(page, per_page=4, error_out=False)
    follows = pagination.items
    return render_template('postpage.html',posts=post, form=form, pagination=pagination, follows=follows, page=int(result))

@post.route('/like/<int:page>')
def like(page):
    post = Posts.query.get_or_404(page)
    zan = Zans.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if zan is None:
        zan = Zans(user_id=current_user.id, post_id=post.id)
        #print(zan)
        db.session.add(zan)
        post.good_num += 1
        db.session.commit()
        flash('操作成功')
    else:
        flash('您已经操作过了')
    return redirect(url_for('post.postpage', id=page)) 

@post.route('/dislike/<int:page>')
def dislike(page):
    post = Posts.query.get_or_404(page)
    zan = Zans.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if zan is None:
        zan = Zans(user_id=current_user.id, post_id=post.id)
        #print(zan)
        db.session.add(zan)
        post.bad_num += 1
        db.session.commit()
        flash('操作成功')
    else:
        flash('您已经操作过了')
    return redirect(url_for('post.postpage', id=page))

@post.route('/collect/<int:page>')
def collect(page):
    post = Posts.query.get_or_404(page)
    c = Collections.query.filter_by(author_id=current_user.id, post_id=post.id).first()
    if c is None:
        c = Collections(author_id=current_user.id, post_id=post.id)
        db.session.add(c)
        post.follow_num += 1
        db.session.commit()
        flash('收藏《'+post.title+'》成功')
    else:
        db.session.delete(c)
        post.follow_num -= 1
        db.session.commit()
        flash('您已经取消了对《' + post.title + '》的收藏')
    return redirect(url_for('post.postpage', id=page))
