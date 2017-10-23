$(document).ready(function () {
    $('.modal_toggle').click(function(e) {
        var id = $(this).attr('task');
        $('#modal').load("/tasks/"+id+"/task_users");
    });
    $('.remove_user').submit(function(e) {
        e.preventDefault();
        var taskid = $(this).attr('task');
        $.post('/tasks/'+taskid+'/removeuser', $.param($(this).serializeArray()), function() {
            $('#modal').load("/tasks/"+taskid+"/task_users");
        });
    });
});
