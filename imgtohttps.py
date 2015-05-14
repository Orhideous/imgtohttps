from flask import Flask, request, abort
from urllib.parse import urlparse

app = Flask(__name__)


def get_from_registry(link):
    raise NotImplementedError


class Link(object):
    raise NotImplementedError


def has_secure_domain(link):
    raise NotImplementedError


def upload(parsed_link):
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

    parsed_link = Link(raw_link)

    if parsed_link.is_secure:
        return raw_link
    else:
        if has_secure_domain(parsed_link):
            return parsed_link.secure
        else:
            return upload(parsed_link)


if __name__ == '__main__':
    app.run()
