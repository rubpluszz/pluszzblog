#-*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.models import User, Post, Comments, likes_table_comments, PrivateMessages
from app.translate import translate
from app.main import bp
from app.main.forms import PostForm, CommentsForm, EmptyForm, MessageForm, SearchForm, ChangeUserNameForm, ChangePasswordForm, ChangeStatusForm
from bbcode import render_html


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
        return redirect(url_for('main.blog'))
    selected_posts = db.session.query(Post).filter(Post.selected_posts==True).all()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.blog', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.blog', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='PluszzBlog',
                           posts=posts, selected_posts=selected_posts, next_url=next_url,
                           prev_url=prev_url, user=user, form=form)


@bp.route('/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):
    form = CommentsForm()
    user = current_user
    post = Post.query.filter_by(id=post_id).first_or_404()
    selected_posts = db.session.query(Post).filter(Post.selected_posts==True).all()
    if form.validate_on_submit() and form.comment.data!=None:
        comment = Comments(body=form.comment.data, user_id=user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        form.comment.data = ''#clear comment field
        return redirect(url_for('main.post', post_id=post_id))
    page = request.args.get('page', 1, type=int)
    comments = Comments.query.filter_by(post_id=post_id).order_by(Comments.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.post',post_id=post_id, page=comments.next_num) if comments.has_next else None
    prev_url = url_for('main.post',post_id=post_id, page=comments.prev_num) if comments.has_prev else None
    locale = get_locale()
    post.vievs_upper()
    db.session.commit()
    return render_template('post.html',render_html = render_html, User=User, Comments=Comments, likes_table_comments=likes_table_comments, 
                            title=post.title, post=post, next_url=next_url, prev_url=prev_url, form=form, db=db, 
                            comments=comments, locale=locale, user=user, selected_posts=selected_posts)

@bp.route('/liked_post/<int:post_id>')
@login_required
def like_post( post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    current_user.like_this_post(post)
    db.session.commit()
    return redirect(url_for('main.post', post_id=post_id))    


@bp.route('/dislike_comment/<int:post_id>')
@login_required
def dislike_post( post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    current_user.dislike_this_post(post)
    db.session.commit()
    return redirect(url_for('main.post', post_id=post_id)) 


@bp.route('/like_comment/<int:comment_id>/<int:post_id>')
@login_required
def like_comment(comment_id, post_id):
    comment = Comments.query.filter_by(id=comment_id).first_or_404()
    current_user.like_this_comments(comment)
    db.session.commit()
    return redirect(url_for('main.post', post_id=post_id))    


@bp.route('/dislike_comment/<int:comment_id>/<int:post_id>')
@login_required
def dislike_comment(comment_id, post_id):
    comment = Comments.query.filter_by(id=comment_id).first_or_404()
    current_user.dislike_this_comments(comment)
    db.session.commit()
    return redirect(url_for('main.post', post_id=post_id)) 
  

@bp.route("/about")
def about():
    selected_posts = db.session.query(Post).filter(Post.selected_posts==True).all()
    post_id = Post.query.filter_by(title='About').first_or_404().id
    return redirect(url_for('main.post', post_id=post_id)) 

@bp.route("/projects")
def projects():
    selected_posts = db.session.query(Post).filter(Post.selected_posts==True).all()
    return render_template('projects.html', selected_posts=selected_posts)

@bp.route("/section")
def section():
    selected_posts = db.session.query(Post).filter(Post.selected_posts==True).all()
    return render_template('section.html', selected_posts=selected_posts)


@bp.route("/cooperation", methods=['GET','POST'])
def cooperation():
    selected_posts = db.session.query(Post).filter(Post.selected_posts==True).all()
    recipient = User.query.filter_by(username="pluszz").first_or_404()
    form = MessageForm()
    user=current_user
    if form.validate_on_submit():
        msg = PrivateMessages(sender=current_user, recipient=recipient,
                      body=form.message.data, title="coperation---"+form.title.data)
        db.session.add(msg)
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('main.cooperation'))
    return render_template('coperation.html', user=user, form=form, selected_posts=selected_posts)


@bp.route('/user/<username>')
@bp.route('/user/<username>/<category>')
@login_required
def user(username, category="_favorite_posts"):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    page = request.args.get('page', 1, type=int)
    page_to_vievs = category+'.html'
    if category=="_favorite_posts":
        liked_posts = user.liked_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('main.blog', page=liked_posts.next_num) if liked_posts.has_next else None
        prev_url = url_for('main.blog', page=liked_posts.prev_num) if liked_posts.has_prev else None
    if category=='_recomendation':
        liked_posts = db.session.query(Post).filter(Post.selected_posts==1).all()
        next_url, prev_url = None, None 
    if category =='_read_later':
        liked_posts = user.to_read_later().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('main.blog', page=liked_posts.next_num) if liked_posts.has_next else None
        prev_url = url_for('main.blog', page=liked_posts.prev_num) if liked_posts.has_prev else None
    return render_template('user_page.html', page_to_vievs=page_to_vievs, Comments=Comments, user=user,
                           form=form ,liked_posts=liked_posts, prev_url=prev_url, next_url=next_url)




@bp.route("/messages")
@login_required
def messages():
    user = current_user
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.message_received.order_by(
        PrivateMessages.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.messages', page=messages.next_num) if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) if messages.has_prev else None
    return render_template('user_page.html',render_html=render_html, page_to_vievs='_messages.html', messages=messages.items, 
                            user=user, next_url=next_url, prev_url=prev_url, User=User)



@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):

    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = PrivateMessages(sender=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('main.user', username=recipient))
    return render_template('send_message.html', title=_('Send Message'),
                           form=form, recipient=recipient)



@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())



@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/delete_post/<post_id>')
@login_required
def delete_post(post_id):
    if current_user.username=='pluszz':
        post = Post.query.filter_by(id=post_id).first()
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('main.post', post_id=post_id))
    else:
        return redirect(url_for(' main.post', post_id=post_id))


@bp.route('/select_post/<post_id>')
@login_required
def select_post(post_id):
    if current_user.username=='pluszz':
        post = Post.query.filter_by(id=post_id).first()
        post.selected_posts = True
        db.session.commit()
        return redirect(url_for('main.post', post_id=post_id))
    else:  
        return redirect(url_for('main.post', post_id=post_id))


@bp.route('/unselect_post/<post_id>')
@login_required
def unselect_post(post_id):
    if current_user.username=='pluszz':
        post = Post.query.filter_by(id=post_id).first()
        post.selected_posts = False
        db.session.commit()
        return redirect(url_for('main.post', post_id=post_id))
    else:  
        return redirect(url_for('main.post', post_id=post_id))



@bp.route('/hidde_post/<post_id>')
@login_required
def hidde_post(post_id):
    if current_user.username=='pluszz':
        post = Post.query.filter_by(id=post_id).first()
        post.hidden_post = True
        db.session.commit()
        return redirect(url_for('main.post', post_id=post_id))
    else:  
        return redirect(url_for('main.post', post_id=post_id))


@bp.route('/unhidde_post/<post_id>')
@login_required
def unhidde_post(post_id):
    if current_user.username=='pluszz':
        post = Post.query.filter_by(id=post_id).first()
        post.hidden_post = False
        db.session.commit()
        return redirect(url_for('main.post', post_id=post_id))
    else:  
        return redirect(url_for('main.post', post_id=post_id))


@bp.route('/edit_post/<post_id>', methods=['GET','POST'])#This method not work????
@login_required
def edit_post(post_id):
    if current_user.username=='pluszz':
        post = Post.query.filter_by(id=post_id).first()
        form = PostForm()
        if form.validate_on_submit():
            db.session.query(Post).filter(Post.id==post.id).update({'body': form.post.data, 'title':form.post_title.data,
                         'description':form.description.data, 'title_image':form.title_image.data,
                         'section':form.post_section.data}, synchronize_session=False)
            db.session.commit()
            return redirect(url_for('main.post', post_id=post_id))
    return render_template('edit_post.html', user=current_user, form=form, post=post)


@bp.route('/user/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():

    user = current_user
    edit_username_form = ChangeUserNameForm(user.username)
    edit_password_form = ChangePasswordForm()
    edit_status_form = ChangeStatusForm()
    if edit_username_form.validate_on_submit():
        user.username = edit_username_form.username.data
        db.session.add(user)
        db.session.commit()
        edit_username_form.username.data=''
        flash(_('Your username has changed.'))
        return redirect(url_for('main.edit_profile'))
    if edit_password_form.validate_on_submit():
        user.set_password(edit_password_form.password.data)
        db.session.add(user)
        db.session.commit()
        edit_password_form.password.data=''
        edit_password_form.password2=''
        flash(_('Your password has changed.'))
        return redirect(url_for('main.edit_profile'))
    if edit_status_form.validate_on_submit():
        user.status = edit_status_form.status.data
        db.session.add(user)
        db.session.commit()
        edit_status_form.status.data=''
        flash(_('Your staus has changed.'))
        return redirect(url_for('main.edit_profile'))
    return render_template('user_page.html', page_to_vievs='_edit_profile.html', user=user, title=_('Edit Profile'), edit_username_form=edit_username_form, 
                           edit_password_form=edit_password_form, edit_status_form=edit_status_form)