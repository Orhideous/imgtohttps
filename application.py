from os import environ
from flask import request, abort
from flask import Flask
from flask.ext.redis import FlaskRedis
from imgurpython import ImgurClient

from lib import LinkSet, LinksMapping, LinkRegistry
from logic import process


app = Flask(__name__)
app.config.from_object(environ.get('APP_SETTINGS', 'config.Development'))

storage = FlaskRedis()
storage.init_app(app)

secure_domains = LinkSet(storage, 'secure_domains')
already_uploaded_links = LinksMapping(storage, 'already_uploaded_links')
image_registry = LinkRegistry(storage, 'image_')
imgur_client = ImgurClient(app.config['IMGUR_CLIENT_ID'], app.config['IMGUR_CLIENT_SECRET'])


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
