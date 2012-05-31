/* Author: Thomas Levine

*/
$(function(){
  var chainsaw=['occurrence','thomaslevine.com'].join('@');
  document.getElementById("e-post").innerHTML=chainsaw;
  $('.not-ie .card').each(function(i){
    $(this).delay(100*i).animate({opacity:1},'1000');
  });
});

/* Tips */

jwts={"penny": "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJhdWQiOiAiR29vZ2xlIiwgImlzcyI6ICIwNTg5MzI1MjE4ODEzNzc5MzAzNCIsICJyZXF1ZXN0IjogeyJjdXJyZW5jeUNvZGUiOiAiVVNEIiwgInByaWNlIjogIjAuMDEiLCAic2VsbGVyRGF0YSI6ICIiLCAibmFtZSI6ICJQZW5ueSIsICJkZXNjcmlwdGlvbiI6ICJZb3UncmUgZHJvcHBpbmcgYSBwZW5ueSBpbiBUb20ncyB0aXAgamFyLiJ9LCAiZXhwIjogMTMyNTQ4NTI5MCwgImlhdCI6IDEzMjU0ODE2OTAsICJ0eXAiOiAiZ29vZ2xlL3BheW1lbnRzL2luYXBwL2l0ZW0vdjEifQ.xE9vktiMQnhJEbE17VEM4T7hCwy5FvwQM5j5o_symvM", "nickel": "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJhdWQiOiAiR29vZ2xlIiwgImlzcyI6ICIwNTg5MzI1MjE4ODEzNzc5MzAzNCIsICJyZXF1ZXN0IjogeyJjdXJyZW5jeUNvZGUiOiAiVVNEIiwgInByaWNlIjogIjAuMDUiLCAic2VsbGVyRGF0YSI6ICIiLCAibmFtZSI6ICJOaWNrZWwiLCAiZGVzY3JpcHRpb24iOiAiWW91J3JlIGRyb3BwaW5nIGEgbmlja2VsIGluIFRvbSdzIHRpcCBqYXIuIn0sICJleHAiOiAxMzI1NDg1MjkwLCAiaWF0IjogMTMyNTQ4MTY5MCwgInR5cCI6ICJnb29nbGUvcGF5bWVudHMvaW5hcHAvaXRlbS92MSJ9.0_7BHBc9O76OWLUsyqcMOvpf_Pv784ewMfC4-8lxSbY", "dime": "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJhdWQiOiAiR29vZ2xlIiwgImlzcyI6ICIwNTg5MzI1MjE4ODEzNzc5MzAzNCIsICJyZXF1ZXN0IjogeyJjdXJyZW5jeUNvZGUiOiAiVVNEIiwgInByaWNlIjogIjAuMTAiLCAic2VsbGVyRGF0YSI6ICIiLCAibmFtZSI6ICJEaW1lIiwgImRlc2NyaXB0aW9uIjogIllvdSdyZSBkcm9wcGluZyBhIGRpbWUgaW4gVG9tJ3MgdGlwIGphci4ifSwgImV4cCI6IDEzMjU0ODUyOTAsICJpYXQiOiAxMzI1NDgxNjkwLCAidHlwIjogImdvb2dsZS9wYXltZW50cy9pbmFwcC9pdGVtL3YxIn0.Fu-Q2aGvvnSnt6Fp2AIfoCNtbFM9322JYCMKY72kTaU"};

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
  goog.payments.inapp.buy({
    'jwt'     : jwts[coinname],
    'success' : successHandler,
    'failure' : failureHandler
  });
  $('#sopa').hide();
}
