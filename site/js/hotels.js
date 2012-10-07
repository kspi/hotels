var map;
var geocoder;
var markerArray;
var icons = new Array(10);
var infoWindow;

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

  infoWindow = new google.maps.InfoWindow();
}

function formatKey(obj, key, bold) {
  if (obj[key]) {
    return '<p>' + (bold ? '<b>' : '') + key + (bold ? '</b>' : '') + ': ' + obj[key] + '</p>';
  } else {
    return '';
  }
}

function formatSpans(obj, key, bold) {
  if (obj[key]) {
    return '<span>' + (bold ? '<b>' : '') + key + (bold ? '</b>' : '') + ': ' + obj[key] + '</span><br/>';
  } else {
    return '';
  }
}

function formatKeyValue(key, value, bold) {
  return '<p>' + (bold ? '<b>' : '') + key + (bold ? '</b>' : '') + ': ' + value + '</p>';  
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

    var info = [];
    info.push('<h5>', title, ' ( ', hotel.rank, ' žvaigždutės )</h5>');
    if (hotel.size != null) {
      info.push(formatKey(hotel.info, 'Vietų skaičius', true));
    }
    
    if (hotel.halls.length) {
      for (var i in hotel.halls) {
        var hall = hotel.halls[i];
        var hallnum = parseInt(i) + 1;
        info.push('<div class="hall-info">');
        info.push('<p><strong>Salė ' + hallnum + (hall.name ? ': ' + hall.name : '') + '</strong></p>');
        info.push('<p>');
        if (hall['Konferencijoms'] == 'Y') {
          info.push('Konferencijoms<br>');
        }
        if (hall['Pobūviams'] == 'Y') {
          info.push('Pobūviams<br>');
        }
        info.push('</p>');
        for(var j in hall.configurations) {
          var conf = hall.configurations[j];
          console.log(conf.people, conf.name);
          info.push(formatKeyValue(conf.name, conf.people + ' asmenų', true));
        }
        info.push(formatKey(hall, 'Įranga', true));
        info.push(formatKey(hall, "Plotas (kv. m.)", true));
        info.push('</div>');
      }
    }
    
    info.push("<div class=\"additional-info\"><b>Papildoma informacija:</b><br/>");
    info.push(formatSpans(hotel.info, "Telefonas", false));
    info.push(formatSpans(hotel.info, "Svetain\u0117s adresas", false));
    info.push(formatSpans(hotel.info, "El. pa\u0161tas", false));
    info.push(formatSpans(hotel.info, "Inventoriaus nuoma", false));
    info.push(formatSpans(hotel.info, "Maitinimo paslaugos", false));
    info.push(formatSpans(hotel.info, "Pri\u0117mimo m\u0117n.", false));
    info.push(formatSpans(hotel.info, "Darbo valandos", false));
    info.push(formatSpans(hotel.info, "Papildomos paslaugos", false));
    info.push('</div>');
    
    google.maps.event.addListener(marker, 'click', function() {
      infoWindow.setContent(info.join(''));
      infoWindow.open(map, marker);
    });
  } else {
    marker.setVisible(visible);
  }
}

