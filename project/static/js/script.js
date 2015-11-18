/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */


// Animates and sets value for buttons on add dish form
$('#radioBtn a').on('click', function(){
    var sel = $(this).data('title');
    var tog = $(this).data('toggle');
    $('#'+tog).prop('value', sel);
    
    $('a[data-toggle="'+tog+'"]').not('[data-title="'+sel+'"]').removeClass('active').addClass('notActive');
    $('a[data-toggle="'+tog+'"][data-title="'+sel+'"]').removeClass('notActive').addClass('active');
})


// Sets value for form action based on which table to search
$('.table_select a').on('click', function(){
    var sel = $(this).data('title');
    var tog = $(this).data('toggle');
    var queryValue = $('#query').val().toLowerCase();
    if(sel == 'restaurants' && queryValue == '')
    {
        $('#query').val('');
    }
    if(sel != 'restaurants' && queryValue == 'restaurants')
    {
        $('#query').val('');
    }
    if(sel != 'users')
    {
        $('#location_div').show();
    }
    else
    {
        $('#location_div').hide();
    }
    $('#'+tog).prop('action', '/search/'+sel);
})


// Sets value for distance based on radio switcher
$('.radius_select a').on('click', function(){
    var sel = $(this).data('title');
    var tog = $(this).data('toggle');
    $('#'+tog).val(sel);
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
            uparrow.addClass('active');
            downarrow.removeClass('active');
        }
        else{
            uparrow.removeClass('active');
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
            downarrow.addClass('active');
            uparrow.removeClass('active');
        }
        else{
            downarrow.removeClass('active');
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


/* Grabs the user's location to find nearby restaurants */
$('#locationButton').on('click', function(event){
    if(navigator.geolocation) {
        var startPos;
        var geoOptions = {
            // 5 minutes maximum age to request updated location
            maximumAge: 5 * 60 * 1000,
            // 10 second maximum timeout
            timeout: 10 * 1000,
        }
        var geoSuccess = function(position) {
            startPos = position;
            var rev_geocode = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=';
            $.getJSON(rev_geocode + startPos.coords.latitude + ',' + startPos.coords.longitude, 
                function(data) {
                    current_address = data.results[0].formatted_address;
                    document.getElementById('locationInput').value = current_address;
                });
        };
        var geoError = function(position) {
            console.log('Error occurred. Error code: ' + error.code);
            // error.code can be:
            //   0: unknown error
            //   1: permission denied
            //   2: position unavailable (error response from location provider)
            //   3: timed out
        };
        navigator.geolocation.getCurrentPosition(geoSuccess, geoError, geoOptions);
    }
    else {
        alert('Your device does not support geolocation');
    }
});


/* Fixes bug where opening a modal shifts contents of the page */
$(document).ready(function(){
    $(window).load(function(){
        var oldSSB = $.fn.modal.Constructor.prototype.setScrollbar;
        $.fn.modal.Constructor.prototype.setScrollbar = function () 
        {
            oldSSB.apply(this);
            if(this.bodyIsOverflowing && this.scrollbarWidth) 
            {
                $('.navbar-fixed-top, .navbar-fixed-bottom').css('padding-right', this.scrollbarWidth);
            }       
        }

        var oldRSB = $.fn.modal.Constructor.prototype.resetScrollbar;
        $.fn.modal.Constructor.prototype.resetScrollbar = function () 
        {
            oldRSB.apply(this);
            $('.navbar-fixed-top, .navbar-fixed-bottom').css('padding-right', '');
        }
    });
});


/* For posting comment to dish modal */
$("[id^=post]").click(function(){
    var index = parseInt($(this).attr('id').replace('post', ''), 10);
    var content = $('#content'+index).val();
    encoded_content = encodeURIComponent(content).replace(/[!'()]/g, escape).replace(/\*/g, "%2A");
    $.getJSON($SCRIPT_ROOT + '/comment', {
        content: encoded_content,
        id: index
    }, function(data) {
        if(data.error) {
            $('#error-msg'+index).removeAttr('hidden');
            $('#error-msg'+index).text(data.error);
            return;
        }
        $('#hidden-content'+index).text(content);
        $('#hidden-comment'+index).removeAttr('hidden');
        $('#content'+index).val('');
        $('#content'+index).attr('disabled', 'disabled');
        $('#content'+index).attr('placeholder', 'Submitted!');
        $('#post'+index).attr('disabled', true);
        $('#hidden-date'+index).text(data.date);
    });
});


addLocation = function(button, google_id, lat, lng, address) {
    // This retrieves the restaurant_id from the URL
    var restaurant_id = window.location.pathname.replace(/\/\s*$/,'').split('/')[2];
    $.getJSON(window.location.origin + '/restaurant/'+restaurant_id+'/add_location', {
        google_id: google_id,
        lat: lat,
        lng: lng,
        address: address
    }, function(data) {
        button.disabled = true;
        button.innerHTML = 'Added';
    });
};
