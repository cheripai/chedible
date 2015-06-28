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
    var index = parseInt($(this).attr("id").replace('upvote', ''), 10);
    var count = $("#count" + index);
    var n = parseInt(count.text());
    count.text(n+1);
});


$("[id^=downvote]").click(function(){
    var index = parseInt($(this).attr("id").replace('downvote', ''), 10);
    var count = $("#count" + index);
    var n = parseInt(count.text());
    count.text(n-1);
});
