#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    app.models.user
    ~~~~~~~~~~~~~~~
    The User model.

    :author: Jeff Kereakoglow
    :date: 2014-11-14
    :copyright: (c) 2014 by Alexis Digital
    :license: MIT, see LICENSE for more details
"""
from app import app, db
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context
from sqlalchemy import func


class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32), index=True)
    time = db.Column(db.DateTime())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())

    @staticmethod
    def get_random_activity():
        return Activity.query.order_by(func.random()).first()

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {"id":self.id,
               "type":self.type,
               "time":self.time.strftime("%Y-%m-%d %H:%M:%S"),
               "location": {"lat": self.latitude, "lon": self.longitude},
               "created": True}
