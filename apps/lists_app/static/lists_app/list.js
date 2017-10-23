$(document).ready(function () {
    $('.modal_toggle').click(function(e) {
        var id = $(this).attr('task');
        $('#modal').load("/tasks/"+id+"/task_users");
    });
});
