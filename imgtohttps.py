from flask import Flask, request, abort
from urllib.parse import urlparse, ParseResult

app = Flask(__name__)


def get_from_registry(link):
    raise NotImplementedError


class EmptyUrlError(Exception):
    pass


class Link:
    secure_scheme = 'https'
    __data = None

    def __init__(self, raw_url):
        fragments = urlparse(raw_url)
        if not any(fragments):
            raise EmptyUrlError()
        else:
            self.__data = fragments

    def __repr__(self):
        return repr(self.__data)

    @property
    def is_secure(self):
        return self.__data.scheme == self.secure_scheme

    @property
    def secure(self):
        return ParseResult(self.secure_scheme, *self.__data[1:]).geturl()


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

    if link.is_secure:
        return link.secure
    else:
        if has_secure_domain(link):
            return link.secure
        else:
            return upload(link)


if __name__ == '__main__':
    app.run()
