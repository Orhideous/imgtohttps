=====================
Simple image uploader
=====================

About
=====

Microservice for uploading all insecure images to Imgur by url.

Use Redis as cache backend and metadata storage.

Installation
============

Install uwsgi and python3 plugin::

    sudo apt-get install uwsgi uwsgi-plugin-python3

Make virtualenv::

    cd /opt
    pyvenv-3.4 img_service
    source img_service/bin/activate

Install from PyPI::

    pip install imgtohttps

Create config file for app::

    [uwsgi]
    plugins = python34
    master = true
    enable-threads = true
    processes = 4
    module = imgtohttps.application:app
    virtualenv = /opt/img_service
    chdir = /opt/img_service
    touch-reload = /opt/img_service/reload
    env=APP_SETTINGS=settings.Production

Connect to nginx::

    server {
        listen		127.0.0.1:2100;
        access_log off;
        location / {
            uwsgi_pass	unix:/run/uwsgi/app/img_service/socket;
            include		uwsgi_params;
        }
    }

Usage
=====

Request::

    curl -X POST -H "Content-Type: application/json" -d '{"url": "http://example.com/image.png"}' http://localhost:2100

Response::

    {"url": "https://i.imgur.com/AxQwu0h.png"}

Error::

    {"error": "Some error message"}

