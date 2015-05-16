from flask import Flask, request, abort
from lib import Link

app = Flask(__name__)


def get_from_registry(netloc):
    raise NotImplementedError


def has_secure_domain(link):
    raise NotImplementedError


def upload(link):
    raise NotImplementedError


@app.route('/', methods=['POST'])
def index():
    # get link
    payload = request.get_json()
    if payload is None:
        abort(404)
    raw_link = payload.get('link')
    if raw_link is None:
        abort(404)

    link = Link(raw_link)

    if link.is_secure or link in secure_domains:
        return link.secure

if __name__ == '__main__':
    app.run()
