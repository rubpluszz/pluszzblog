#-*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.models import User, Post
from app.translate import translate
from app.main import bp
from app.main.forms import PostForm

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
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
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Ноme'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url, user=user, form=form)