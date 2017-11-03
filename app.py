# encoding: utf-8
from flask import Flask
import config

app = Flask(__name__)
app.config.from_object(config)


@app.route("/")
def index():
    return "欢迎光临寒舍"


@app.route("/article/<article_id>/")
def article(article_id):
    return u"您的请求参数为:{param}".format(param=article_id)


if __name__ == "__main__":
    app.run()
