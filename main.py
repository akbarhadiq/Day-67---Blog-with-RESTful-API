from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor, CKEditorField
from forms import CreatePostForm
from datetime import datetime
from clean_strip_html import strip_invalid_html
from load_dotenv import load_dotenv
import os


load_dotenv("secret.env")

# were gonna use our db with our own api now
## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


@app.route('/home')
@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    return render_template("post.html",post=requested_post)
    


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/add", methods=["POST","GET"])
def add():
    form=CreatePostForm()

    if form.validate_on_submit():
        # look up the datetime using python datetime function
        title = form.title.data
        subtitle = form.subtitle.data
        author = form.author.data
        date = datetime.today().strftime("%B %d, %Y")
        img_url = form.img_url.data
        # body = user article post
        body = strip_invalid_html(form.body.data) 

        new_data = BlogPost(
            title=title,
            subtitle=subtitle,
            author=author,
            img_url=img_url,
            body=body,
            date=date
        )

        db.session.add(new_data)
        db.session.commit()

        return redirect(url_for('home'))


    return render_template("make-post.html", form=form, is_edit=False)

@app.route("/edit/<int:post_id>", methods=["GET","POST"])
def edit_post(post_id):

    post = BlogPost.query.get(post_id)
    date = post.date
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )

    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        post.date = date
        db.session.commit()
        return redirect(url_for('show_post', post_id=post.id))  

    return render_template("make-post.html", form=edit_form, post=post, is_edit=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)