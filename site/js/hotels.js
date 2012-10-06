var map;
function initialize() {
  var mapOptions = {
    zoom: 7,
    center: new google.maps.LatLng(55.316643, 23.752441),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  map = new google.maps.Map(document.getElementById('map_canvas'),
  mapOptions);
}

google.maps.event.addDomListener(window, 'load', initialize);
