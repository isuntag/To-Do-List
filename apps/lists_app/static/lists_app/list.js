$(document).ready(function () {
    // $('.toggle_modal').click(function (e) {
    //     e.preventDefault();
    //     $.ajax({
    //         type: "POST",
    //         url: "myphp.php",
    //         data: { id: this.id },
    //         dataType: "json",
    //         success: function (msg) {
    //             if (msg.success) {
    //                 $("#one").html(msg);
    //             } else {
    //                 alert("error");
    //             }
    //         }
    //     });
    // });
    $('.remove_user').on('submit', function () {
        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function() { // on success..
                $('.modal-body').load(document.URL + '.modal-body'); // update the DIV
            }
        });
        return false;
    });
    // $('.edit-modal').click(function(ev) { // for each update url
    //     ev.preventDefault(); // prevent navigation
    //     var url = $(this).data('form'); // get the update form url
    //     $('#RSVPModal').load(url, function() { // load the url into the modal
    //         $(this).modal('show'); // display the modal on url load
    //     });
    //     return false; // prevent click propagation
    // });
});
