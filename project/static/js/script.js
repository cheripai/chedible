/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */


// Sets value for form action based on which table to search
$('.table_select a').on('click', function(){
    var sel = $(this).data('title');
    var tog = $(this).data('toggle');
    var queryValue = $('#query').val().toLowerCase();
    if(sel == 'restaurants')
    {
        $('#location_div').show();
        $('#all_restaurants_div').show();
    }
    else if(sel == 'dishes')
    {
        $('#location_div').show();
        $('#all_restaurants_div').hide();
    }
    else
    {
        $('#location_div').hide();
        $('#all_restaurants_div').hide();
    }
    $('#'+tog).prop('action', '/search/'+sel);
})


// Grabs the user's location to find nearby restaurants
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
            var rev_geocode = 'https://nominatim.openstreetmap.org/reverse?format=json&lat='
            $.getJSON(rev_geocode + startPos.coords.latitude + '&lon=' + startPos.coords.longitude, 
                function(data) {
                    current_address = data.display_name;
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


// Sets value for distance based on radio switcher
$('.radius_select a').on('click', function(){
    var sel = $(this).data('title');
    var tog = $(this).data('toggle');
    $('#'+tog).val(sel);
})


// Places the text 'restaurant' in the query when searchAll is clicked
// Disables query so that user cannot change the value
$("#searchAll").click(function() {
    var searchAll = $("#searchAll");
    var query = $("#query");
    if(searchAll.is(':checked')) {
        query.val("Restaurants");
        query.prop("disabled", true);
    } else {
        query.prop("disabled", false);
        if(query.val().toLowerCase() == "restaurants") {
            query.val("");
        }
    }
});


// Resets query to enabled when form is submitted
// This allows the value of query to be sent
$(function ($) {        
    $('#search_table').bind('submit', function () {
        $("#query").prop('disabled', false);
    });
});


// Prevents #search_ddm from closing when clicking inside of it
$('#search_ddm').on('click', function(event){
    var events = $._data(document, 'events') || {};
    events = events.click || [];
    for(var i = 0; i < events.length; i++) {
        if(events[i].selector) {

            // Check if the clicked element matches the event selector
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


// Animates carousel on index page
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


// Animates and sets value for buttons on add dish form
$('#radioBtn a').on('click', function(){
    var sel = $(this).data('title');
    // Holds the name of the target input
    var tog = $(this).data('toggle');

    // Sets the value of the hidden, target input to the active value (data-title)
    $('#'+tog).prop('value', sel);

    // Animates toggle so that the currently selected toggle is blue and the others are gray
    $('a[data-toggle="'+tog+'"]').not('[data-title="'+sel+'"]').removeClass('active').addClass('notActive');
    $('a[data-toggle="'+tog+'"][data-title="'+sel+'"]').removeClass('notActive').addClass('active');
})


// AJAX call to add restaurant location to database
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


// For changing value of voting system
$("[id^=upvote]").click(function(){
    // Gets id of dish clicked
    var dish_id = parseInt($(this).attr('id').replace('upvote', ''), 10);
    $.getJSON($SCRIPT_ROOT + '/vote', {
        vote: 'upvote',
        id: dish_id
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


// For posting comment to dish modal 
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


// For changing value of voting system
$("[id^=downvote]").click(function(){
    var dish_id = parseInt($(this).attr('id').replace('downvote', ''), 10);
    $.getJSON($SCRIPT_ROOT + '/vote', {
        vote: 'downvote',
        id: dish_id
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


// Fixes bug where opening a modal shifts contents of the page
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
