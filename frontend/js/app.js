// Global vars
var map;
var cells = {};
var mapBounds  = {
  north: 31,
  south: 25,
  east: -79,
  west: -88
};;

// Florida boundaries
/*mapBounds = {
  north: 31,
  south: 25,
  east: -80,
  west: -88
};*/


// Stuff for coloring cells
var shades = ["#FFEBEE", "#FFCDD2", "#EF9A9A", "#E57373", "#EF5350", "#F44336"];
var opacity = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5];

// Firebase setup
var firebase = new Firebase("https://tweetengine.firebaseio.com/");
var locations = firebase.child("locations");

// Draw square on map for given params
function makeSquare(bounds, map, color) {
  return new google.maps.Rectangle({
    strokeColor: color,
    strokeOpacity: 0.00,
    strokeWeight: 0,
    fillColor: color,
    fillOpacity: 0.05,
    map: map,
    bounds: bounds,
    clickable:false
  });
}

// Modify cell shade for given lng, lat.
function shadeCell(rect, opacity) {
  rect.setOptions({fillOpacity:opacity, map:map});
}

function calculateOpacity(rate) {
  var opacity = rate/3;
  if(opacity > 100) {
    return 100;
  } else {
    return opacity;
  }
}

// Output cell deets to console
function printCell(lng,lat) {
  var rect = cells[lat][lng];
  console.log(rect.cell.fillColor);
}

// Init draw cells on map
function drawCell(x, y, width) {

  var cellBounds = {
    north: y + width,
    south: y,
    east: x + width,
    west: x
  };

  return makeSquare(cellBounds, map, shades[5]);

}


function init() {

  // Prepare the map
  var mapCanvas = document.getElementById('map');
  var mapOptions = {
    //draggable: false,
    //zoomControl: false,
    //scrollwheel: false,
    //disableDoubleClickZoom: true,
    //mapTypeControl: false,
    //zoomControl: false,
    center: new google.maps.LatLng(28, -84),
    zoom: 7,
    disableDefaultUI: true
  };
  map = new google.maps.Map(mapCanvas, mapOptions);

} // init()

// Listen for new nodes
locations.on("child_added", function(snapshot) {
  var cellName = snapshot.key();
  var cell = snapshot.val();
  console.log("Added new cell " + cellName + " at " + cell.x + ", " + cell.y);
  cells[cellName] = drawCell(cell.x, cell.y, cell.width)
});

// Listen for updates
locations.on("child_changed", function(snapshot) {
  var cellName = snapshot.key();
  var cellVal = snapshot.val();
  console.log("Updated on cell " + cellName);
  var cell = cells[cellName]
  if(cell == undefined) {
    cells[cellName] = drawCell(cellVal.x, cellVal.y, cellVal.width);
    cell = cells[cellName];
  }
  shadeCell(cell, calculateOpacity(cellVal.velocity));
});

// Listen for nodes shutting down
locations.on("child_removed", function(snapshot){
  var cellName = snapshot.key();
  delete cells[cellName];
});

// Set the listen to init everything on load
google.maps.event.addDomListener(window, 'load', init);
