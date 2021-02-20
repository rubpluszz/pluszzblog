#-*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.models import User, Post, Comments
from app.translate import translate
from app.main import bp
from app.main.forms import PostForm, CommentsForm

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/blog', methods=['GET', 'POST'])
def blog():
    form = PostForm()
    user = current_user
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body = form.post.data, 
                    title = form.post_title.data,
                    description = form.description.data,
                    title_image = form.title_image.data,
                    language = language,
                    section = form.post_section.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    selected_posts = db.session.query(Post).filter(Post.selected_posts==1).all()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.blog', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.blog', page=posts.prev_num) \
        if posts.has_prev else None
    posts1=[]#Posts in first column
    posts2=[]#Posts in second column
    for post in posts.items:
        if post.id%2==1:
            posts1.append(post)
        else:
            posts2.append(post)
    return render_template('index.html', title='PluszzBlog',
                           posts1=posts1 ,posts2=posts2, selected_posts=selected_posts, next_url=next_url,
                           prev_url=prev_url, user=user, form=form)


@bp.route('/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):
    form = CommentsForm()
    user = current_user
    post = Post.query.filter_by(id=post_id).first()
    if form.validate_on_submit:
        comment = Comments(body=form.comment.data, user_id=user.id, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        form.comment.data=''#clear comment field
    page = request.args.get('page', 1, type=int)
    comments=Comments.query.filter_by(post_id=post.id).paginate(page, current_app.config['COMMENTS_PER_PAGE'], False)
    next_url = url_for('main.post',post_id=post_id, page=comments.next_num) if comments.has_next else None
    prev_url = url_for('main.post',post_id=post_id, page=comments.prev_num) if comments.has_prev else None
    locale = get_locale()
    return render_template('post.html', title=post.title, post=post, next_url=next_url, prev_url=prev_url, form=form, comments=comments.items, locale=locale)