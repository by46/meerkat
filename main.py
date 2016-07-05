from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "hello, world!"


if __name__ == '__main__':
    from gevent.wsgi import WSGIServer

    WSGIServer(('', 8889), application=app).serve_forever()
