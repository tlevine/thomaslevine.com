google.load('payments', '1.0', {
  'packages': ['sandbox_config']
});

jwts={
  penny:"abc"
, nickel:"abc"
, dime:"abc"
};

function tip(jwt){
  goog.payments.inapp.buy({
    'jwt'     : jwts[jwt],
    'success' : successHandler,
    'failure' : failureHandler
  });
}
