from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column


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
    text: Mapped[str] = mapped_column(unique=True)
    topicId: Mapped[str]

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
    print(comments)
    for comment in comments:
        print(comment)
    return render_template("topic.html", topic=topic)


app.run(debug=True)