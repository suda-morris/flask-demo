# encoding: utf-8
from flask import Flask, render_template, request, redirect, url_for, session

import config
from exts import db
from models import User

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


@app.route("/monitor/")
def monitor():
    return render_template("monitor.html")


if __name__ == "__main__":
    app.run()
