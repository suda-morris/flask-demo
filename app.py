# encoding: utf-8
from flask import Flask, render_template, request, redirect, url_for, session

import config
from decorators import login_required
from exts import db
from models import User, Question

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        telephone = request.form.get("telephone")
        password = request.form.get("password")
        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
            session["user_id"] = user.id
            session.permanent = True
            return redirect(url_for("index"))
        else:
            return u"该用户不存在!"


@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        telephone = request.form.get("telephone")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u"该手机号码已经被注册，请更换手机号码！"
        else:
            if password1 == password2:
                user = User(telephone=telephone, password=password1, username=username)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("login"))
            else:
                return u"两次密码不相同，请核对后再填写！"


@app.route("/question/", methods=["GET", "POST"])
@login_required
def question():
    if request.method == "GET":
        return render_template("question.html")
    else:
        title = request.form.get("title")
        content = request.form.get("content")
        user_id = session.get("user_id")
        user = User.query.filter(User.id == user_id).first()
        newquestion = Question(title=title, content=content)
        newquestion.author = user
        db.session.add(newquestion)
        db.session.commit()
        return redirect(url_for("index"))


@app.route("/monitor/")
@login_required
def monitor():
    return render_template("monitor.html")


@app.context_processor
def my_context_processor():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {"user": user}
    return {}


@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404


if __name__ == "__main__":
    app.run()
