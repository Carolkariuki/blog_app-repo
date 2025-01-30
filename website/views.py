
from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required,current_user,logout_user
from .models import User,Post,Comment,Subscriber
from . import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from .forms import UpdateProfileForm,AddPostForm,CommentForm
import functools

views=Blueprint('views',__name__)

def role_required(*roles):
    def decorator(function):
      @functools.wraps(function)
      def wrapper(*args,**kwargs):
          if current_user.role not in roles:
              return 'access denied'
          return function(*args,**kwargs)
      return wrapper
    return decorator
          




@views.route('/',methods=['GET'])
def home():
    user=User.query.get(3)
    print(user.username)
    if user:
        
        posts=user.posts
       
        for post in posts:
           print(post.heading)
    post_count=Post.query.filter_by(user_id=user.id).count()
    print(post_count)
   
    return render_template('home.html',user=user,posts=posts)



@views.route('/all_posts',methods=['GET'])
def all_posts():
    form=CommentForm()
    posts = Post.query.order_by(desc(Post.date_posted)).all()
    return render_template('all_posts.html',posts=posts,form=form)

@views.route('/feedback_comment/<int:post_id>', methods=['POST'])
@login_required
def feedback_comment(post_id):
    form=CommentForm()
    if form.validate_on_submit():
        feedback = form.feedback.data
        new_comment = Comment(feedback=feedback, username=current_user.username, post_id=post_id,user_id=current_user.id)
        new_comment.save()
        post=Post.query.get(post_id)
        post.comment_count +=1
        post.commit()
        flash('Comment added successfully!', category='success')
        return redirect(url_for('views.all_posts'))
    print(form)
    return redirect(url_for('views.all_posts'))
    

@views.route('/delete_comment/<int:comment_id>', methods=['POST','DELETE'])
@login_required
def delete_comment(comment_id):
    comment=Comment.query.get(comment_id)
    post=comment.post_comments
    comment.delete()
    if post.comment_count > 0:
        post.comment_count -= 1
        post.commit()
   
    flash('Comment deleted successfully!', category='success')
    return redirect(url_for('views.all_posts'))

@views.route('/like_post/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post=Post.query.get(post_id)
    if post:
       post.likes += 1  
       post.commit()
       flash('You liked the post!', category='success')
    return redirect(url_for('views.all_posts'))

@views.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('Writer not found!', 'error')
        return redirect(url_for('views.home'))
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('profile.html', user=user, posts=posts)

@views.route('/subscribe/<int:user_id>', methods=['POST'])
def subscribe(user_id):
    if request.method=='POST':
        email=request.form['email']
        new_subscriber=Subscriber(email=email,user_id=user_id)
        new_subscriber.save()
        flash('subscribed',category='success')
    return redirect(url_for('views.profile',user_id=user_id))

@views.route('/update_profile',methods=['GET','POST'])
@login_required
def update_profile():
    form=UpdateProfileForm()
    if form.validate_on_submit():
        username=form.username.data
        fullname=form.fullname.data
        about=form.about.data

        current_user.username=username
        current_user.fullname=fullname
        current_user.about=about
        current_user.commit()
        flash('user updated',category='success')
        return render_template('update_profile.html',form=form)
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.fullname.data = current_user.fullname
        form.about.data = current_user.about
    return render_template('update_profile.html',form=form)


@views.route('/add_posts',methods=['GET','POST'])
@login_required
@role_required('writer')
def add_posts():
    form=AddPostForm()
    if form.validate_on_submit():
        heading=form.heading.data
        content=form.content.data
        new_post=Post(heading=heading,content=content,user_id=current_user.id)
        new_post.save()
        
        flash('post added',category='success')
        return render_template('add_posts.html',form=form)
    return render_template('add_posts.html',form=form)
    
@views.route('/update_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
@role_required('writer')
def update_post(post_id):
    post = Post.query.get(post_id)
    form=AddPostForm()
    if form.validate_on_submit():
        post.heading = form.heading.data
        post.content = form.content.data
        post.commit()
        flash('Post has been updated!',category= 'success')
        return redirect(url_for('views.all_posts'))
    elif request.method == 'GET':  # On GET request, populate the form with the current post data
        form.heading.data = post.heading
        form.content.data = post.content
    return render_template('update_post.html', post=post,form=form)


@views.route('/delete_post/<int:post_id>',methods=['POST','DELETE'])
@login_required
@role_required('writer')
def delete_post(post_id):
    post = Post.query.get(post_id)
    print(f"Attempting to delete post with ID: {post_id}")
    print(f"Request method: {request.method}") 
    if post and post.user_id == current_user.id: 
        post.delete()
        flash('Post deleted successfully.', category='success')
    else:
        flash('You are not authorized to delete this post.', category='error')
    return redirect(url_for('views.all_posts'))

@views.before_request
def handle_method_override():
    if request.method == 'POST' and '_method' in request.form:
        request.method = request.form['_method'].upper()
   
@views.route('/delete_profile',methods=['POST','DELETE'])
@login_required
def delete_profile():
    user=current_user 
    user.delete()
    flash('account deleted successfully.', category='success')
    logout_user()
    return redirect(url_for('auth.login'))


