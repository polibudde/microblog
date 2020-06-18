"""Routes for main pages."""
from flask import Blueprint, request, render_template, redirect
from .models import db, Post
from flask_login import login_required, current_user


# Blueprint Configuration
main_bp = Blueprint('main_bp',
                    __name__,
                    template_folder='templates',
                    static_folder='static')

@main_bp.route('/', methods=['GET'])
def home():
    """Homepage route."""
    return render_template('index.jinja2',
                           title='Home',
                           template='home-static main',
                           body="Home")

@main_bp.route('/posts', methods=['POST', 'GET'])
@login_required
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        if (post_content != "") and (post_title != "") :
            new_post = Post(title=post_title,
                            content=post_content,
                            user_id=current_user.get_id())
            try:
                db.session.add(new_post)
                db.session.commit()
                return redirect('/posts')
            except:
                return 'There was an issue adding your post'
        else:
            return redirect('/posts')
    else:
        posts = Post.query.order_by(Post.date_created).all()
        return render_template('posts.jinja2',
                               posts=posts,
                               title='Posts',
                               template='posts-static main',
                               body="Posts",
                               authuserid=current_user.id)

@main_bp.route('/delete/<int:id>')
def delete(id):
    post_to_delete = Post.query.get_or_404(id)
    if (post_to_delete.user_id) == (current_user.id):
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'There was a problem deleting that post'
    else:
        return 'Not your post'

@main_bp.route('/read/<int:id>', methods=['GET'])
@login_required
def read(id):
    post = Post.query.get_or_404(id)
    return render_template('read.jinja2',
                           post=post,
                           title='Read full post',
                           template='read-static main',
                           body="Read")

@main_bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get_or_404(id)
    if (post.user_id) == (current_user.id):
        if request.method == 'POST':
            post.content = request.form['content']
            try:
                db.session.commit()
                return redirect('/posts')
            except:
                return 'There was an issue updating your post'
        else:
            return render_template('update.jinja2',
                                   post=post,
                                   title='Update post',
                                   template='update-static main',
                                   body="Update")
    else:
        return 'Not your post'



@main_bp.route('/about', methods=['GET'])
@login_required
def about():
    """About page route."""
    return render_template('about.jinja2',
                           title='About',
                           template='about-static main',
                           body="About")