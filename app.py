# encoding: utf-8
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
db.create_all()


@app.route("/")
def index():
    books = [
        {"name": u"三国演义", "author": u"罗贯中", "price": 100},
        {"name": u"水浒传", "author": u"施耐庵", "price": 110},
        {"name": u"西游记", "author": u"吴承恩", "price": 120},
        {"name": u"红楼梦", "author": u"曹雪芹", "price": 130}
    ]
    return render_template("index.html", books=books)


@app.route("/article/<article_id>/")
def article(article_id):
    return u"您的请求文章ID为:{param}".format(param=article_id)


if __name__ == "__main__":
    app.run()
