#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    run
    ~~~
    This is the entry point into the application.
    To run the application, open your terminal and type:
    $ python run.py

    :author: Jeff Kereakoglow
    :date: 2014-11-14
    :copyright: (c) 2014 by Alexis Digital
    :license: MIT, see LICENSE for more details
"""
from app import app
import os

print("Goto: https://active-robertlayton.c9users.io")
app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 5000)), debug=True)
