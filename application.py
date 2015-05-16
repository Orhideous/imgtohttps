from flask import request, abort
from flask import Flask
from flask.ext.redis import FlaskRedis

from logic import process


redis_store = FlaskRedis()

app = Flask(__name__)
redis_store.init_app(app)


@app.route('/', methods=['POST'])
def index():
    payload = request.get_json()
    if payload is None:
        abort(404)
    raw_link = payload.get('link')
    if raw_link is None:
        abort(404)

    return process(raw_link)


if __name__ == '__main__':
    app.run()
