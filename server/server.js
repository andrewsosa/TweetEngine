// server.js

// BASE SETUP
// =============================================================================

// call the packages we need
var express     = require('express');        // call express
var app         = express();                 // define our app using express
var bodyParser  = require('body-parser');

// configure app to use bodyParser()
// this will let us get the data from a POST
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

var port = process.env.PORT || 8080;        // set our port

// ROUTES FOR OUR API
// =============================================================================
var router = express.Router();              // get an instance of the express Router

// middleware to use for all requests
router.use(function(req, res, next) {
    // do logging
    console.log('Someone is connecting!');
    next(); // make sure we go to the next routes and don't stop here
});

// test route to make sure everything is working (accessed at GET http://localhost:8080/api)
router.get('/', function(req, res) {
    res.json({message: 'This is where the TweetEngine lives.'});
});

// Used by new connecting nodes
router.route('/connect')

    // register a connection
    .post(function(req, res) {

        // assign the new node a sector
        x = 30;
        y = -85;

        // Let them know
        res.json({
            message: 'Connection successful.',
            target: {
                southwest: {
                    longitude: x,
                    latitude: y
                },
                northeast: {
                    longitude: x + 1,
                    latitude: y + 1
                }
            }
        });

    });


// Used by actively working nodes
router.route('/update')

    // upload new data about a point
    .post(function(req, res){

        // extract location and velocity

    });

// REGISTER OUR ROUTES -------------------------------
// all of our routes will be prefixed with /api
app.use('/api', router);

// START THE SERVER
// =============================================================================
app.listen(port);
console.log('Magic happens on port ' + port);


/*
// more routes for our API will happen here
// on routes that end in /feed
// ----------------------------------------------------
router.route('/feed')

    // create a feed (accessed at POST http://localhost:8080/api/feed)
    .post(function(req, res) {

        var feed = new Feed();      // create a new instance of the Feed model
        feed.message = req.body.message;  // set the feed name (comes from the request)
        feed.authorID = req.body.authorID;
        // save the feed and check for errors
        feed.save(function(err) {
            if (err)
                res.send(err);

            res.json({ message: 'Feed post created!' });
        });
    })

    // get all the feed objs (accessed at GET http://localhost:8080/api/feed)
    .get(function(req, res) {
        Feed.find(function(err, feed) {
            if (err)
                res.send(err);

            res.json(feed);
        });

    });

// on routes that end in /feed/:feed_id
// ----------------------------------------------------
router.route('/feed/:feed_id')

    // get the feed with that id (accessed at GET http://localhost:8080/api/feeds/:feed_id)
    .get(function(req, res) {
        Feed.findById(req.params.feed_id, function(err, feed) {
            if (err)
                res.send(err);
            res.json(feed);
        })

    // update the feed obj with this id (accessed at PUT http://localhost:8080/api/feed/:feed_id)
    .put(function(req, res) {

        // use our feed model to find the feed we want
        Feed.findById(req.params.feed, function(err, feed) {

            if (err)
                res.send(err);

            feed.message = req.body.message;  // update the feeds info
            feed.authorID = req.body.authorID;

            // save the feed
            feed.save(function(err) {
                if (err)
                    res.send(err);
                res.json({ message: 'Feed updated!' });
            });

        });
    })

    // delete the feed with this id (accessed at DELETE http://localhost:8080/api/feed/:feed_id)
    .delete(function(req, res) {
        Feed.remove({
            _id: req.params.feed_id
        }, function(err, feed) {
            if (err)
                res.send(err);
            res.json({ message: 'Successfully deleted' });
        });
    });

}); */
