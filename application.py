from flask import request, abort
from flask import Flask
from flask.ext.redis import FlaskRedis

from lib import RedisLinkSet, RedisLinkHash
from logic import process


storage = FlaskRedis()
app = Flask(__name__)
storage.init_app(app)

secure_domains = RedisLinkSet(storage, 'secure_domains')
already_uploaded_links = RedisLinkHash(storage, 'already_uploaded_links')


@app.route('/', methods=['POST'])
def index():
    payload = request.get_json()
    if payload is None:
        abort(404)
    raw_link = payload.get('link')
    if raw_link is None:
        abort(404)
    result = process(raw_link)
    if result is None:
        abort(404)

    return result


if __name__ == '__main__':
    app.run()
