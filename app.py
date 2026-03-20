
from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "secret"

messages = []

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        session["email"] = request.form["email"]
        return redirect("/chat")
    return render_template("login.html")

@app.route("/chat", methods=["GET","POST"])
def chat():
    if "email" not in session:
        return redirect("/")

    if request.method == "POST":
        msg = request.form["message"]
        messages.append({"user":session["email"],"text":msg})

    return render_template("chat.html",messages=messages,user=session["email"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)
