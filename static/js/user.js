$(document).ready(function() {
    
    //Enable Tab Card for User Profile
    var current_url = window.location.pathname.split('/');
    if (current_url[1] == 'recipez' && current_url[2] == 'user_profile') {
        tabCardActivate();
    }

});

  // Function of Tab Card for User Profile
  function tabCardActivate() {
    var nav_items1 = $('.nav-link.1');
    var tab_items1 = $('.tab-pane.1');
    $(nav_items1[0]).addClass('active');
    $(tab_items1[0]).addClass('active');

    $(nav_items1).click(function(){
        var id = $(this).attr('id');
        console.log(id);
        $(nav_items1).removeClass('active');
        $(this).addClass('active');
        $(tab_items1).removeClass('active');
        $(tab_items1).removeClass('show').addClass('fade');
        $('#'+id+'-post').addClass('active');
        $('#'+id+'-post').addClass('show');
    });
    
    var nav_items2 = $('.nav-link.2');
    var tab_items2 = $('.tab-pane.2');
    $(nav_items2[0]).addClass('active');
    $(tab_items2[0]).addClass('active');

    $(nav_items2).click(function(){
        var id = $(this).attr('id');
        console.log(id);
        $(nav_items2).removeClass('active');
        $(this).addClass('active');
        $(tab_items2).removeClass('active');
        $(tab_items2).removeClass('show');
        $('#'+id+'-saved').addClass('active');
        $('#'+id+'-saved').addClass('show');
    });
  }