var map;
var geocoder;
var markerArray;
var icons = new Array(10);

function initializeMap() {
  var center = new google.maps.LatLng(55.316643, 23.752441);
  var mapOptions = {
    zoom: 7,
    center: center,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);

  geocoder = new google.maps.Geocoder();
  markerArray = {};

  for (var i = 0; i < 10; ++i) {
    icons[i] = new google.maps.MarkerImage("img/h-" + (i + 1) + ".png", null, null, new google.maps.Point(0, 32));
  }
}

function toggleMarker(title, loc,  hotel, visible) {
  var marker = markerArray[title];
  if (marker == null) {
    if (hotel.size != null) {
      icon_i = Math.round(9 * hotel.size / largest_hotel_size);
    } else {
      icon_i = 3;
    }
    marker = new google.maps.Marker({
      map: map,
      visible: visible,
      position: loc,
      title: title,
      icon: icons[icon_i]
    });
    markerArray[title] = marker;
  } else {
    marker.setVisible(visible);
  }
}

$(function(){
  // MAPS CODE
  initializeMap();
    
  // UI CODE
  
  var $sidebar = $('#sidebar');
  
  var test = function(item, model) {
    if (!item) {
      return false;
    }
    if (!model) {
      return true;
    }
    
    var passed = false;
    $.each(model.grades, function(i, el) {
      if (el + "*" == item.info['Klasė']) {
        passed = true;
      }
    });    
    if (!passed) {
      return false;
    }
    
    //console.log(item, model);
    
    return true;
  };
  
  var filter = function(model) {
    for (var i in hotels) {
      var hotel = hotels[i];
      var c = hotel.coords;
      toggleMarker(hotel.name, new google.maps.LatLng(c.lat, c.lng), hotel, test(hotel, model));
    }
  };
  
  var readRange = function($slider) {
    return [$slider.slider( "values", 0 ), $slider.slider( "values", 1 )];
  };
  
  var executeFilter = function() {
    
    setTimeout(function(){
      var model = {};
      //Determine selected type
      var type = [];
      $sidebar.find('.model-type-hall').is(':checked') && type.push('hall');
      $sidebar.find('.model-type-hotel').is(':checked') && type.push('hotel');
      model.type = type.join('_');

      model.grades = [];
      $sidebar.find('.model-grade .btn').each(function() {
        var $this = $(this);
        if ($this.hasClass('active')) {
          model.grades.push($this.data('value'));
        }
      });
      
      //Get filter model for conference halls
      if (model.type == 'hall' || model.type == 'hall_hotel') {
        model.hall = {
          count: $sidebar.find('.model-hall').slider('value'),
          capacity: readRange($sidebar.find('.model-hall-capacity')),
          configuration: $sidebar.find('.model-hall-configuration').select2("data"),
          celebration: $sidebar.find('.model-hall-celebration').is(':checked'),
          conference: $sidebar.find('.model-hall-conference').is(':checked'),
          hardware: $sidebar.find('.model-hall-hardware').select2("data")
        };
      }
      //Get filter model for hotel
      if (model.type == 'hotel' || model.type == 'hall_hotel') {
        model.hotel = {
            capacity: readRange($sidebar.find('.model-hotel-capacity')),
            roomCapacity: readRange($sidebar.find('.model-hotel-room-capacity')),
            food: $sidebar.find('.model-hotel-food').select2("data"),
            forDisabled: $sidebar.find('.model-hotel-for-disabled').is(':checked')            
        };        
      }
      
      //Show/hide panels for conference hall and hotel information 
      $sidebar.find('.model-hall').toggle(model.type == 'hall' || model.type == 'hall_hotel');
      $sidebar.find('.model-hotel').toggle(model.type == 'hotel' || model.type == 'hall_hotel');
      
      //Execute filter function
      filter(model);
    }, 1);   
  };
  
  var toggleAndExecute = function() {
    $(this).toggleClass('active');
    executeFilter();
  };
  
  //Set up UI controls
  $sidebar.find('.model-type-hall, .model-type-hotel, .model-hotel-for-disabled').change(executeFilter);
  
  $sidebar.find('.model-grade .btn').click(toggleAndExecute);
  
  $sidebar.find('.model-hall-count').slider({
    min: 1,
    max: 10,
    values: [ 1 ],
    slide: executeFilter
  });
  
  $sidebar.find('.model-hall-capacity').slider({
    range: true,
    min: 0,
    max: 500,
    values: [ 40, 50 ],
    slide: executeFilter
  });
  
  $sidebar.find('.model-hotel-capacity').slider({
    range: true,
    min: 0,
    max: 500,
    values: [ 40, 50 ],
    slide: executeFilter
  });
  
  $sidebar.find('.model-hotel-room-capacity').slider({
    range: true,
    min: 0,
    max: 500,
    values: [ 40, 50 ],
    slide: executeFilter
  });
  
  $sidebar.find('.model-hall-configuration').select2();
  $sidebar.find('.model-hall-hardware').select2();
  $sidebar.find('.model-hotel-food').select2();
  
  //first execution
  executeFilter();
});
