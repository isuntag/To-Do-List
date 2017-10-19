$(document).ready(function() {
    $('.circle').each(function() {
        if($(this).outerHeight() > $(this).width()) {
            $(this).css('width', $(this).outerHeight());
        }
        if($(this).outerWidth() > $(this).height()) {
            $(this).css('height', $(this).outerWidth());
        }
    });
    $('.check').each(function() {
        if($(this).outerHeight() > $(this).width()) {
            $(this).css('width', $(this).outerHeight());
        }
        if($(this).outerWidth() > $(this).height()) {
            $(this).css('height', $(this).outerWidth());
        }
    });
});
