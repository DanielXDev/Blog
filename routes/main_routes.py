from flask import Blueprint, render_template, request, redirect, url_for
import smtplib, os
from datetime import datetime
from dotenv import load_dotenv
from flask_login import current_user

load_dotenv()

main_bp = Blueprint("main", __name__)

# Inject current year into all templates
@main_bp.app_context_processor
def inject_now():
    return {
        "current_year": datetime.now().year,
        "current_user": current_user
    }


@main_bp.route("/")
def homepage():
    from models.blog import BlogPost
    from models.base import db

    page = request.args.get("page", 1, type=int)
    per_page = 6

    blogs_query = db.select(BlogPost)
    blogs = db.paginate(blogs_query, page=page, per_page=per_page)

    return render_template("index.html", blogs=blogs)


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        my_email = os.getenv("MY_EMAIL")
        password = os.getenv("PASSWORD")

        # Only send if all fields are filled
        if name and email and message:
            try:
                with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user=my_email, password=password)
                    connection.sendmail(
                        from_addr=email,
                        to_addrs=my_email,
                        msg=f"Subject: New Contact Message\n\n"
                            f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
                    )
            except Exception as e:
                print("Error sending email:", e)

    return render_template("contact.html")
