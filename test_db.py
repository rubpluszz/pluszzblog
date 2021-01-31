from datetime import datetime, timedelta
from app import db, app
from app import models as m
from app.models import User, Post
from config import Config

def add_user():
    return {user_one : m.User(username ='lida', email='lida@gmail.com'),
            user_thwo : m.User(username = 'vasja', email = 'vasja@fmail.ua'),
            user_three : m.User(username = 'dasza', email = 'dasza@fmail.com'),
             user_fore : m.User(username='fore', email='dasza@gmail.com'),}


def clear_database():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print ('Clear table %s' % table)
        db.session.execute(table.delete())
    db.session.commit()


def add_to_users_table(users):#users must be list [[username, email],[username, email]]
    for u in users:
        user = m.User(username=u[0], email=u[1])
        db.session.add(m.)
        print ("Add {} to user page".format(u))    
    db.session.commit()


def read_one_from_user_table(username):
    u = m.User.query.filter_by(username=username).first_or_404()
    return u.user_id

def read_all_from_uer_table()
    users = m.User.query.all()
    ret = []
    for u in users:
        ret.append(u.username)
    return ret


def add_status(user_id):
    u = m.User.query.filter_by(id=user_id).first_or_404()
    

def read_status():
    pass


def add_password(password, username, email):
    u = m.User(username=username, email=email)
    u.set_password(password) 


def read_password(username, password):
    u = m.User.query.filter_by(username=username).first_or_404() 
    return u.check_password(password)

def add_post(posts):#[[title],[body]]
    for p in posts:
        post = m.Post(title=p[0], body=[1])
        db.session.add(post)
    db.session.commit()


def read_one_post(post_id):
    return m.Post.query.get(post_id)


def read_registration_time():
    pass


def read_last_seen(): 
    pass 


def read_all_posts():
    posts = m.Post.query.all()
    return posts


def likes_post():
    pass


def dislike_post():
    pass

def read_likes_post():
    pass

def redact_post():
    pass


def change_vievs_post():
    pass


def read_old_version(parent_post_id, version):
    pass

def read_timestamp_post():


def add_comments():
    pass


def likes_comment():
    pass


def dislike_comments():
    pass


def read_timestamp_comments():
    pass


def read_comments_for_user_id():
    pass

def read_like_comments():
    pass

def add_private_message(body, sender_id, recepient_id,):
    pass

def read_private_message_for_id(message_id):
    pass

def read_private_messages_for_recipient_id(recepient_id):
    pass

def resd_private_messages_for_rsender_id(sendr_id):
    pass