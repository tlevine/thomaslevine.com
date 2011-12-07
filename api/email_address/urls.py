from django.conf.urls.defaults import patterns, include, url
from views import make_email_address

urlpatterns = patterns('',
  url(r'^email.js$',make_email_address, name='email'),
)

