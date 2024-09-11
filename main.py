from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from form import Login, Register, CarBlog, EditBlogForm
import os
app = Flask("__name__")

class Base(DeclarativeBase):
    pass

app.config['SECRET_KEY'] = os.environ.get('Link')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)
ckeditor = CKEditor(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

# User database model
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100))

class Blog(db.Model):
    __tablename__ = "blogs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    car_name: Mapped[str] = mapped_column(String(100), nullable=False)
    car_company: Mapped[str] = mapped_column(String(100), nullable=False)
    engine: Mapped[str] = mapped_column(String(100), nullable=False)
    max_speed: Mapped[str] = mapped_column(String(100), nullable=False)
    Time: Mapped[str] = mapped_column(String(100), nullable=False)
    power: Mapped[str] = mapped_column(String(100), nullable=False)
    img_url: Mapped[str] = mapped_column(String(100), nullable=False)
    blog: Mapped[str] = mapped_column(Text, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    form = Login()
    if request.method == "POST" and form.validate_on_submit():
        password = request.form.get("password")
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar_one_or_none()
        if not user:
            flash("Email does not exist")
        elif not check_password_hash(user.password, password):
            flash("Password is wrong")
        else:
            login_user(user)
            return redirect(url_for("all_post"))
    return render_template("login.html", form=form)

@app.route("/register", methods=["POST", "GET"])
def register():
    form = Register()
    if request.method == "POST" and form.validate_on_submit():
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        user = db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()
        if user:
            flash("Email already exists")
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            new_user = User(
                name=name,
                email=email,
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("register.html", form=form)

@app.route('/make_blog', methods=['POST', 'GET'])
@login_required
def make_blog():
    form = CarBlog()
    if request.method == 'POST' and form.validate_on_submit():
        car = Blog(
            car_name=form.car_name.data,
            car_company=form.car_company.data,
            engine=form.engine.data,
            max_speed=form.max_speed.data,
            Time=form.Time.data,
            power=form.power.data,
            img_url=form.img_url.data,
            blog=form.blog.data
        )
        db.session.add(car)
        db.session.commit()
        return redirect(url_for('all_post'))
    return render_template("make_blog.html", form=form)

@app.route("/post", methods=["GET"])
@login_required
def all_post():
    data = db.session.execute(db.select(Blog)).scalars().all()
    return render_template("Blog.html", data=data)

@app.route("/post/read-blog/<int:id>",methods=["GET","POST"])
@login_required
def read(id):
    blog=db.get_or_404(Blog,id)
    return render_template("read-blog.html",blog=blog,current_user=current_user)


@app.route("/post/edit/<int:id>", methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Blog.query.get_or_404(id)  # Fetch the blog post from the database
    form = EditBlogForm(obj=post)  # Pre-fill the form with the current blog data

    if form.validate_on_submit():  # Check if the form is submitted and valid
        post.car_name = form.car_name.data
        post.car_company = form.car_company.data
        post.engine = form.engine.data
        post.max_speed = form.max_speed.data
        post.Time = form.Time.data
        post.power = form.power.data
        post.img_url = form.img_url.data
        post.blog = form.blog.data

        db.session.commit()  # Commit the changes to the database
        flash('Blog post has been updated successfully!', 'success')
        return redirect(url_for('all_post'))  # Redirect to the list of all posts

    return render_template("make_blog.html", form=form, is_edit=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
