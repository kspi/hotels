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

$(function() {
  
  var $sidebar = $('#sidebar');
  
  var filter = function(model) {
    console.log(model);
  };
  
  var readRange = function($slider) {
    return [$slider.slider( "values", 0 ), $slider.slider( "values", 1 )];
  };
  
  var executeFilter = function() {
    
    setTimeout(function(){
      var model = {};
      console.log('execute filter');
      model.type = $sidebar.find('.model-type .active').data('type');
      $sidebar.find('.model-hall').toggle(model.type == 'hall');
      $sidebar.find('.model-hotel').toggle(model.type == 'hotel');
      model.forDisabled = $sidebar.find('.model-for-disabled').is(':checked');
      
      model.vacancies = readRange($sidebar.find('.model-vacancy-count'));
      model.grades = [];
      $sidebar.find('.model-grade .btn').each(function() {
        var $this = $(this);
        if ($this.hasClass('active')) {
          model.grades.push($this.data('value'));
        }
      });
      
      
      
      filter(model);
    }, 1);   
  };
  
  var toggleAndExecute = function() {
    $(this).toggleClass('active');
    executeFilter();
  };
  
  var toggleChildrenAndExecute = function() {
    $(this).addClass('active').siblings().removeClass('active');
    executeFilter();
  };
  $sidebar.find('.model-type .btn').click(toggleChildrenAndExecute);
  
  $sidebar.find('.model-for-disabled').change(executeFilter);
  
  $sidebar.find('.model-grade .btn').click(toggleAndExecute);

  $sidebar.find('.model-vacancy-count').slider({
    range: true,
    min: 0,
    max: 100,
    values: [ 10, 80 ],
    slide: executeFilter
  });
  
  $sidebar.find('.model-needed-count').slider({
    min: 0,
    max: 100,
    values: [ 50 ],
    slide: executeFilter
  });
  
  //first execution
  executeFilter();
});