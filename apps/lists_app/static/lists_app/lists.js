$(document).ready(function () {
    $('.remove_user').submit(function(e) {
        e.preventDefault();
        var listid = $(this).attr('list');
        $.post('/lists/'+listid+'/removeuser', $.param($(this).serializeArray()), function() {
            $('#modal').load("/lists/"+listid+"/list_users");
        });
    });
    $('.add_user').submit(function(e) {
        e.preventDefault();
        var listid = $(this).attr('list');
        $.post('/lists/'+listid+'/adduser', $.param($(this).serializeArray()), function() {
            $('#modal').load("/lists/"+listid+"/list_users");
        });
    });
});
