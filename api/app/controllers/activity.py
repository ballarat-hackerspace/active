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
from dateutil import parser
from datetime import datetime, timezone
import random
import requests


mod = Blueprint("activity", __name__, url_prefix="/api")

# Morphed form of http://data.gov.au/geoserver/ballarat-indoor-recreation-facilities/wfs?request=GetFeature&typeName=9006b1fc_9a36_425d_ae2a_6307c37c99c9&outputFormat=json
facilities = {'The Arch Centre, Ballarat High School Alfredton': ('-37.554031',
  '143.816944'),
 'Eastwood Leisure Complex Ballarat': ('-37.565328', '143.862280'),
 'Ballarat East Recreation Centre Ballarat East': ('-37.560247', '143.892782'),
 'Buninyong Sports Centre Buninyong': ('-37.653405', '143.886064'),
 'Delacombe Recreation Centre Delacombe': ('-37.583788', '143.817585'),
 'Ballarat Netball Centre Golden Point': ('-37.567756', '143.866350'),
 'Damascus College Mt Clear': ('-37.611270', '143.869159'),
 'Ballarat Basketball Centre (Minerdome) Wendouree': ('-37.528130',
  '143.841241'),
 'Wendouree Sports and Events Centre Wendouree': ('-37.535142', '143.843603'),
 'Ballarat Badminton Centre Wendouree': ('-37.527529', '143.841871'),
 'Ballarat Table Tennis Centre Wendouree': ('-37.524810', '143.841591'),
 'Learmonth Recreation Reserve': (739818, 5854882),
 'Alfredton Recreation Reserve': (747286, 5839794),
 None: (747236, 5839599),
 'Binney  Reserve (Binney Street Res.)': (753649, 5840301),
 'Brown Hill Reserve  (Progress Park)': (755864, 5840005),
 'Buninyong Community Facility': (755069, 5829107),
 'Cardigan Village Reserve': (739445, 5844692),
 'C.E Brown Reserve': (751335, 5841694),
 'City Oval': (750668, 5839420),
 'Doug Dean Reserve': (748692, 5836556),
 'Eastern Oval': (752802, 5839357),
 'Grant Street Reserve': (749997, 5834141),
 'Invermay Recreation Reserve': (754222, 5843184),
 'Llanberris Athletics Reserve': (753128, 5838175),
 'Russell Square': (754758, 5839497),
 'MARKS RESERVE': (752959, 5841018),
 'Marty Busch Reserve': (751094, 5834328),
 'McKenzie Reserve': (753702, 5838745),
 'Morshead Park': (750335, 5837058),
 'MT CLEAR RECREATION RESERVE (MT CLEAR TECH RESERVE)': (753773, 5833909),
 'Mt Pleasant Reserve': (751763, 5837196),
 'M.R Power Park': (749712, 5834715),
 'NORTHERN OVAL': (751640, 5841483),
 'Pleasant Street Reserve': (750480, 5837892),
 'Prince of Wales Park': (748810, 5840366),
 'Ballarat Botanical Gardens (South)': (749251, 5840095),
 'Sparrow Ground Reserve': (754779, 5837212),
 'St Georges Reserve': (750674, 5835691),
 'Trekardo Park': (750643, 5837994),
 'Victoria Park': (749329, 5838415),
 'Wendouree West Recreation Reserve': (749113, 5843165),
 'Western Oval': (750763, 5838627),
 'White Flat': (752285, 5838200),
 'Wyndholm Reserve': (749510, 5843464),
 'Yarana Drive Park': (753699, 5831968)}  # TODO: Convert all to lat/lon
 


