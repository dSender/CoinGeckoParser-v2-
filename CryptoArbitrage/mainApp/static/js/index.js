$(document).ready(function(){
  var hide_network_buttons = $('.hide-show-network-a');
  $(hide_network_buttons).click(function(){
      var net = $(this).attr('class').split(' ')[1];
      var val = $(this).attr('value');
      if (val == 'showed'){
          $(this).text('Show');
          $(net).hide();
          $(this).attr('value', 'hidden');
      }
      else{
        var pos = $(this).offset();
        window.scrollTo(0, 0);
        $(this).text('Hide');
        $(this).attr('value', 'showed');
        $(net).show();
      }
    });
  var hide_coin_button = $('.hide-show-coins');
  $(hide_coin_button).click(function(){
    var c = $(this).attr('class').split(' ')[1];
    var val = $(this).attr('value');
    if (val == 'showed'){
        $(this).text('Show');
        $(c).hide();
        $(this).attr('value', 'hidden');
    }
    else{
      var pos = $(this).offset();
      window.scrollTo(0, 0);
      $(this).text('Hide');
      $(this).attr('value', 'showed');
      $(c).show();
    }
  });
});
