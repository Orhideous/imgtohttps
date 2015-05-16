from os import environ

from flask import request
from flask import Flask
from imgurpython import ImgurClient

from lib import ImgError
from logic import process
from storage import storage


app = Flask(__name__)
app.config.from_object(environ.get('APP_SETTINGS', 'config.Development'))
storage.init_app(app)
app.imgur_client = ImgurClient(app.config['IMGUR_CLIENT_ID'], app.config['IMGUR_CLIENT_SECRET'])


@app.route('/', methods=['POST'])
def index():
    try:
        return process(request.data.decode())
    except ImgError:
        return ''


if __name__ == '__main__':
    app.run()
