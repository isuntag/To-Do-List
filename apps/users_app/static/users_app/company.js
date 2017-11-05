$(document).ready(function () {
    $('.modal_toggle').click(function(e) {
        var id = $(this).attr('list');
        $('#modal').load("/lists/"+id+"/list_users");
    });
})
