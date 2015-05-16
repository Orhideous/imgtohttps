from collections.abc import Container
from urllib.parse import ParseResult, urlparse


class ImgError(Exception):
    """ Common exception for different nasty errors"""


class RedisContainer:
    """ Redis container"""

    __storage = None
    name = None

    def __init__(self, storage, name):
        """ Initialize container

        :type name: str
        :type storage: Redis or StrictRedis
        :param storage: Redis client
        :param name: Key name or prefix
        """

        self.__storage = storage
        self.name = name


class LinkSet(RedisContainer, Container):
    """ Wrapper class for handling some use cases for
    redis sets as usual python sets
    """

    def __contains__(self, link):
        """
        :type link: Link
        :rtype : bool
        """
        return self.__storage.sismember(self.name, link.netloc)

    def add(self, link):
        """
        :type link: Link
        """
        self.__storage.sadd(self.name, link.netloc)


class LinksMapping(RedisContainer, Container):
    """ Wrapper class for handling some use cases for
    redis hashes as usual python dicts
    """

    def __contains__(self, link):
        """
        :type link: Link
        """
        return self.__storage.hexists(self.name, link.url)

    def add(self, link, uploaded):
        """
        :type link: Link
        :type uploaded: Link
        """
        self.__storage.hset(self.name, link.url, uploaded.secure)

    def __getitem__(self, link):
        """
        :rtype : Link
        :type link: Link
        """
        if not isinstance(link, Link):
            raise TypeError

        result = self.__storage.hget(self.name, link.url)
        if result is None:
            raise KeyError

        return result


class LinkRegistry(RedisContainer):
    """Registry for metadata of each uploaded image"""

    def update(self, data):
        """
        :type data: dict[str, str|int|None]
        """
        self.__storage.hmset(self.name + data['link'], data)


class Link:
    secure_scheme = 'https'
    _data = None

    def __init__(self, raw_url):
        """ Construct Link instance with some useful methods

        :type raw_url: str
        """
        fragments = urlparse(raw_url)
        if not any(fragments):
            raise ImgError()
        else:
            self._data = fragments

    def __repr__(self):
        return repr(self._data)

    @property
    def is_secure(self):
        """
        :rtype : str
        """
        return self._data.scheme == self.secure_scheme

    @property
    def secure(self):
        """
        :rtype : str
        """
        if self.is_secure:
            return self.url
        return ParseResult(self.secure_scheme, *self._data[1:]).geturl()

    @property
    def url(self):
        """
        :rtype : str
        """
        return self._data.get_url()
