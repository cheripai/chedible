// Animates and sets value for buttons on add dish form
$('#radioBtn a').on('click', function(){
    var sel = $(this).data('title');
    var tog = $(this).data('toggle');
    $('#'+tog).prop('value', sel);
    
    $('a[data-toggle="'+tog+'"]').not('[data-title="'+sel+'"]').removeClass('active').addClass('notActive');
    $('a[data-toggle="'+tog+'"][data-title="'+sel+'"]').removeClass('notActive').addClass('active');
})


// Sets value for form action based on which table to search
$('#table_ddmi').on('click', function(){
    var sel = $(this).children(":selected").prop('value');
    $('#search_table').prop('action', sel);
})


/* For changing value of voting system */
$("[id^=upvote]").click(function(){
    var index = parseInt($(this).attr('id').replace('upvote', ''), 10);
    $.getJSON($SCRIPT_ROOT + '/vote', {
        vote: 'upvote',
        id: index
    }, function(data) {
        var count = $('#count' + index);
        var uparrow = $('#upvote' + index);
        var downarrow = $('#downvote' + index);
        if(count.text() < data.result){
            uparrow.css('color', '#337AB7');
            downarrow.css('color', '#777');
        }
        else{
            uparrow.css('color', '#777');
        }
        count.text(data.result);
    });
});


$("[id^=downvote]").click(function(){
    var index = parseInt($(this).attr('id').replace('downvote', ''), 10);
    $.getJSON($SCRIPT_ROOT + '/vote', {
        vote: 'downvote',
        id: index
    }, function(data) {
        var count = $('#count' + index);
        var uparrow = $('#upvote' + index);
        var downarrow = $('#downvote' + index);
        if(count.text() > data.result){
            downarrow.css('color', '#337AB7');
            uparrow.css('color', '#777');
        }
        else{
            downarrow.css('color', '#777');
        }
        count.text(data.result);
    });
});


/* Animates carousel on index page */
$(document).ready( function() {
    $('#indexCarousel').carousel({
		interval:   4000
	});
	
	var clickEvent = false;
	$('#indexCarousel').on('click', '.nav a', function() {
			clickEvent = true;
			$('.nav li').removeClass('active');
			$(this).parent().addClass('active');		
	}).on('slide.bs.carousel', function(e) {
		if(!clickEvent) {
			var count = $('.nav').children().length - 1;
			var current = $('.nav li.active');
			current.removeClass('active').next().addClass('active');
			var id = parseInt(current.data('slide-to'));
			if(count == id) {
				$('.nav li').first().addClass('active');	
			}
		}
		clickEvent = false;
	});
});

/* Prevents #search_ddm from closing when clicking inside of it */
$('#search_ddm').on('click', function(event){
    var events = $._data(document, 'events') || {};
    events = events.click || [];
    for(var i = 0; i < events.length; i++) {
        if(events[i].selector) {

            //Check if the clicked element matches the event selector
            if($(event.target).is(events[i].selector)) {
                events[i].handler.call(event.target, event);
            }

            // Check if any of the clicked element parents matches the 
            // delegated event selector (Emulating propagation)
            $(event.target).parents(events[i].selector).each(function(){
                events[i].handler.call(this, event);
            });
        }
    }
    event.stopPropagation(); //Always stop propagation
});
