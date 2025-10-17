# import smtplib
# import datetime
# import os
# from dotenv import load_dotenv
# from flask import Flask, render_template, request, redirect, url_for
# # from flask_bootstrap import Bootstrap5
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from sqlalchemy import Integer, String, Text, select
# from flask_wtf import FlaskForm, CSRFProtect
# from wtforms import StringField, SubmitField, TextAreaField
# from wtforms.validators import DataRequired, URL
# from flask_ckeditor import CKEditor, CKEditorField

# load_dotenv()

# app = Flask(__name__)
# app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'


# # CREATE DATABASE
# class Base(DeclarativeBase):
#     pass

# db = SQLAlchemy(model_class=Base)
# db.init_app(app)
# csrf = CSRFProtect(app)
# ckeditor = CKEditor(app)

# # CONFIGURE TABLE
# class BlogPost(db.Model):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
#     subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
#     date: Mapped[str] = mapped_column(String(250), nullable=False)
#     body: Mapped[str] = mapped_column(Text, nullable=False)
#     author: Mapped[str] = mapped_column(String(250), nullable=False)
#     img_url: Mapped[str] = mapped_column(String(250), nullable=False)


# with app.app_context():
#     db.create_all()

# # CREATE FORM

# class CreateBlogForm(FlaskForm):
#     title = StringField("Blog Title", validators=[DataRequired()])
#     subtitle = StringField("Subtitle", validators=[DataRequired()])
#     date = StringField("Date", validators=[DataRequired()])
#     body = TextAreaField("Blog Content", validators=[DataRequired()])
#     author = StringField("Author", validators=[DataRequired()])
#     img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
#     submit = SubmitField("Submit Post")

# year = datetime.datetime.now().year

# @app.context_processor
# def inject_now():
#     return {"current_year": year}

# @app.route("/")
# def homepage():
#     page = request.args.get("page", 1, type=int)
#     per_page = 6

#     blogs_query = select(BlogPost)
#     blogs = db.paginate(blogs_query, page=page, per_page=per_page)

#     return render_template("index.html", blogs=blogs)

# @app.route("/create_blog", methods=["GET", "POST"])
# def create_blog():
#     form = CreateBlogForm()
#     if form.validate_on_submit():
#         new_post = BlogPost(
#             title=form.title.data,
#             subtitle=form.subtitle.data,
#             date=form.date.data,
#             body=form.body.data,
#             author=form.author.data,
#             img_url=form.img_url.data,
#         )
#         db.session.add(new_post)
#         db.session.commit()
#         return redirect(url_for("homepage"))
#     return render_template("create.html", form=form, year=year)

# @app.route("/blog")
# def get_blog():
#     blog_id = request.args.get('id')
#     blog = db.get_or_404(BlogPost, blog_id)
#     return render_template("blog.html", blog=blog, year=year)

# @app.route("/about")
# def about():
#     return render_template("about.html", year=year)

# @app.route("/contact", methods=["POST", "GET"])
# def contact():
#     #Check if user is sending a message
#     if "message" in request.form:
#         name = request.form.get("name")
#         email = request.form.get("email")
#         message = request.form.get("message")

#         my_email = os.getenv("MY_EMAIL")
#         password = os.getenv("PASSWORD")

#         with smtplib.SMTP(host="smtp.gmail.com") as connection:
#             connection.starttls()
#             connection.login(user=my_email, password=password)
#             connection.sendmail(
#                 from_addr=email,
#                 to_addrs=my_email,
#                 msg=f"Subject: Message!!!\n\n Name:{name} \n Email:{email} \n Message:{message}"
#             )
#     return render_template("contact.html", year=year)


# if __name__ == "__main__":
#     app.run(debug=True)
