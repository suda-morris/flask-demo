# encoding: utf-8
from flask import Flask, render_template, request, redirect, url_for, session, g
from sqlalchemy import or_

import config
from decorators import login_required
from exts import db, mqtt
from models import User, Question, Answer

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mqtt.init_app(app)

mqtt.subscribe('home/mytopic')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(data)


@app.route("/")
def index():
    questions = Question.query.order_by(db.desc(Question.create_time)).all()
    return render_template("index.html", questions=questions)


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        telephone = request.form.get("telephone")
        password = request.form.get("password")
        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            session.permanent = True
            return redirect(url_for("index"))
        else:
            return u"手机号或者密码错误，请检查后再次登录"


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
        newquestion = Question(title=title, content=content)
        newquestion.author = g.user
        db.session.add(newquestion)
        db.session.commit()
        return redirect(url_for("index"))


@app.route("/detail/<question_id>/")
def detail(question_id):
    ques = Question.query.filter(Question.id == question_id).first()
    return render_template("detail.html", question=ques)


@app.route("/add_answer/", methods=["POST"])
@login_required
def add_answer():
    comment = request.form.get("comment")
    question_id = request.form.get("question_id")
    answer = Answer(content=comment)
    answer.author = g.user
    ques = Question.query.filter(Question.id == question_id).first()
    answer.question = ques
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for("detail", question_id=question_id))


@app.route("/search/")
def search():
    q = request.args.get("q")
    condition = or_(Question.content.contains(q), Question.title.contains(q))
    questions = Question.query.filter(condition).order_by(db.desc(Question.create_time))
    return render_template("index.html", questions=questions)


@app.route("/monitor/")
@login_required
def monitor():
    return render_template("monitor.html")


@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


@app.context_processor
def my_context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


@app.errorhandler(404)
def page_not_found(error):
    return u'您访问的页面不存在', 404


if __name__ == "__main__":
    app.run(host="0.0.0.0")
