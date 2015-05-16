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
    if not request.data:
        abort(404)
    result = process(request.data)
    if result is None:
        abort(404)

    return result


@app.errorhandler(404)
def page_not_found():
    return '', 404

if __name__ == '__main__':
    app.run()
