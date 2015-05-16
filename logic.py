from imgurpython.helpers.error import ImgurClientError
import requests

from lib import Link, ImgError
from application import secure_domains, insecure_domains
from application import already_uploaded_links, imgur_client, image_registry


def has_secure_domain(link):
    """ Check if given link can be served over HTTPS

    :type link: Link
    :param link: Link to check
    :return: Existence of secure domain
    :rtype: bool
    """

    try:
        resp = requests.head(link.secure)
    except requests.exceptions.RequestException:
        return False

    if resp.status_code == 200:
        secure_domains.add(link)
        return True
    else:
        insecure_domains.add(link)
        return False


def upload(link):
    """ Upload image to Imgur

    :type link: Link
    :param link: Link instance
    :return: Link to uploaded image
    :rtype: Link
    :raise ImgError:
    """

    try:
        result = imgur_client.upload_from_url(link.url)
    except ImgurClientError as e:
        raise ImgError from e
    else:
        uploaded = Link(result['link'])
        image_registry.update(result)
        already_uploaded_links.add(link, uploaded)
        return uploaded


def process(raw_link):
    """ Process URL and return possible secure alternative
    or url for uploaded image

    :type raw_link: str
    :param raw_link: Raw url
    :return: Processed url
    :rtype: str
    """

    link = Link(raw_link)

    if link in already_uploaded_links:
        return already_uploaded_links[link]

    if link in insecure_domains:
        return upload(link).secure

    if link.is_secure or link in secure_domains or has_secure_domain(link):
        return link.secure

    return upload(link).secure
