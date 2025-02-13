from flask import Blueprint,request,flash,render_template,redirect,url_for
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User,Post
from . import db
from flask_login import login_user,logout_user,login_required
from .forms import SignupForm,LoginForm
from .utils import send_email
from werkzeug.utils import secure_filename
import os
 
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
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join('static/image', filename)
            image_file.save(image_path)
        else:
            filename = 'default_profile_pic.png'

        user = User.query.get(email)
        if user:
            flash('user already exists', category='error')
            return redirect(url_for('auth.login'))
        
        new_user=User(username=username,fullname=fullname,email=email,about=about,role=role,profile_image=filename,password=generate_password_hash(password1))
        new_user.save()
        subject='Welcome to the writing app'
        body=f'Welcome {username} enjoy your experience with this app'
        send_email(subject,[email],body)
        flash('account created',category='success')
        login_user(new_user)
        print(repr(new_user))
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

@auth.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
   


