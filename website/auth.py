from flask import Blueprint,request,flash,render_template,redirect,url_for,current_app
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User,Post
from . import db
from flask_login import login_user,logout_user,login_required
from .forms import SignupForm,LoginForm,ForgotPasswordForm,ResetPasswordForm
from .utils import send_email
from werkzeug.utils import secure_filename
import os

DEFAULT_PROFILE_IMAGE = "default_profile_pic.png"
 
auth=Blueprint('auth',__name__)

@auth.route('/signup',methods=['GET','POST'])
def signup():
    form=SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        fullname = form.fullname.data
        email = form.email.data
        about = form.about.data
        role = form.role.data
        password1 = form.password1.data
        image_file = form.profile_image.data
        
        filename = 'default_profile_pic.png' 
        if image_file:
            print(f"Received file: {image_file.filename}")  # Debugging
            
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            
            print(f"Saving image to: {image_path}")  # Debugging
            
            # Ensure the images directory exists
            # os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)

            # Save the uploaded file
            image_file.save(image_path)

        user = User.query.get(email)
        if user:
            flash('user already exists', category='error')
            return redirect(url_for('auth.login'))
        subject='Welcome to the writing app'
        body=f'Welcome {username} enjoy your experience with this app'
        send_email(subject,[email],body)
        flash('account created',category='success')
        new_user=User(username=username,fullname=fullname,email=email,about=about,role=role,profile_image=filename,password=generate_password_hash(password1))
        new_user.save()
        login_user(new_user)
        return redirect(url_for('views.update_profile'))
    return render_template('signup.html',form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                login_user(user)
                flash('user logged in successful',category='success')
                return redirect(url_for('views.update_profile'))
            else:
                flash('incorrect information',category='error')
                return redirect(url_for('auth.login'))
        else:
           flash('user not signed up',category='error')
           return redirect(url_for('auth.signup'))
    return render_template('login.html',form=form)


@auth.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
     
        user = User.query.filter_by( email=form.email.data).first()
        if user:
            token=user.get_reset_token()
            subject='reset password link'
            body=f'''To reset your password, click the following link:
                {url_for('auth.reset_password', token=token, _external=True)}
                 If you did not request this, ignore this email.'''
            
            send_email(subject,[user.email],body)
        flash('If an account with that email exists, a reset link has been sent.',category='success')
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html', form=form)

@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token.', category='error')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        password= form.password.data
        new_password=generate_password_hash(password)
        user.password = new_password
        user.commit()
        flash('Your password has been updated! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('reset_password.html', form=form,token=token)

@auth.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
   


