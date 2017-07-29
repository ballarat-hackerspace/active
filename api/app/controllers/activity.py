#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    app.controllers.activiyt
    ~~~~~~~~~~~~~~~
    The activity controller module.

    :author: Jeff Kereakoglow
    :date: 2014-11-14
    :copyright: (c) 2014 by Alexis Digital
    :license: MIT, see LICENSE for more details
"""
from flask import abort, Blueprint, request, jsonify, g, url_for
from app.utils import *
from app.models.activity import Activity
from app import db, auth

mod = Blueprint("activity", __name__, url_prefix="/api")

@mod.route("/activity", methods=["GET"])
def get_random_activity():
    return jsonify(
        prepare_json_response(
            message=None,
            success=True,
            data=[Activity.get_random_activity().serialize]
        )
    )


@mod.route("/activity/add")
def add_some():
    
    from datetime import datetime
    
    activity1 = Activity()
    activity1.latitude = 141.1
    activity1.longitude = -31.1
    activity1.time = datetime.strptime("2017-07-29 13:01:00", "%Y-%m-%d %H:%M:%S")
    activity1.type = "Basketball"
    
    
    activity2 = Activity()
    activity2.latitude = 142.2
    activity2.longitude = -32.2
    activity2.time = datetime.strptime("2017-07-29 14:02:00", "%Y-%m-%d %H:%M:%S")
    activity2.type = "Running"
    
    activity3 = Activity()
    activity3.latitude = 143.3
    activity3.longitude = -33.3
    activity3.time = datetime.strptime("2017-07-29 15:03:00", "%Y-%m-%d %H:%M:%S")
    activity3.type = "Squash"
    
    db.session.add(activity1)
    db.session.add(activity2)
    db.session.add(activity3)
    db.session.commit()

    return jsonify({"success": True})

@mod.route("/list", methods=["GET"])
def all():
    return jsonify(
        prepare_json_response(
            message=None,
            success=True,
            data=[activity.serialize for activity in Activity.query.all()]
        )
    )


@mod.route("/activity/<int:id>", methods=["GET"])
def single(id):
    activity = Activity.query.get(id)
    if not activity:
        abort(400)

    return jsonify(
        prepare_json_response(
            message="User found",
            success=True,
            data=activity.serialize
        )
    )