$(function(){
  // MAPS CODE
  initializeMap();
  
  var firstPass = function(hotel) {
    
    var prep = {
      star: hotel.info['Klasė'].replace('*', '').trim(),
      capacity: parseInt(hotel.info['Vietų skaičius'], 10),
      roomCapacity: parseInt(hotel.info['Kambarių skaičius'], 10),
      forDisabled: (hotel.info['Pritaikyta neįgaliesiems'] || '').toLowerCase() == 'yra',
      food: {},
      hall: {
        count: hotel.halls.length,
        celebration: false,
        conference: false
      }
    };
    
    var configHash = {};
    var hotelHallMinSum = 0, hotelHallMaxSum = 0;
    var hardwareHash = {};
    $.each(hotel.halls, function(i, el) {
      
      var min = 1000000, max = 0;
      $.each(el.configurations, function(i, config) {
        configHash[config.name] = 1;
        min = Math.min(min, config.people);
        max = Math.max(max, config.people);
      });
      hotelHallMinSum = min;
      hotelHallMaxSum = max;
      if ((el['Konferencijoms'] || '').toLowerCase() == 'y') {
        prep.hall.conference = true;
      }
      if ((el['Pobūviams'] || '').toLowerCase() == 'y') {
        prep.hall.celebration = true;
      }
      $.each(el.hardware, function(i, hardware) {
        hardwareHash[hardware] = true;
      });
    });
    prep.hall.minCap = hotelHallMinSum;
    prep.hall.maxCap = hotelHallMaxSum;
    prep.hall.configs = configHash;
    prep.hall.hardware = hardwareHash;
    
    var arr = hotel.info['Maitinimo paslaugos'].split(',');
    $.each(arr, function(i, item) {
      prep.food[item.trim()] = true;
    });
    
    hotel.prep = prep;
  };
  
  var firstPassData = function() {
    var newList = [];
    for (var i in hotels) {
      var hotel = hotels[i];
      var c = addrs[hotel.address];
      if (c) {
        firstPass(hotel);
        newList.push(hotel);
      }
    }
    hotels = newList; // Override hotel list
  };
  
  firstPassData();
  
  // UI CODE
  
  var $sidebar = $('#sidebar');
  
  var test = function(item, model) {
    
    if (!model.grades[item.prep.star]) {
      return false; //Doesn't have required star
    }
    
    if (model.hall) {
      
      if (item.prep.hall.count < model.hall.count) {
        return false; // not enough conference halls
      }
      
      if ((item.prep.hall.minCap < model.hall.capacity[0] && item.prep.hall.minCap < model.hall.capacity[0]) 
          || (item.prep.hall.minCap > model.hall.capacity[1] && item.prep.hall.minCap > model.hall.capacity[1])) {
        return false;// conference halls contain either to small or too big of a capacity
      }
      
      if (model.hall.configuration.length > 0) {
        var passed = false;
        $.each(model.hall.configuration, function(i, el) {
          if (item.prep.hall.configs[el]) {
            passed = true;
          }
        });
        if (!passed) {
          return false; // At least one configuration must exist in this hotel, none exist
        }
      }
      
      if (model.hall.hardware.length > 0) {
        var passed = true;
        $.each(model.hall.hardware, function(i, el) {
          if (!item.prep.hall.hardware[el]) {
            passed = false;
          }
        });
        if (!passed) {
          return false; // Every selected hardware must exist in this hotel, but it doesn't
        }
      }
      
      if (model.hall.celebration) {
        if (!item.prep.hall.celebration) {
          return false; // Hotel is not suitable for disabled people
        }
      }
      
      if (model.hall.conference) {
        if (!item.prep.hall.conference) {
          return false; // Hotel is not suitable for disabled people
        }
      }
      
    }
    if (model.hotel) {
      if (item.prep.capacity < model.hotel.capacity[0] || item.prep.capacity > model.hotel.capacity[1]) {
        return false;// hotel contains either to small or too big of a capacity
      }
      if (item.prep.roomCapacity < model.hotel.roomCapacity[0] || item.prep.roomCapacity > model.hotel.roomCapacity[1]) {
        return false;// hotel contains either to small or too big of a room capacity
      }
      
      if (model.hotel.food.length > 0) {
        var passed = false;
        $.each(model.hotel.food, function(i, el) {
          if (item.prep.food[el]) {
            passed = true;
          }
        });
        if (!passed) {
          return false; // At least one configuration must exist in this hotel, none exist
        }
      }
      
      if (model.hotel.forDisabled) {
        if (!item.prep.forDisabled) {
          return false; // Hotel is not suitable for disabled people
        }
      }
    }
    
    return true;
  };
  
  var filter = function(model) {
    for (var i in hotels) {
      var hotel = hotels[i];
      var c = addrs[hotel.address];
      if (c) {
        toggleMarker(hotel.name, new google.maps.LatLng(c.lat, c.lng), hotel, test(hotel, model));
      }
    }
  };
  
  var readRange = function($slider) {
    return [$slider.slider( "values", 0 ), $slider.slider( "values", 1 )];
  };
  
  var writeLabel = function($label, values) {
    $label.text(values[0] + ' - ' + values[1]);
  };
  
  var executeFilter = function() {
    
    setTimeout(function(){
      var model = {};
      //Determine selected type
      var type = [];
      $sidebar.find('.model-type-hall').is(':checked') && type.push('hall');
      $sidebar.find('.model-type-hotel').is(':checked') && type.push('hotel');
      model.type = type.join('_');

      model.grades = {};
      $sidebar.find('.model-grade .btn').each(function() {
        var $this = $(this);
        if ($this.hasClass('active')) {
          model.grades[$this.data('value') + ''] = true;
        }
      });
      
      //Get filter model for conference halls
      if (model.type == 'hall' || model.type == 'hall_hotel') {
        model.hall = {
          count: $sidebar.find('.model-hall-count').slider('value'),
          capacity: readRange($sidebar.find('.model-hall-capacity')),
          configuration: $.map($sidebar.find('.model-hall-configuration').select2("data"), function(el) { return el.id; }),
          celebration: $sidebar.find('.model-hall-celebration').is(':checked'),
          conference: $sidebar.find('.model-hall-conference').is(':checked'),
          hardware: $.map($sidebar.find('.model-hall-hardware').select2("data"), function(el) { return el.id; })
        };

        $sidebar.find('.label-hall-count').text(model.hall.count);
        writeLabel($sidebar.find('.label-hall-capacity'), model.hall.capacity);
      }
      //Get filter model for hotel
      if (model.type == 'hotel' || model.type == 'hall_hotel') {
        model.hotel = {
            capacity: readRange($sidebar.find('.model-hotel-capacity')),
            roomCapacity: readRange($sidebar.find('.model-hotel-room-capacity')),
            food: $.map($sidebar.find('.model-hotel-food').select2("data"), function(el) { return el.id; }),
            forDisabled: $sidebar.find('.model-hotel-for-disabled').is(':checked')
        };
        writeLabel($sidebar.find('.label-hotel-capacity'), model.hotel.capacity);
        writeLabel($sidebar.find('.label-hotel-room-capacity'), model.hotel.roomCapacity);
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
  $sidebar.find('.model-type-hall, .model-type-hotel, .model-hotel-for-disabled, .model-hall-celebration, .model-hall-conference').change(executeFilter);
  
  $sidebar.find('.model-grade .btn').click(toggleAndExecute);
  
  $sidebar.find('.model-hall-count').slider({
    range: 'max',
    min: 1,
    max: 10,
    value: 1,
    slide: executeFilter
  });
  
  var commonOptions = {
    range: true,
    min: 1,
    max: 500,
    values: [ 1, 500 ],
    slide: executeFilter
  };
  
  $sidebar.find('.model-hall-capacity, .model-hotel-capacity, .model-hotel-room-capacity').slider(commonOptions);
  
  $sidebar.find('.model-hall-configuration, .model-hall-hardware, .model-hotel-food').select2().on('change', executeFilter);
  
  //first execution
  executeFilter();
});
