# -*- coding: utf-8 -*-

from fedwidgets import app

@app.route('/')
def index():
    return 'Hello Fedora!'

