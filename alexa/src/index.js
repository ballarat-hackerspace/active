var https = require('https');
var Alexa = require('alexa-sdk');

var APP_ID = 'amzn1.ask.skill.31d3dd92-1be3-4073-8af7-1a6e76fa0a2d';
var INDOOR_ACTIVITIES = 'indoor cricket, squash, basketball, laser tag';
var OUTDOOR_ACTIVITIES = 'walking, netball, running, football, soccer';

var handlers = {
    'LaunchRequest': function () {
        logEntry('LaunchRequest', this.event);
        this.emit(':ask', 'Welcome to dot space active. You can ask for an activity or I can suggest one.')
    },
    'ListActivities': function () {
        logEntry('ListActivities', this.event);
        var speechOutput = 'You can do activities like ';
        var setting = isSlotValid(this.event.request, 'setting');
        console.log('setting is ' + setting);
        switch (setting) {
            case 'inside':
            case 'in doors':
                speechOutput += INDOOR_ACTIVITIES;
                break;
            case 'outside':
            case 'out doors':
                speechOutput += OUTDOOR_ACTIVITIES;
                break;
            default:
                speechOutput += OUTDOOR_ACTIVITIES + ', ' + INDOOR_ACTIVITIES;
        }
        this.emit(':ask', speechOutput);
    },
    'AcceptActivity': function () {
        logEntry('AcceptActivity', this.event);
        var acceptance = isSlotValid(this.event.request, 'activity');


    },
    'StartActivity': function () {
        logEntry('StartActivity', this.event);
        var activity = isSlotValid(this.event.request, 'activity');
        console.log('activity is ' + activity);
        if (this.event.request.dialogState === 'STARTED') {

                var loc = 'ballarat'; //TODO hard coded
                //httpsPost(loc, myResult => {
                obtainActivity(loc, myResult => {
                    console.log("received : " + JSON.stringify(myResult));
                    this.emit(':confirmIntent', 'How about ' + myResult.data.activity.type);
                });

        } else if (this.event.request.dialogState === 'IN_PROGRESS'){
            console.log('delegating');
            this.emit(':delegate');
        } else {
            // All the slots are filled (And confirmed if you choose to confirm slot/intent)
            console.log('dialog is complete');
            console.log(this.event);
            var confirmation = false;
            if (this.event.request.intent.confirmationStatus === 'CONFIRMED') {
                confirmation = true;
            } 
            // Call back end to confirm/cancel Activity
            acceptActivity('1', confirmation, acceptActivityResult => {
                var speechOutput = "Sorry there was an error processing your request";
                if (acceptActivityResult.meta.success) { // successfully called back end to confirm
                    var confirmationString = 'canceled';
                    if (confirmation)
                        confirmationString = 'confirmed'
                    speechOutput = "Ok, your activity has been " + confirmationString;
                }                    

                this.emit(':tell', speechOutput);
            });            
        }
    },
    'AMAZON.HelpIntent': function () {
        logEntry('HelpIntent', this.event);
        speechOutput = "Ask for a particular activity, like walking or indoor cricket. Or we can find you something to do";
        reprompt = "Ask for a suggestion of something to do";
        this.emit(':ask', speechOutput, reprompt);
    },
    'AMAZON.CancelIntent': function () {
        logEntry('CancelIntent', this.event);
        var speechOutput = "ok, canceling that one";
        this.emit(':tell', speechOutput);
    },
    'AMAZON.StopIntent': function () {
        logEntry('StopIntent', this.event);
        var speechOutput = "ok, not that one";
        this.emit(':tell', speechOutput);
    },
    'SessionEndedRequest': function () {
        logEntry('SessionEndedRequest', this.event);
        var speechOutput = "thanks, good bye";
        this.emit(':tell', speechOutput);
    },
};

exports.handler = (event, context) => {
    var alexa = Alexa.handler(event, context);
    alexa.APP_ID = APP_ID;
    alexa.registerHandlers(handlers);
    alexa.execute();
};

function isSlotValid(request, slotName) {
    var slot = request.intent.slots[slotName];
    var slotValue;

    //if we have a slot, get the text and store it into speechOutput
    if (slot && slot.value) {
        //we have a value in the slot
        slotValue = slot.value.toLowerCase();
        return slotValue;
    } else {
        //we didn't get a value in the slot.
        return false;
    }
}

function logEntry(str, evt) {
    console.log(str);
    console.log(JSON.stringify(evt));
}

function obtainActivity(location, callback) {
    httpsPost('/api/activity', {"location": location}, callback);
}

function acceptActivity(activityId, confirmation, callback) {
    httpsPost('/api/activity/accept', {"id": activityId, "confirmation": confirmation}, callback);
}

//function httpsPost(location, callback) {
function httpsPost(path, value, callback) {    

    var post_options = {
        host: 'ballarathacker.space',
        port: '443',
        path: path,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(JSON.stringify(value))
        }
    };

    //TODO error handling
    var post_req = https.request(post_options, res => {
        res.setEncoding('utf8');
        var returnData = "";
        res.on('data', chunk => {
            returnData += chunk;
        });
        res.on('end', () => {
            console.log(returnData);
            callback(JSON.parse(returnData));
        });
    });
    post_req.write(JSON.stringify(value));
    post_req.end();
}