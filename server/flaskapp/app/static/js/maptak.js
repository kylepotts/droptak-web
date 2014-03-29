/**
 * Maptak JS Library
 * requires: Google maps v3 , JQuery
 **/

var markers = [];
var map;

/**
* initialize the map
*/
function initialize() {

	var myLatlng = new google.maps.LatLng(40.43, -86.92);
	
	var styleArray = [{
		"featureType": "poi",
		"stylers": [{
			"visibility": "off"
		}]
	}];

	var mapOptions = {
		zoom: 14,
		center: myLatlng,
		styles: styleArray
	}

	map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

	google.maps.event.addDomListener(window, "resize", function () {
		var center = map.getCenter();
		google.maps.event.trigger(map, "resize");
		map.setCenter(center);
	});
}

function addMarker(lat, lng) {
	marker = new google.maps.Marker({
		position: new google.maps.LatLng(lat, lng),
		map: map
	});
	markers.push(marker);
}

/**
* Asynchronously load google maps into body
* after completion, it calls the callback which is initialize
*/
function loadGoogleMaps() {
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyBHXLk2GBOiUDeMZp5VMtUY9Pu8aiPZrao&sensor=false&libraries=drawing&callback=initialize';
  document.body.appendChild(script);
}

window.onload = loadGoogleMaps;