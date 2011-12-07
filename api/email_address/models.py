from django.db import models

class EmailAddress(models.Model):
  username=models.CharField(max_length=42)
  date=models.DateTimeField(auto_now=True)
  REMOTE_ADDR=models.IPAddressField(blank=True)
  used=models.BooleanField(default=False)
  def __uni__(self):
    return self.address
