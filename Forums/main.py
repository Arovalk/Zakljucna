from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)

class Topic(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    topicId: Mapped[str]



class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


with app.app_context():
    db.create_all()

@app.route("/",methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Dodamo razpravo
        topic = Topic(
            title=request.form["title"],
            description=request.form["description"],
        )
        db.session.add(topic)
        db.session.commit()

    topics = db.session.execute(db.select(Topic)).scalars()
#    for topic in topics:
#        print(topic.title, topic.description, topic.id)
    
    return render_template("index.html", topics=topics)

@app.route("/topic/<int:id>",methods=["GET", "POST"])
def topic(id):
    if request.method == "POST":
        # Dodamo kommentar na razpravo
        comment = Comment(
            text=request.form["comment"],
            topicId=id
        )
        db.session.add(comment)
        db.session.commit()


    # prikaži razpravo
    topic = db.get_or_404(Topic, id)
    comments = Comment.query.filter_by(topicId=id).all()
#    print(comments)
#    for comment in comments:
#        print(comment)
    return render_template("topic.html", topic=topic, comments=comments)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")  
        password = request.form.get("password")
        print(username, password)       
        user = User.query.filter_by(username=username).first()
        
        
        
        if user and user.check_password(password):
            session["user_id"] = user.id
            return redirect(url_for("home"))
        else:
            return render_template("login.html")
    
    return render_template("login.html")      




app.run(debug=True)