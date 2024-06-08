from flask import Blueprint, render_template

info = Blueprint('info', __name__)


@info.route("/about")
def about():
    return render_template("about.html")


@info.route("/contact")
def contact():
    return render_template("contact.html")
