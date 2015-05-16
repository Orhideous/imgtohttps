from imgurpython.helpers.error import ImgurClientError
import requests
from lib import Link, EmptyUrlError
from application import secure_domains, insecure_domains
from application import already_uploaded_links, imgur_client, image_registry


def has_secure_domain(link):
    try:
        resp = requests.head(link.secure)
    except requests.exceptions.RequestException:
        return False
    else:
        if resp.status_code == 200:
            secure_domains.add(link)
            return True
        else:
            insecure_domains.add(link)
            return False


def upload(link):
    try:
        result = imgur_client.upload_from_url(link.url)
    except ImgurClientError as e:
        raise EmptyUrlError from e
    else:
        uploaded = Link(result['link'])
        image_registry.update(result)
        already_uploaded_links.add(link, uploaded)
        return uploaded.secure


def process(raw_link):
    link = Link(raw_link)

    if link in already_uploaded_links:
        return already_uploaded_links[link]

    if link in insecure_domains:
        return upload(link)

    if link.is_secure or link in secure_domains or has_secure_domain(link):
        return link.secure

    return upload(link)
