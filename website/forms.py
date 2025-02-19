from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField,PasswordField,TextAreaField,SubmitField,EmailField,FileField
from wtforms.validators import DataRequired, Length,Email,EqualTo
from flask_wtf.file import FileAllowed


class SignupForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=10)])
    fullname=StringField('Fullname',validators=[DataRequired(),Length(min=5)])
    email=EmailField('Email',validators=[DataRequired(),Email(),Length(min=10)])
    about=TextAreaField('About',validators=[DataRequired(),Length(min=10,max=200)])
    role=StringField('Role',validators=[Length(min=4,max=20)])
    profile_image=FileField('Upload Profile image',validators=[FileAllowed(['jpg', 'png', 'jpeg'], message='Images only!')])
    password1=PasswordField('Password1',validators=[DataRequired(),Length(min=4)])
    password2=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password1',message='passwords must match')])
    submit=SubmitField('Signup')

class LoginForm(FlaskForm):
    email=EmailField('Email',validators=[DataRequired(),Email(),Length(min=10)]) 
    password=PasswordField('Password',validators=[DataRequired()])  
    submit=SubmitField('Login')

class ForgotPasswordForm(FlaskForm):
    email=EmailField('Email',validators=[DataRequired(),Email(),Length(min=10)]) 
    submit=SubmitField('Send Reset link')

class ResetPasswordForm(FlaskForm):
    password=PasswordField('New password',validators=[DataRequired(),Length(min=4)])
    confirm_password=PasswordField('Confirm password',validators=[EqualTo('password')])
    submit=SubmitField('Reset Password')

class UpdateProfileForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=10)])
    fullname=StringField('Fullname',validators=[DataRequired(),Length(min=5)])
    profile_image=FileField('Upload Profile image',validators=[FileAllowed(['jpg', 'png', 'jpeg'], message='Images only!')])
    about=TextAreaField('About',validators=[DataRequired(),Length(min=10,max=200)])
    submit=SubmitField('Update')

class AddPostForm(FlaskForm):
    heading=StringField('Heading',validators=[DataRequired(),Length(max=50)])
    content=TextAreaField('Content',validators=[DataRequired()])
    submit=SubmitField('Add Post')

class CommentForm(FlaskForm):
    feedback=StringField('Feedback',validators=[DataRequired(),Length(max=100)])
    submit=SubmitField('Comment')



   


