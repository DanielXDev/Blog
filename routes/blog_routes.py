from flask import Blueprint, render_template, request, redirect, url_for, abort
from models.blog import BlogPost, Comment
from models.base import db
from forms.blog_form import CreateBlogForm
from forms.comments import CommentForm
from datetime import datetime
from flask_login import login_required, current_user
from functools import wraps


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

blog_bp = Blueprint("blog", __name__, url_prefix="/blog")

@blog_bp.route("/create", methods=["GET", "POST"])
@admin_only
@login_required
def create_blog():
    form = CreateBlogForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            date=datetime.now().strftime("%B %d, %Y"),
            body=form.body.data,
            author=form.author.data,
            img_url=form.img_url.data,
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("main.homepage"))
    return render_template("create.html", form=form)

@blog_bp.route("/edit/<int:blog_id>", methods=["GET", "POST"])
@admin_only
@login_required
def edit_blog(blog_id):
    blog = BlogPost.query.get_or_404(blog_id)
    form = CreateBlogForm(obj=blog)
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.subtitle = form.subtitle.data
        blog.body = form.body.data
        blog.author = form.author.data
        blog.img_url = form.img_url.data
        db.session.commit()
        return redirect(url_for("blog.get_blog", title=blog.title))
    return render_template("edit.html", form=form, blog=blog)   

@blog_bp.route("/delete/<int:blog_id>")
@admin_only
@login_required
def delete_blog(blog_id):
    blog = BlogPost.query.get_or_404(blog_id)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for("main.homepage"))

@blog_bp.route("/blog/<title>", methods=["GET", "POST"])
@login_required
def get_blog(title):
    blog = BlogPost.query.filter_by(title=title).first_or_404()
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(
            name=current_user.name,
            date=datetime.now().strftime("%B %d, %Y"),
            text=form.text.data,
            post_id=blog.id
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("blog.get_blog", title=title))
    return render_template("blog.html", blog=blog, form=form, current_user=current_user)

@blog_bp.route("/delete_comment/<int:comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    blog_id = comment.post_id
    blog = BlogPost.query.get_or_404(blog_id)
    if current_user.id != 1 and current_user.name != comment.name:
        return abort(403)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("blog.get_blog", title=blog.title)) 