$(document).ready(function(){
    if(!window.location.hash) {
        $(".login").fadeIn('fast');
    }
    else if(window.location.hash == '#register') {
        $(".register").fadeIn('fast');
    }
    else if(window.location.hash == '#company') {
        $(".company").fadeIn('fast');
    }
    $(".loginMod").click(function() {
        $(this).parent(".module").fadeOut('fast');
        $(".login").fadeIn();
    });
    $(".registerMod").click(function() {
        $(this).parent(".module").fadeOut('fast');
        $(".register").fadeIn();
    });
    $(".companyMod").click(function() {
        $(this).parent(".module").fadeOut('fast');
        $(".company").fadeIn();
    });
});
