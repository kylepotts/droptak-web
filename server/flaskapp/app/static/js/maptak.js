/**
 * Maptak JS Library
 * requires: Google maps v3 , JQuery
 **/
 var map_initialized = false;
 var markers = [];
 var asycmarkers = [];
 var map;
 var bounds;
 var myLatlng;
 var globalinfowindow;
 // var geocoder;
  

/**
* initialize the map
*/
function initialize() {
	// geocoder = new google.maps.Geocoder();
	myLatlng = new google.maps.LatLng(40.43, -86.92);
	var styleArray = [{
		"featureType": "poi",
		"stylers": [{
			"visibility": "off"
		}]
	}];
	bounds = new google.maps.LatLngBounds();
	var mapOptions = {
		zoom: 14,
		center: myLatlng,
		styles: styleArray,
		mapTypeId: google.maps.MapTypeId.ROADMAP,
		panControl: true, 
		zoomControl: true, 
		zoomControlOptions: {
			style: google.maps.ZoomControlStyle.LARGE,
			position: google.maps.ControlPosition.LEFT_CENTER
		},
		mapTypeControl: true,
		scaleControl: true, 
		streetViewControl: true, 
	}

	map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

	google.maps.event.addDomListener(window, "resize", function () {
		var center = map.getCenter();
		google.maps.event.trigger(map, "resize");
		map.setCenter(center);
	});
	map_initialized = true;
	globalinfowindow = new google.maps.InfoWindow();
	for (var i = 0; i < asycmarkers.length; i++) {
		setMarkers(asycmarkers);
	}
}
function addInfoWindow(marker) {
	var infoWindow = new google.maps.InfoWindow({
		content: '<h2>' + marker.title + '</h2>' +
				' <div><span>' + marker.position.lat() + ', ' + marker.position.lng() + '</span></div>' 
	});

	google.maps.event.addListener(marker, 'click', function () {
		globalinfowindow.close();
		globalinfowindow = infoWindow;
		infoWindow.open(map, marker);
	});
}
function addMarker(lat, lng, opts) {
	opts = opts || {};
    opts.title = opts.title || "";
    if(map_initialized){
		marker = new google.maps.Marker({
			position: new google.maps.LatLng(lat, lng),
			map: map,
			title: opts.title
		});
		addInfoWindow(marker);
		markers.push(marker);
		bounds.extend(marker.position);
	}
	else{
		var c = {
			lat: lat,
			lng: lng,
			opts: opts
		}
		asycmarkers.push(c);
	}
}
// Sets the map on all markers in the array.
function setAllMap(map) {
	for (var i = 0; i < markers.length; i++) {
		markers[i].setMap(map);
	}
}
// sets all markers invisible but keeps in array
function clearMarkers() {
	setAllMap(null);
}
// fit all markers on map without zooming in too far
function fitMarkers(){
	if(markers.length == 0){
		// no markers so set to purdue
		bounds.extend(myLatlng);

	}
	if (bounds.getNorthEast().equals(bounds.getSouthWest())) {
       var extendPoint1 = new google.maps.LatLng(bounds.getNorthEast().lat() + 0.01, bounds.getNorthEast().lng() + 0.01);
       var extendPoint2 = new google.maps.LatLng(bounds.getNorthEast().lat() - 0.01, bounds.getNorthEast().lng() - 0.01);
       bounds.extend(extendPoint1);
       bounds.extend(extendPoint2); 
    }
    map.fitBounds(bounds);
}
// removes all markers
function deleteMarkers(){
	clearMarkers();
	markers = [];
	bounds = new google.maps.LatLngBounds();
}
function setMarkers(data) {
	deleteMarkers();
	console.log(data);
	for (var i = 0; i < data.length; i++) {
		addMarker(data[i].lat, data[i].lng, {title: data[i].title});
	}
	fitMarkers();
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