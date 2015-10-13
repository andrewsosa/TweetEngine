// Global(?) map
var map;
var cells;

// Florida boundaries
/*bounds = {
  north: 31,
  south: 25,
  east: -80,
  west: -87.6
};*/


var shades = ["#FFEBEE", "#FFCDD2", "#EF9A9A", "#E57373", "#EF5350", "#F44336"];
var opacity = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5];

function makeSquare(bounds, map, color) {
  return new google.maps.Rectangle({
    strokeColor: color,
    strokeOpacity: 0.05,
    strokeWeight: 1,
    fillColor: color,
    fillOpacity: 0.05,
    map: map,
    bounds: bounds,
    clickable:false
  });
}

function shadeCell(lng, lat, level) {
  var rect = cells[lat][lng].cell;
  rect.setOptions({fillOpacity:opacity[level], map:map});
  cells[lat][lng].level = level
}

// TODO fine tune level ratings
function calculateLevel(rate) {
  if(rate < 0.5) return 0;
  if(rate < 1.0) return 1;
  if(rate < 1.5) return 2;
  if(rate < 2.0) return 3;
  if(rate < 2.5) return 4;
  return 5;
}

function printCell(lng,lat) {
  var rect = cells[lat][lng];
  console.log(rect.cell.fillColor);
  console.log(rect.level);
}

function initmap() {

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

  // Function to manage calculating cell bounds
  function drawCell(x, y) {

    var latNorth = (y + 1);
    var latSouth = y;
    var lngEast = (x + 1);
    var lngWest = x;

    bounds = {
      north: latNorth,
      south: latSouth,
      east: lngEast,
      west: lngWest
    };

    return makeSquare(bounds, map, shades[5]);
  }

  // Init array
  cells = [];

  // 2D for loop for lat/lng
  for(y = 25; y < 31; ++y) {

    // Push new subarray for each row
    cells.push([]);

    // Draw cell for each column on the new row
    for(x = -88; x < -79; ++x) {
      cells[y-25].push({cell:drawCell(x, y),level:0});
    }
  }

} // initMap()

// Set the listen to init everything on load
google.maps.event.addDomListener(window, 'load', initmap);
