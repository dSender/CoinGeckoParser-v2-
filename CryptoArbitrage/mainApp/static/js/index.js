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
        $(this).text('Hide');
        $(this).attr('value', 'showed');
        $(c).show();
    }
  });

  var market_buttons = $('.market-button');
  var mrkets_field = $('#id_markets');

  var selected_markets = mrkets_field.val().split('/');


  for (var j=0; j<selected_markets.length; j++){
    for (var i=0; i<market_buttons.length; i++){
      if (selected_markets[j] == market_buttons.eq(i).attr('name')){
        market_buttons.eq(i).attr({'style': 'background-color:#ffc107;'});
        break;
      }
    }
  }

  $(market_buttons).click(function(){
    var selected_markets = mrkets_field.val().split('/');
    var exist_val = mrkets_field.val();
    var n_val = $(this).attr('name');
    var flag_market_in_field = false;
    for (var i=0; i<selected_markets.length; i++){
        if (selected_markets[i] == n_val){
            flag_market_in_field = true;
            break;
        }
    }
    if (!flag_market_in_field){
        var new_field_val = exist_val + '/' + n_val;
        mrkets_field.val(new_field_val);
        $(this).attr({'style': 'background-color:#ffc107;'});
    }
    else{
        var new_field_val = '';
        for (var i=0; i<selected_markets.length; i++){
            if (selected_markets[i] != n_val){
                if (i != 0){
                    new_field_val = new_field_val + '/' + selected_markets[i];
                }
                else{
                    new_field_val = new_field_val + selected_markets[i];
                }
            }
        }
        mrkets_field.val(new_field_val);
        $(this).attr({'style': 'background-color:#ffffff;'});
    }
  });
});
