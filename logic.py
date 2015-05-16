from imgurpython.helpers.error import ImgurClientError

from lib import Link
from application import secure_domains, already_uploaded_links, imgur_client, image_registry


def process(raw_link):
    link = Link(raw_link)

    if link.is_secure or link in secure_domains:
        return link.secure

    if link in already_uploaded_links:
        return already_uploaded_links[link]

    try:
        result = imgur_client.upload_from_url(link.url)
    except ImgurClientError:
        return None
    else:
        uploaded = Link(result['link'])
        image_registry.update(result)
        already_uploaded_links += (link, uploaded)
        return uploaded.secure
