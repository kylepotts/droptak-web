/**
 * Maptak JS Library
 * 
 **/
var markers = [];

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

	var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);


	var addMarker = function(location) {
		var marker = new google.maps.Marker({
			position: location,
			map: map
		});
		markers.push(marker);
	}
	location = new google.maps.LatLng(0, 0);

	google.maps.event.addDomListener(window, "resize", function () {
		var center = map.getCenter();
		google.maps.event.trigger(map, "resize");
		map.setCenter(center);
	});
}

google.maps.event.addDomListener(window, 'load', initialize);