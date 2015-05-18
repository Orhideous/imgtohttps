=====================
Simple image uploader
=====================

About
=====

Microservice for uploading all insecure images to Imgur by url.

Use Redis as cache backend and metadata storage.

Installation
============

From PyPI::

    pip install imgtohttps

From GitHub::

    git clone https://github.com/Orhideous/imgtohttps.git

Usage
=====

Request::

    curl -X POST -H "Content-Type: application/json" -d '{"url": "http://example.com/image.png"}' http://localhost:5000

Response::

    {"url": "https://i.imgur.com/AxQwu0h.png"}

Error::

    {"error": "Some error message"}

