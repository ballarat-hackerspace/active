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
import random


mod = Blueprint("activity", __name__, url_prefix="/api")


@mod.route("/activity", methods=["GET", "POST"])
def get_activity_by_preferences():
    activity_type = request.json.get("activity_type", None)
    going_to_rain, rain_percentage = is_it_going_to_rain()
    
    activities = []
    
    # Find only activities of this type
    activities = [activity for activity in Activity.query.all()
                      # If an activity type not given, of if one was given and its of this type
                  if ((not activity_type) or activity.type == activity_type)
                       # if its indoor, it doesn't matter if its going to rain
                  and ((activity.indoor) or 
                       # Only suggest outdoor activities if it isn't going to rain 
                       (activity.outdoor and not is_rain))
                 ]

    if not activities:
        message = "I couldn't find that"
        # Couldn't find an activity. This would really only happen if an activity was asked for, so choose one from the other activities
        activities = [activity for activity in Activity.query.all()
                      # If an activity type not given, of if one was given and its of this type
                  if  # if its indoor, it doesn't matter if its going to rain
                      ((activity.indoor) or 
                       # Only suggest outdoor activities if it isn't going to rain 
                       (activity.outdoor and not is_rain))
                 ]

    # If we found valid activities, choose one of the activities received at random and return it
    activity = random.choice(activities)
    
    data = {"activity": activity.serialize, 'message': message}
    return jsonify(
        prepare_json_response(
            message=None,
            success=True,
            data={'activity':activity.serialize, "message": message, 'going_to_rain': going_to_rain, 'rain_percentage': rain_percentage}
        )
    )
        
        
def is_it_going_to_rain():
    # @srw put BOM stuff here
    rain_percentage = random.random()
    going_to_rain = rain_percentage > 0.5  # Actually make a decision here
    
    
    return going_to_rain, rain_percentage


@mod.route("/activity/add")
def add_some():
    
    from datetime import datetime
    
    activity1 = Activity()
    activity1.latitude = 141.1
    activity1.longitude = -31.1
    activity1.time = datetime.strptime("2017-07-29 13:01:00", "%Y-%m-%d %H:%M:%S")
    activity1.type = "Basketball"
    activity1.indoors = True
    activity1.outdoors = True
    
    
    activity2 = Activity()
    activity2.latitude = 142.2
    activity2.longitude = -32.2
    activity2.time = datetime.strptime("2017-07-29 14:02:00", "%Y-%m-%d %H:%M:%S")
    activity2.type = "Running"
    activity2.indoors = False
    activity2.outdoors = True
    
    activity3 = Activity()
    activity3.latitude = 143.3
    activity3.longitude = -33.3
    activity3.time = datetime.strptime("2017-07-29 15:03:00", "%Y-%m-%d %H:%M:%S")
    activity3.type = "Squash"
    activity3.indoors = True
    activity3.outdoors = False
    
    activity4 = Activity()
    activity4.latitude = 144.4
    activity4.longitude = -34.4
    activity4.time = datetime.strptime("2017-07-29 16:04:00", "%Y-%m-%d %H:%M:%S")
    activity4.type = "Laser Tag"
    activity4.indoors = True
    activity4.outdoors = False
    
    activity5 = Activity()
    activity5.latitude = 145.5
    activity5.longitude = -35.5
    activity5.time = datetime.strptime("2017-07-29 17:05:00", "%Y-%m-%d %H:%M:%S")
    activity5.type = "FPV Drone Racing"
    activity5.indoors = True
    activity5.outdoors = True
    
    db.session.add(activity1)
    db.session.add(activity2)
    db.session.add(activity3)
    db.session.add(activity4)
    db.session.add(activity5)
    db.session.commit()

    return jsonify({"success": True})

@mod.route("/activity/list", methods=["GET"])
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

@mod.route("/activity/accept")
def accept_activity():
    return jsonify(
        prepare_json_response(
            message="Activity accepted",
            success=True,
            data={}
        )
    )
