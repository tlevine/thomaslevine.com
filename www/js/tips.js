//Success handler
var successHandler = function(purchaseAction){
  if (window.console != undefined) {
    console.log("Purchase completed successfully.");
  }
}

//Failure handler
var failureHandler = function(purchaseActionError){
  if (window.console != undefined) {
    console.log("Purchase did not complete.");
  }
}

function tip(coinname){
  $('#sopa').hide();
  goog.payments.inapp.buy({
    'jwt'     : jwts[coinname],
    'success' : successHandler,
    'failure' : failureHandler
  });
}
