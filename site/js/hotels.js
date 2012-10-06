var map;
var geocoder;

function initializeMap() {
  var center = new google.maps.LatLng(55.316643, 23.752441);
  var mapOptions = {
    zoom: 7,
    center: center,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);

  geocoder = new google.maps.Geocoder();
}

function putMarker(title, loc) {
  var marker = new google.maps.Marker({
    map: map,
    position: loc,
    title: title
  });
}

$(function(){
  initializeMap();
  for (var i in hotels) {
    var hotel = hotels[i];
    var c = hotel.coords;
    if (c) {
      putMarker(hotel.name, new google.maps.LatLng(c.lat, c.lng));
    }
  }
});
