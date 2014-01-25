var map;
function initialize() {
  var mapOptions = {
    zoom: 16,
    center: new google.maps.LatLng(40.4249, -86.9162)
  };
  map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);

}

google.maps.event.addDomListener(window, 'load', initialize);