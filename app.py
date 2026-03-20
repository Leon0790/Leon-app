from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

# ---------------- MODELS ---------------- #

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    text = db.Column(db.String(500))

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student = db.Column(db.String(100))
    subject = db.Column(db.String(50))
    marks = db.Column(db.Integer)

# ---------------- ROUTES ---------------- #

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        session["email"] = email
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        return redirect("/")
    return render_template("dashboard.html", user=session["email"])

# -------- CHAT -------- #

@app.route("/chat", methods=["GET","POST"])
def chat():
    if "email" not in session:
        return redirect("/")
        
    if request.method == "POST":
        msg = request.form["message"]
        db.session.add(Message(user=session["email"], text=msg))
        db.session.commit()

    messages = Message.query.all()
    return render_template("chat.html", messages=messages, user=session["email"])

# -------- REPORT -------- #

@app.route("/report", methods=["GET","POST"])
def report():
    if request.method == "POST":
        text = request.form["report"]
        db.session.add(Report(text=text))
        db.session.commit()
    return render_template("report.html")

# -------- PERFORMANCE -------- #

@app.route("/performance", methods=["GET","POST"])
def performance():
    if request.method == "POST":
        student = request.form["student"]
        subject = request.form["subject"]
        marks = request.form["marks"]

        db.session.add(Score(student=student, subject=subject, marks=int(marks)))
        db.session.commit()

    scores = Score.query.all()
    return render_template("performance.html", scores=scores)

# -------- LOGOUT -------- #

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# -------- RUN -------- #

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
