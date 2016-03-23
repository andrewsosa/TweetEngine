// server.js

// BASE SETUP
// =============================================================================

// call the packages we need
var express     = require('express');        // call express
var app         = express();                 // define our app using express
var bodyParser  = require('body-parser');
var firebase    = require('firebase');
var tokengen    = require('firebase-token-generator')
var hri         = require('human-readable-ids').hri;
var Flutter     = require('flutter');
var session     = require('express-session');
var register    = require('node-persist');

// Init the register of user/node storage
register.initSync();

var host = "http://localhost:8080/engine";
var port = process.env.PORT || 8080;        // set our port
var cells = {};

// Check for enviromental vars
// =============================================================================
var consumer_key = "<consumer_key>";
var consumer_secret = "<consumer_secret>";
var firebase_secret = "<firebase_secret>";
var session_sercet = "<session_secret>";

/*if(consumer_key == null) {
    console.log("Missing required enviromental variable TWEET_ENGINE_CONSUMER_KEY");
    exit(1);
} else if (consumer_secret == null) {
    console.log("Missing required enviromental variable TWEET_ENGINE_CONSUMER_SECRET");
    exit(1);
} else if (firebase_secret == null) {
    console.log("Missing required enviromental variable TWEET_ENGINE_FIREBASE_SECRET");
    exit(1);
} else if (session_sercet == null) {
    console.log("Missing required enviromental variable TWEET_ENGINE_SESSION_SECRET");
    exit(1);
} */


// configure app to use bodyParser()
// this will let us get the data from a POST
// =============================================================================
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.use(session({
    secret: session_sercet,
    resave: false,
    saveUninitialized: true})
);


// Firebase Auth and Connection
// =============================================================================
var tokenGenerator = new tokengen(firebase_secret);
var token = tokenGenerator.createToken(
    {uid: "forkingqueue", boss: "andrewthewizard"},
    {admin:true}
);

var ref  = new Firebase("https://tweetengine.firebaseio.com/locations");
ref.authWithCustomToken(token, function(error, authData) {
    if (error) {
      console.log("Login Failed!", error);
    } else {
      console.log("Login Succeeded!");
    }
});


// Twitter OAuth Support
// =============================================================================
var flutter = new Flutter({
    consumerKey: consumer_key,
    consumerSecret: consumer_secret,
    loginCallback: host + '/callback',
    cache: false,
    connectCallback: function(req, res) {
        if (req.error) {
          console.log(req.error);
          return res.send('Oh no an error');
        }
    },
    authCallback: function(req, res, next) {
        if (req.error) {
            console.log(req.error);
            return res.send('Oh no an error');
        }

        // Store away oauth credentials here
        var accessToken = req.session.oauthAccessToken;
        var accessSecret = req.session.oauthAccessTokenSecret;
        var nodeID = hri.random();

        // Record user
        register.setItem(nodeID, accessToken);

        var msg =   "Please copy the following into the bottom of your config.py:" + "</br></br></br>" +
                    "ACCESS_TOKEN = \"" + accessToken + "\"</br>" +
                    "ACCESS_TOKEN_SECRET = \"" + accessSecret + "\"</br>" +
                    "NODE_ID = \"" + nodeID + "\""

        res.send(msg)

    }
});

// Cell tracking
// =============================================================================

function validateNode(id, token) {
    return (token == register.getItem(id));
}

function initCoords() {
    for (i = -180; i <= 180 ; i++) {
        for (j = -90; j <= 90; j++ ) {
            cells[''+i+','+j] = null;
        }
    }
}
initCoords();

function approveCoords(southwest, northeast, id) {

    // check if we're cool first
    for (i = southwest.x; i <= northeast.x; i++) {
        for (j = southwest.y; j <= northeast.y; j++) {
            if (cells[''+i+','+j] != null) {
                return false;
            }
        }
    }

    // alloc the requested areas
    for (i = southwest.x; i <= northeast.x; i++) {
        for (j = southwest.y; j <= northeast.y; j++) {
            cells[''+i+','+j] = id;
        }
    }

    return true;

}

function disconnectCoords(southwest, northeast, id) {
    // dealloc the requested areas
    for (i = southwest.x; i <= northeast.x; i++) {
        for (j = southwest.y; j <= northeast.y; j++) {
            if (cells[''+i+','+j] == id) {
                cells[''+i+','+j] = null;
            }
        }
    }
}


// ROUTES FOR OUR API
// =============================================================================
var router = express.Router();      // get an instance of the express Router

// Middleware to use for all requests.
router.use(function(req, res, next) {
    // Verify and log a connection.

    // Move along, move along.
    next();
});

// Test route
router.get('/', function(req, res) {
    res.json({message: 'This is where the TweetEngine lives.'});
});

// Twitter Auth handlers
router.get('/register', flutter.connect);
router.get('/callback', flutter.auth);

// Get update messages from the server
router.post('/status', function(req, res) {

    // Validate they're cool
    if(!validateNode(req.body.id, req.body.token)) {
        console.log("Denying connection");
        res.json({message:'You are not registered.', version: 1.0});
        return;
    }

    res.json({
        message: "Server running.",
        version: 1.0
    });
});

// Used by connecting nodes to get an assignment.
router.post('/connect', function(req, res) {

    // Validate they're cool
    if(!validateNode(req.body.id, req.body.token)) {
        console.log("Denying connection");
        res.json({message:'Request denied.'});
        return;
    }

    // Approve their location request
    var approved = approveCoords(req.body.southwest, req.body.northeast, req.body.id);

    if(approved) {
        // Send back the extras data
        res.json({
            appr: true,
            message: "Connection approved.",
            extras: ['python'],
            target: {
                southwest: {
                   longitude: req.body.southwest.x,
                   latitude: req.body.southwest.y
                },
                northeast: {
                   longitude: req.body.northeast.x,
                   latitude: req.body.northeast.y
                }
       }
        });
    } else {
        res.json({
            appr: false,
            message: "Coordinates overlap. Please consult map to find open area."
        });
    }
});

router.post('/disconnect', function(req, res){

    // Validate they're cool
    if(!validateNode(req.body.id, req.body.token)) {
        console.log("Denying connection");
        res.json({message:'Request denied.'});
        return;
    }

    disconnectCoords(req.body.southwest, req.body.northeast, req.body.id);

    res.json({
        message: "Disconnected coordinates."
    })

});


// Used by actively working nodes to upload coord data
router.post('/upload', function(req, res){

    // Validate they're cool
    if(!validateNode(req.body.id, req.body.token)) {
        res.json({message:'Request denied.'});
        res.json({message:'Request denied.'});
        return;
    }

    // Make sure the location matches their ID



    var pos = "" + req.body.x + "," + req.body.y;

    var msg = "Receiving update on tile " + pos + " from node " + req.body.id;
    console.log(msg);

    var loc = ref.child(pos);
    loc.set({
        x: parseFloat(req.body.x),
        y: parseFloat(req.body.y),
        width: parseFloat(req.body.width),
        velocity: parseFloat(req.body.velocity),
        acceleration: parseFloat(req.body.acceleration),
        torque: parseFloat(req.body.torque)
    });

    res.json({
        message: 'Upload received.'
    });

});

// REGISTER OUR ROUTES -------------------------------
// all of our routes will be prefixed with /engine
app.use('/engine', router);

// START THE SERVER
// =============================================================================
app.listen(port);
console.log('Magic happens on port ' + port);
