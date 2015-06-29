// Animates and sets value for buttons on add dish form
$('#radioBtn a').on('click', function(){
    var sel = $(this).data('title');
    var tog = $(this).data('toggle');
    $('#'+tog).prop('value', sel);
    
    $('a[data-toggle="'+tog+'"]').not('[data-title="'+sel+'"]').removeClass('active').addClass('notActive');
    $('a[data-toggle="'+tog+'"][data-title="'+sel+'"]').removeClass('notActive').addClass('active');
})


// Animates and sets value for drop-down menu in search bar
$('.table_ddmi').on('click', function(){
    var sel = $(this).data('title');
    var tog = $(this).data('toggle');
    var btn = $(this).data('button');
    $('#'+tog).prop('action', sel);
    $('#'+btn).text($(this).text()+' ');
})


/* For changing value of voting system */
$("[id^=upvote]").click(function(){
    var index = parseInt($(this).attr('id').replace('upvote', ''), 10);
    $.getJSON($SCRIPT_ROOT + '/vote', {
        vote: 'upvote',
        id: index
    }, function(data) {
        var count = $('#count' + index);
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
        count.text(data.result);
    });
});
