from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)

class topic(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(unique=True)
    topicId: Mapped[str]



@app.route("/",methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Dodamo razpravo
        user = topic(
            title=request.form["title"],
            description=request.form["description"],
        )
        db.session.add(topic)
        db.session.commit()
    return render_template("index.html")

@app.route("/topic/<int:id>",methods=["GET", "POST"])
def topic(id):
    if request.method == "POST":
        # Dodamo kommentar na razpravo
        comment = Comment(
            text=request.form["text"],
            topicId=request.form["topicId"],
        )
        db.session.add(comment)
        db.session.commit()


        # prikaži razpravo
    return render_template("user/detail.html", user=user)


app.run(debug=True)