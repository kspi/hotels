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

function getCoords(address, ok, fail) {
  geocoder.geocode({'address': address}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      if (ok) {
        ok(results[0].geometry.location);
      }
    } else {
      if (fail) {
        fail(status);
      }
    }
  });
}

function putMarker(loc) {
  var marker = new google.maps.Marker({
      map: map,
      position: loc
  });
}

$(function(){
  initializeMap();
  getCoords('Vokiečių g. 2, Vilnius', putMarker, function(status) { alert(status); });
});
