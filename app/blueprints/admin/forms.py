from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField, SelectField, IntegerField, HiddenField
from wtforms.validators import InputRequired, Email, ValidationError, Length, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_ckeditor import CKEditorField


def no_spaces(form, field):
    if ' ' in field.data:
        raise ValidationError('No spaces allowed')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), no_spaces], render_kw={'placeholder': 'Username'})
    password = PasswordField('Password', validators=[InputRequired()], render_kw={'placeholder': 'Password'})
    submit = SubmitField('Login')


class ProductLinkForm(FlaskForm):
    prod_name = StringField('Product Name', validators=[InputRequired()], render_kw={'placeholder': 'Name'})
    prod_url = StringField('Product Url', validators=[InputRequired()], render_kw={'placeholder': 'Url'})
    # prod_cat = SelectField('Category', validators=[InputRequired()])
    prod_descr = TextAreaField('Product Description', validators=[InputRequired()], render_kw={'placeholder': 'Description'})
    prod_brand = StringField('Seller Brand', render_kw={'placeholder': '(Optional)'})
    prod_source = StringField('Online Store Name', render_kw={'placeholder': 'ex: Amazon'})
    submit = SubmitField('Submit')


class ProjectForm(FlaskForm):
    id = HiddenField()
    title = StringField('Project Title', validators=[InputRequired()], render_kw={'placeholder': 'Title'})
    # category = SelectField('Category', validators=[InputRequired()])
    tags = HiddenField('Tags')
    photo = FileField('Photo', validators=[FileAllowed(['jpg', 'png', 'heic', 'heif'], 'Images only!')])
    blurb = CKEditorField('Blurb', validators=[InputRequired()], render_kw={'placeholder': 'Blurb'})
    steps = CKEditorField('Steps', validators=[InputRequired()], render_kw={'placeholder': 'Cooking Instructions'})
    form_submit_btn = SubmitField('Submit')


class BlogForm(FlaskForm):
    id = HiddenField('Blog ID')
    title = StringField('Blog Title', validators=[InputRequired()], render_kw={'placeholder': 'Title'})
    # category = SelectField('Category', validators=[InputRequired()])
    tags = HiddenField('Tags')
    photo = FileField('Photo', validators=[FileAllowed(['jpg', 'png', 'heic', 'heif'], 'Images only!')])
    blurb = CKEditorField('Blurb', validators=[InputRequired()], render_kw={'placeholder': 'Blurb'})
    form_submit_btn = SubmitField('Submit')


class UserInfoForm(FlaskForm):
    id = HiddenField()
    username = StringField('Username', validators=[InputRequired(), no_spaces], render_kw={'placeholder': 'Username'})
    logo_img = FileField('Logo Image', validators=[FileAllowed(['jpg', 'png', 'heic', 'heif'], 'Images only!')])
    email = EmailField('Email', validators=[InputRequired(), no_spaces], render_kw={'placeholder': 'Email'})
    security_question = StringField('Security Question', validators=[InputRequired()], render_kw={'placeholder': 'Security Question'})
    answer = StringField('Answer', validators=[InputRequired()], render_kw={'placeholder': 'Answer'})
    submit = SubmitField('Submit')


class UpdatePasswordForm(FlaskForm):
    old_pw = PasswordField('Old Password', validators=[InputRequired()], render_kw={'placeholder': 'Old Password'})
    new_pw = PasswordField('New Password', validators=[
        InputRequired(),
        Length(min=8, message='Password must be at least 8 characters long.'),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]+$',
           message="Password must contain at least one letter and one number, and only use standard characters.")
        ], render_kw={'placeholder': 'new Password'})
    rep_new_pw = PasswordField('Re-Enter New Password', validators=[
        InputRequired(),
        Length(min=8, message='Password must be at least 8 characters long.'),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]+$',
           message="Password must contain at least one letter and one number, and only use standard characters.")
        ], render_kw={'placeholder': 'Repeat New Password'})
    submit = SubmitField('Submit')





