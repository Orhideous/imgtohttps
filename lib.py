from urllib.parse import ParseResult, urlparse


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
