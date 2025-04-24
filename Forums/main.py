from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash



db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.secret_key = "Rambo"

db.init_app(app)

class Topic(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    author: Mapped[str]

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    topicId: Mapped[str]
    author: Mapped[str]




class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


with app.app_context():
    db.create_all()

@app.route("/",methods=["GET", "POST"])
def index():
    return render_template("index.html")




@app.route("/home",methods=["GET", "POST"])
def home():
    if "username" not in session:
        session['username'] = 'anonymous'
    
    if request.method == "POST":
        # Dodamo razpravo
        topic = Topic(
            title=request.form["title"],
            description=request.form["description"],
            author=session['username'],
        )
        if Topic.query.filter_by(title=topic.title).first():
            topics = db.session.execute(db.select(Topic)).scalars()
            return render_template("home.html", error="Topic already exists", topics=topics, username=session['username'])
        db.session.add(topic)
        db.session.commit()
    

    topics = db.session.execute(db.select(Topic)).scalars()
     # nastavi username na "anonymous" če ni prijavljen
    if "username" in session:
        return render_template("home.html", topics=topics, username=session['username'])

    else:
        return render_template("home.html", topics=topics, username='anonymous')
    
@app.route("/topic/<int:id>",methods=["GET", "POST"])
def topic(id):
    
    if "username" not in session:
        session['username'] = 'anonymous'
    
    
    if request.method == "POST":
        # Dodamo kommentar na razpravo
        comment = Comment(
            text=request.form["comment"],
            topicId=id,
            author=session['username']
        )
        db.session.add(comment)
        db.session.commit()


    # prikaži razpravo
    topic = db.get_or_404(Topic, id)
    comments = Comment.query.filter_by(topicId=id).all()
    print(comments)
    if "username" in session:
        return render_template("topic.html", topic=topic, comments=comments, username=session['username'])
    else:
        return render_template("topic.html", topic=topic, comments=comments, username="anonymous")

@app.route("/login", methods=["GET", "POST"])
def login():
    username = request.form.get("username")  
    password = request.form.get("password")
    print(username, password)       
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        session["user_id"] = user.id
        session["username"] = user.username 
        return redirect(url_for("home"))
    if user and not user.check_password(password):
        return render_template("login.html", error="Wrong password")
    else:
        return render_template("login.html")
  
@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form.get("username")  
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("login.html", error="Username already exists")
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('login'))



@app.route("/profile", methods=["GET"])
def profile():
    if "username" not in session or session["username"] == "anonymous":
        return redirect(url_for("login")) 

    user = User.query.filter_by(username=session["username"]).first()
    if not user:
        return redirect(url_for("login"))  

    topic_count = Topic.query.filter_by(author=session["username"]).count()
    comment_count = Comment.query.filter_by(author=session["username"]).count()

    return render_template("profile.html", user=user, topic_count=topic_count, comment_count=comment_count)


@app.route("/logout")
def logout():
    session.clear()  
    return redirect(url_for("login"))


@app.route("/about")
def about(): 
    if "username" not in session:
        session['username'] = 'anonymous'
    return render_template("about.html", username=session['username'])
app.run(debug=True)