@mod.route("/activity", methods=["GET", "POST"])
def get_activity_by_preferences():
    data = request.json
    
    if not data:
        data = {}
    
    activity_type = data.get("activity_type", None)
    going_to_rain, rain_percentage = is_it_going_to_rain()

    activities = []
    message = "We found an activity for you!"
    
    # Find only activities of this type
    activities = [activity for activity in Activity.query.all()
                      # If an activity type not given, of if one was given and its of this type
                  if ((not activity_type) or activity.type == activity_type)
                       # if its indoor, it doesn't matter if its going to rain
                  and ((activity.indoors) or 
                       # Only suggest outdoor activities if it isn't going to rain 
                       (activity.outdoors and not going_to_rain))
                 ]

    if not activities:
        message = "I couldn't find that"
        # Couldn't find an activity. This would really only happen if an activity was asked for, so choose one from the other activities
        activities = [activity for activity in Activity.query.all()
                      # If an activity type not given, of if one was given and its of this type
                  if  # if its indoor, it doesn't matter if its going to rain
                      ((activity.indoors) or 
                       # Only suggest outdoor activities if it isn't going to rain 
                       (activity.outdoors and not going_to_rain))
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
    ballarat_geohash = 'r1q63d4'
    bom_api = 'https://api.cloud.bom.gov.au/forecasts/v1/grid/three-hourly/%s/precipitation'
    bom_key = 'rmRCkYgM2Y1TffChzB8JtaJxzd6dv2SU4dIk0tj7'

    r = requests.get(bom_api % ballarat_geohash,
                     headers={"accept": "application/vnd.api+json",
                              "x-api-key": bom_key })

    if r.status_code != 200:
        return None, None

    prediction = r.json()
    if 'data' in prediction:
        if 'attributes' in prediction['data']:
            if 'probability_of_precipitation' in prediction['data']['attributes']:
                if 'forecast_data' in prediction['data']['attributes']['probability_of_precipitation']:
                    next_three_hours = None
                    time_now = datetime.now(timezone.utc)
                    rain_percentage = None
                    going_to_rain = None
                    for p in prediction['data']['attributes']['probability_of_precipitation']['forecast_data']:
                        dt = parser.parse(p['time'])
                        if dt > time_now:
                            rain_percentage = float(p['value'])/100.0
                            going_to_rain = rain_percentage > 0.5
                            break
                    return going_to_rain, rain_percentage
    return None, None


@mod.route("/activity/add")
def add_some():
    
    from datetime import datetime
    
    activity1 = Activity()
    activity_key = 'Ballarat Basketball Centre (Minerdome) Wendouree'
    activity1.latitude = facilities[activity_key][0]
    activity1.longitude = facilities[activity_key][1]
    activity1.facility = activity_key
    activity1.time = datetime.strptime("2017-07-29 13:01:00", "%Y-%m-%d %H:%M:%S")
    activity1.type = "Basketball"
    activity1.indoors = True
    activity1.outdoors = True
    
    
    activity2 = Activity()
    activity_key = 'Damascus College Mt Clear'
    activity2.latitude = facilities[activity_key][0]
    activity2.longitude = facilities[activity_key][1]
    activity2.facility = activity_key
    activity2.time = datetime.strptime("2017-07-29 14:02:00", "%Y-%m-%d %H:%M:%S")
    activity2.type = "Running"
    activity2.indoors = False
    activity2.outdoors = True
    
    activity3 = Activity()
    activity_key = 'Ballarat Table Tennis Centre Wendouree'
    activity3.latitude = facilities[activity_key][0]
    activity3.longitude = facilities[activity_key][1]
    activity3.facility = activity_key
    activity3.time = datetime.strptime("2017-07-29 15:03:00", "%Y-%m-%d %H:%M:%S")
    activity3.type = "Table Tennis"
    activity3.indoors = True
    activity3.outdoors = False
    
    activity4 = Activity()
    activity_key = 'Delacombe Recreation Centre Delacombe'
    activity4.latitude = facilities[activity_key][0]
    activity4.longitude = facilities[activity_key][1]
    activity4.facility = activity_key
    activity4.time = datetime.strptime("2017-07-29 16:04:00", "%Y-%m-%d %H:%M:%S")
    activity4.type = "Laser Tag"
    activity4.indoors = True
    activity4.outdoors = False
    
    activity5 = Activity()
    activity_key = 'Eastwood Leisure Complex Ballarat'
    activity5.latitude = facilities[activity_key][0]
    activity5.longitude = facilities[activity_key][1]
    activity5.facility = activity_key
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

@mod.route("/activity/accept", methods=["POST", "GET"])
def accept_activity():
    return jsonify(
        prepare_json_response(
            message="Activity accepted",
            success=True,
            data={}
        )
    )
