import web
import jwt,time

urls = (
  '/','Tips',
  '/penny','Penny',
  '/nickel','Nickel',
  '/dime','Dime',
)
t_globals = {
    'datestr': web.datestr
}
render = web.template.render('templates', base='base', globals=t_globals)
app = web.application(urls, globals())

sellerIdentifier='05893252188137793034'
SELLER_SECRET='_XlCAY7Tgi5xmsHg-K8SUA'

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

#class Coin:
#  def __init__(self,coinname,cents):
#    self.coinname=unicode(coinname)
#    self.cents=int(cents)
#  def GET(self):
#    return maketoken(self.coinname,self.cents)

class Penny:
  def GET(self):
    return render.coin(maketoken("Penny",1))

class Nickel:
  def GET(self):
    return maketoken("Nickel",5)

class Quarter:
  def GET(self):
    return maketoken("Dime",10)

if __name__ == "__main__":
  app.run()
