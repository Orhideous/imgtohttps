from collections.abc import Container
from urllib.parse import ParseResult, urlparse


class EmptyUrlError(Exception):
    pass


class UploadError(Exception):
    pass


class RedisContainer:
    __storage = None
    name = None

    def __init__(self, storage, name):
        self.__storage = storage
        self.name = name


class RedisLinkSet(RedisContainer, Container):

    def __contains__(self, link):
        return self.__storage.sismember(self.name, link.url)


class RedisLinkHash(RedisContainer, Container):

    def __contains__(self, link):
        return self.__storage.hexists(self.name, link.url)

    def __iadd__(self, other):
        link, uploaded = other
        self.__storage.hset(self.name, link.url, uploaded.url)

    def __getitem__(self, link):
        if not isinstance(link, Link):
            raise TypeError

        result = self.__storage.hget(self.name, link.url)
        if result is None:
            raise KeyError

        return result


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
        if self.is_secure:
            return self.url
        return ParseResult(self.secure_scheme, *self.__data[1:]).geturl()

    @property
    def url(self):
        return self.__data.get_url()
