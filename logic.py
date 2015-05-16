from lib import Link


def process(raw_link):
    link = Link(raw_link)

    if link.is_secure or link in secure_domains:
        return link.secure


def get_from_registry(netloc):
    raise NotImplementedError

