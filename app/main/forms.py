from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo
from flask_babel import _, lazy_gettext as _l
from app.models import User



class EmptyForm(FlaskForm):

    submit = SubmitField('Submit')



class PostForm(FlaskForm):

    post_title = StringField(_l('Post Title'), validators=[DataRequired()])
    post_section = StringField(_l('Post Section'), validators=[DataRequired()])
    description = StringField(_l('Post Description'), validators=[DataRequired()])
    post = TextAreaField(_l('Say Something'), validators=[DataRequired()])
    title_image = StringField(_l('Title Image'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))



class CommentsForm(FlaskForm):

    comment = TextAreaField(_l('Write your comment'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class SearchForm(FlaskForm):

    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)



class MessageForm(FlaskForm):

    '''This is form to send private message'''

    title= StringField(_l('Message Title'), validators = [DataRequired(),Length(min=0, max=140)])
    message = TextAreaField(_l('Message'), validators = [DataRequired(), Length(min=0, max=340)])
    submit = SubmitField(_l('Submit'))




class ChangeUserNameForm(FlaskForm):

    '''This is form to change user name in the edit_profile'''

    username = StringField(_l('Username'),validators=[DataRequired()])
    submit = SubmitField(_l('Change'))
        
    def __init__(self, original_username, *args, **kwargs):
        super(ChangeUserNameForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))
    


class ChangePasswordForm(FlaskForm):

    '''This is form to change password name in the edit_profile'''
    
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField(_l('Change'))
    
class ChangeStatusForm(FlaskForm):

    '''This is form to change password name in the edit_profile'''

    status = StringField(_l('Status'),validators=[DataRequired()])
    submit = SubmitField(_l('Change'))
        