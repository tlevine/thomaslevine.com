import jwt,time,json
DEVELOPMENT=False

sellerIdentifier='05893252188137793034'
SELLER_SECRET='c7ehLOf_pbyEEqy4-eVZsA' if DEVELOPMENT else '_XlCAY7Tgi5xmsHg-K8SUA'

def maketoken(coinname,cents):
  return jwt.encode(
  {
    "iss" : sellerIdentifier,
    "aud" : "Google",
    "typ" : "google/payments/inapp/item/v1",
    "exp" : int(time.time() + 3600),
    "iat" : int(time.time()),
    "request" :{
      "name" : coinname,
      "description" : "You're dropping a %s in Tom's tip jar" % coinname,
      "price" : "0.%02d" % cents,
      "currencyCode" : "USD",
      "sellerData" : ""
    }
  },
  SELLER_SECRET)


if __name__ == "__main__":
  print "jwts=%s;" % json.dumps({
    "penny":maketoken("Penny",1)
  , "nickel":maketoken("Nickel",5)
  , "dime":maketoken("Dime",10)
  })

