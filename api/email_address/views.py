from django.shortcuts import render_to_response
from models import EmailAddress

def make_email_address(request):
  try:
    e=EmailAddress.objects.filter(used=False)[0]
  except IndexError:
    username='ligature'
  else:
    e.REMOTE_ADDR=request.META['REMOTE_ADDR']
    e.used=True
    e.save()
    username=e.username
  return render_to_response('email.js',{"username":username},mimetype="text/javascript")
