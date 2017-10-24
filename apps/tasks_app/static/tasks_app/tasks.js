$(document).ready(function () {
    $('.remove_user').submit(function(e) {
        e.preventDefault();
        var taskid = $(this).attr('task');
        $.post('/tasks/'+taskid+'/removeuser', $.param($(this).serializeArray()), function() {
            $('#modal').load("/tasks/"+taskid+"/task_users");
        });
    });
    $('.add_user').submit(function(e) {
        e.preventDefault();
        var taskid = $(this).attr('task');
        $.post('/tasks/'+taskid+'/adduser', $.param($(this).serializeArray()), function() {
            $('#modal').load("/tasks/"+taskid+"/task_users");
        });
    });
});
