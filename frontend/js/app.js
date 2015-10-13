// Global vars
var map;
var cells;
var mapBounds;

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

function getCellFromLngLat(lng, lat) {
  var x = lng - mapBounds.west;
  var y = lat - mapBounds.south;
  return {cell:cells[x][y].cell, x:x, y:y};
}

// Modify cell shade for given lng, lat.
function shadeCell(lng, lat, opacity) {
  var rect = cells[lng][lat].cell;
  rect.setOptions({fillOpacity:opacity, map:map});
}

function calculateOpacity(rate) {
  var opacity = rate/10;
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

// Push cell to db
function initDBLocation(lng, lat) {
  var name = lng.toString() + "," + lat.toString();
  locations.child(name).update({
    x:lng,
    y:lat,
  });
}

function initCells(west, south, east, north) {

  // Init draw cells on map
  function drawCell(x, y) {

    var latNorth = (y + 1);
    var latSouth = y;
    var lngEast = (x + 1);
    var lngWest = x;

    cellBounds = {
      north: latNorth,
      south: latSouth,
      east: lngEast,
      west: lngWest
    };

    return makeSquare(cellBounds, map, shades[5]);
  }

  var bounds = {
    north: north + 1,
    east: east + 1,
    south: south,
    west: west
  }

  // Init array
  cells = [];

  // 2D for loop for lat/lng
  for(x = bounds.west; x < bounds.east; ++x) {
    cells.push([]);
    for(y = bounds.south; y < bounds.north; ++y) {
      cells[x-bounds.west].push({cell:drawCell(x, y)});
      initDBLocation(x,y);
    }
  }

  // TODO Initial shading


}

function init() {

  // Prepare the map
  var mapCanvas = document.getElementById('map');
  var mapOptions = {
    draggable: false,
    zoomControl: false,
    scrollwheel: false,
    disableDoubleClickZoom: true,
    mapTypeControl: false,
    zoomControl: false,
    center: new google.maps.LatLng(28, -84),
    zoom: 7,
    disableDefaultUI: true
  };
  map = new google.maps.Map(mapCanvas, mapOptions);

  initCells(-88, 25, -80, 31);

  mapBounds = {
    north: 31,
    south: 25,
    east: -80,
    west: -88
  };

  // tallahassee=[-85,30,-84,31]


  /*for(arr in cells){
    for(entry in arr){
      initDBLocation(entry.cell.)
    }
  }*/

} // init()

// Listen for updates
locations.on("child_changed", function(snapshot) {
  var changedPost = snapshot.val();
  console.log("Updated on cell " + changedPost.x + " " + changedPost.y);

  var temp = getCellFromLngLat(changedPost.x, changedPost.y);


  console.log("Needs array " + (temp.x).toString() + " " + (temp.y).toString());
  shadeCell(temp.x, temp.y, calculateOpacity(changedPost.velocity));
});


// Set the listen to init everything on load
google.maps.event.addDomListener(window, 'load', init);
