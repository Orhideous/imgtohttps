from lib import Link, UploadError
from application import secure_domains, already_uploaded_links


def upload(link):
    return


def process(raw_link):
    link = Link(raw_link)

    if link.is_secure or link in secure_domains:
        return link.secure

    if link in already_uploaded_links:
        return already_uploaded_links[link]

    try:
        uploaded = upload(link)
    except UploadError:
        return None
    else:
        already_uploaded_links += (link, uploaded)
        return uploaded.secure
